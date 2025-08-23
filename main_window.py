"""
Teresa V2 主界面 - 现代化设计
集成所有高级功能的主窗口
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QMenu, QStatusBar, QSystemTrayIcon, QApplication,
    QToolBar, QSpacerItem, QSizePolicy, QFrame, QStackedWidget,
    QFileDialog, QMessageBox, QDialog, QLabel
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QAction, QIcon, QPixmap, QShortcut, QKeySequence
from datetime import datetime
import sys
import json

# 导入自定义模块
from modern_ui import (
    ModernButton, ChatScrollArea, ModernLineEdit, SidebarHistoryList,
    TypingIndicator, ConversationItem
)
from config import config
from features import (
    smart_suggestions, notification_manager, search_manager,
    conversation_exporter, chat_analyzer
)
from TeresaV2_HistoryUI import HistoryManager
from settings_dialog import SettingsDialog
from about_dialog import AboutDialog
from ai_provider import AIProvider

class MainWindow(QMainWindow):
    """主窗口类"""
    
    conversation_changed = pyqtSignal(str)  # 对话切换信号
    
    def __init__(self):
        super().__init__()
        
        # 初始化核心组件
        self.history_manager = HistoryManager()
        self.ai_provider = AIProvider()
        self.current_conv_id = None
        self.is_generating = False
        
        # UI状态
        self.sidebar_visible = True
        self.typing_timer = QTimer()
        self.stats_status = None  # 预先声明属性
        
        # 设置窗口
        self.setup_window()
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_tool_bar()
        self.setup_status_bar()
        self.setup_shortcuts()
        self.setup_system_tray()
        
        # 连接信号
        self.setup_connections()
        
        # 应用主题
        self.apply_theme()
        
        # 加载数据
        self.load_conversations()
        
        # 显示欢迎消息
        self.show_welcome_message()
    
    def setup_window(self):
        """设置窗口属性"""
        self.setWindowTitle("Teresa V2 - AI Chat Assistant")
        self.setMinimumSize(1000, 700)
        self.resize(1400, 900)
        
        # 设置窗口图标
        # self.setWindowIcon(QIcon("assets/icon.png"))
        
        # 居中显示
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def setup_ui(self):
        """设置主UI布局"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        
        # 创建分割器
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.splitter)
        
        # 左侧边栏
        self.setup_sidebar()
        
        # 主聊天区域
        self.setup_chat_area()
        
        # 设置分割器比例
        self.splitter.setSizes([300, 1100])
        self.splitter.setCollapsible(0, True)
        self.splitter.setCollapsible(1, False)
    
    def setup_sidebar(self):
        """设置侧边栏"""
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(300)
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)
        self.sidebar_layout.setSpacing(10)
        self.sidebar.setLayout(self.sidebar_layout)
        
        # 标题和新建按钮
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("Conversations")
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: {config.appearance.font_size + 2}px;
                font-weight: bold;
                color: {config.get_theme_colors()['text_primary']};
            }}
        """)
        
        self.new_chat_btn = ModernButton("New Chat", style="primary")
        self.new_chat_btn.clicked.connect(self.start_new_chat)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.new_chat_btn)
        
        # 搜索框
        self.search_input = ModernLineEdit("Search conversations...")
        self.search_input.textChanged.connect(self.on_search_changed)
        
        # 历史列表
        self.history_list = SidebarHistoryList()
        self.history_list.itemSelected.connect(self.load_conversation)
        
        # 添加到布局
        self.sidebar_layout.addLayout(header_layout)
        self.sidebar_layout.addWidget(self.search_input)
        self.sidebar_layout.addWidget(self.history_list)
        
        # 统计信息
        self.stats_label = QLabel()
        self.update_stats()
        self.sidebar_layout.addWidget(self.stats_label)
        
        self.splitter.addWidget(self.sidebar)
    
    def setup_chat_area(self):
        """设置聊天区域"""
        self.chat_widget = QWidget()
        chat_layout = QVBoxLayout()
        chat_layout.setContentsMargins(10, 10, 10, 10)
        chat_layout.setSpacing(10)
        self.chat_widget.setLayout(chat_layout)
        
        # 聊天标题栏
        self.setup_chat_header()
        
        # 聊天消息区域
        self.chat_display = ChatScrollArea()
        chat_layout.addWidget(self.chat_display)
        
        # 打字指示器
        self.typing_indicator = TypingIndicator()
        self.typing_indicator.hide()
        chat_layout.addWidget(self.typing_indicator)
        
        # 输入区域
        self.setup_input_area(chat_layout)
        
        self.splitter.addWidget(self.chat_widget)
    
    def setup_chat_header(self):
        """设置聊天标题栏"""
        header_frame = QFrame()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_frame.setLayout(header_layout)
        
        # 对话标题
        self.chat_title = QLabel("Teresa V2 Assistant")
        self.chat_title.setStyleSheet(f"""
            QLabel {{
                font-size: {config.appearance.font_size + 4}px;
                font-weight: bold;
                color: {config.get_theme_colors()['text_primary']};
            }}
        """)
        
        # 操作按钮
        self.export_btn = ModernButton("Export", style="secondary")
        self.export_btn.clicked.connect(self.export_conversation)
        
        self.clear_btn = ModernButton("Clear", style="secondary")
        self.clear_btn.clicked.connect(self.clear_chat)
        
        header_layout.addWidget(self.chat_title)
        header_layout.addStretch()
        header_layout.addWidget(self.export_btn)
        header_layout.addWidget(self.clear_btn)
        
        self.chat_widget.layout().addWidget(header_frame)
    
    def setup_input_area(self, parent_layout):
        """设置输入区域"""
        input_frame = QFrame()
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_frame.setLayout(input_layout)
        
        # 主输入区域
        input_row = QHBoxLayout()
        input_row.setSpacing(10)
        
        # 多行输入框
        self.message_input = ModernLineEdit("Type your message...")
        self.message_input.returnPressed.connect(self.send_message)
        
        # 发送按钮
        self.send_btn = ModernButton("Send", style="primary")
        self.send_btn.clicked.connect(self.send_message)
        
        input_row.addWidget(self.message_input)
        input_row.addWidget(self.send_btn)
        
        # 智能建议（可选显示）
        self.suggestions_frame = QFrame()
        self.suggestions_layout = QHBoxLayout()
        self.suggestions_frame.setLayout(self.suggestions_layout)
        self.suggestions_frame.hide()
        
        input_layout.addWidget(self.suggestions_frame)
        input_layout.addLayout(input_row)
        
        parent_layout.addWidget(input_frame)
    
    def setup_menu_bar(self):
        """设置菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Chat", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.start_new_chat)
        file_menu.addAction(new_action)
        
        export_action = QAction("Export Chat", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(self.export_conversation)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu("Edit")
        
        clear_action = QAction("Clear Chat", self)
        clear_action.setShortcut(QKeySequence("Ctrl+Shift+C"))
        clear_action.triggered.connect(self.clear_chat)
        edit_menu.addAction(clear_action)
        
        settings_action = QAction("Settings", self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(self.open_settings)
        edit_menu.addAction(settings_action)
        
        # 视图菜单
        view_menu = menubar.addMenu("View")
        
        toggle_sidebar_action = QAction("Toggle Sidebar", self)
        toggle_sidebar_action.setShortcut(QKeySequence("Ctrl+B"))
        toggle_sidebar_action.triggered.connect(self.toggle_sidebar)
        view_menu.addAction(toggle_sidebar_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_tool_bar(self):
        """设置工具栏"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # 新建聊天
        new_action = QAction("New", self)
        new_action.triggered.connect(self.start_new_chat)
        toolbar.addAction(new_action)
        
        toolbar.addSeparator()
        
        # 导出
        export_action = QAction("Export", self)
        export_action.triggered.connect(self.export_conversation)
        toolbar.addAction(export_action)
        
        # 设置
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        toolbar.addAction(settings_action)
    
    def setup_status_bar(self):
        """设置状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 状态标签
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
        # 统计信息
        self.stats_status = QLabel()
        self.status_bar.addPermanentWidget(self.stats_status)
        
        self.update_status("Ready")
    
    def setup_shortcuts(self):
        """设置快捷键"""
        # 发送消息
        send_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        send_shortcut.activated.connect(self.send_message)
        
        # 新建聊天
        new_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        new_shortcut.activated.connect(self.start_new_chat)
        
        # 搜索
        search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        search_shortcut.activated.connect(self.focus_search)
    
    def setup_system_tray(self):
        """设置系统托盘"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            # self.tray_icon.setIcon(QIcon("assets/icon.png"))
            
            tray_menu = QMenu()
            show_action = tray_menu.addAction("Show")
            show_action.triggered.connect(self.show)
            
            quit_action = tray_menu.addAction("Quit")
            quit_action.triggered.connect(QApplication.instance().quit)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
    
    def setup_connections(self):
        """设置信号连接"""
        # 通知管理器
        notification_manager.notification_requested.connect(self.show_notification)
        
        # AI提供者连接
        self.ai_provider.response_ready.connect(self.on_ai_response)
        self.ai_provider.error_occurred.connect(self.on_ai_error)
        self.ai_provider.stream_chunk.connect(self.on_ai_stream_chunk)
    
    def apply_theme(self):
        """应用主题"""
        colors = config.get_theme_colors()
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background: {colors['bg_primary']};
                color: {colors['text_primary']};
            }}
            QFrame {{
                background: {colors['bg_secondary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
            QMenuBar {{
                background: {colors['bg_secondary']};
                color: {colors['text_primary']};
                border: none;
            }}
            QMenuBar::item {{
                background: transparent;
                padding: 8px 12px;
            }}
            QMenuBar::item:selected {{
                background: {colors['accent']};
            }}
            QStatusBar {{
                background: {colors['bg_secondary']};
                color: {colors['text_primary']};
                border-top: 1px solid {colors['border']};
            }}
        """)
    
    def load_conversations(self):
        """加载对话列表"""
        self.history_list.clear()
        conversations = self.history_manager.load_conversations()
        
        for conv in conversations:
            updated_time = datetime.fromisoformat(conv["updated_at"])
            self.history_list.add_conversation(
                conv["id"], 
                conv["title"], 
                updated_time
            )
        
        self.update_stats()
    
    def start_new_chat(self):
        """开始新对话"""
        self.current_conv_id = None
        self.chat_display.clear_messages()
        self.chat_title.setText("New Conversation")
        self.message_input.setFocus()
        self.update_status("Started new conversation")
    
    def load_conversation(self, conv_id: str):
        """加载指定对话"""
        self.current_conv_id = conv_id
        messages = self.history_manager.load_conversation_messages(conv_id)
        
        # 清空当前显示
        self.chat_display.clear_messages()
        
        # 加载消息
        for msg in messages:
            if msg["role"] == "user":
                self.chat_display.add_message(msg["content"], "You", is_user=True)
            elif msg["role"] == "assistant":
                self.chat_display.add_message(msg["content"], "AI", is_user=False)
        
        # 更新标题
        conversations = self.history_manager.load_conversations()
        for conv in conversations:
            if conv["id"] == conv_id:
                self.chat_title.setText(conv["title"])
                break
        
        self.message_input.setFocus()
        self.update_status(f"Loaded conversation: {conv_id}")
    
    def send_message(self):
        """发送消息"""
        if self.is_generating:
            return
        
        message = self.message_input.text().strip()
        if not message:
            return
        
        # 显示用户消息
        self.chat_display.add_message(message, "You", is_user=True)
        self.message_input.clear()
        
        # 准备消息历史
        messages = []
        if self.current_conv_id:
            messages = self.history_manager.load_conversation_messages(self.current_conv_id)
        else:
            messages = [{"role": "system", "content": "You are a helpful assistant."}]
            self.current_conv_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # 添加用户消息
        messages.append({"role": "user", "content": message})
        
        # 开始生成
        self.is_generating = True
        self.send_btn.setEnabled(False)
        self.typing_indicator.start_animation()
        self.update_status("AI is thinking...")
        
        # 调用AI
        self.ai_provider.generate_response(messages)
    
    def on_ai_stream_chunk(self, chunk: str):
        """处理AI流式响应"""
        # 这里需要实现流式显示
        pass
    
    def on_ai_response(self, response: str):
        """处理AI响应完成"""
        self.typing_indicator.stop_animation()
        self.chat_display.add_message(response, "AI", is_user=False)
        
        # 保存对话
        messages = self.history_manager.load_conversation_messages(self.current_conv_id) if self.current_conv_id else []
        messages.append({"role": "assistant", "content": response})
        
        title = self.history_manager.generate_title(messages)
        is_new = len(messages) <= 3
        
        self.history_manager.save_conversation(
            self.current_conv_id, title, messages, is_new
        )
        
        if is_new:
            self.load_conversations()  # 刷新列表
            self.chat_title.setText(title)
        
        self.is_generating = False
        self.send_btn.setEnabled(True)
        self.message_input.setFocus()
        self.update_status("Response complete")
    
    def on_ai_error(self, error: str):
        """处理AI错误"""
        self.typing_indicator.stop_animation()
        self.chat_display.add_message(f"Error: {error}", "System", is_user=False)
        self.is_generating = False
        self.send_btn.setEnabled(True)
        self.update_status(f"Error: {error}")
    
    def clear_chat(self):
        """清空聊天"""
        reply = QMessageBox.question(
            self, "Clear Chat", 
            "Are you sure you want to clear the current chat?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.start_new_chat()
    
    def export_conversation(self):
        """导出对话"""
        if not self.current_conv_id:
            QMessageBox.information(self, "Export", "No conversation to export.")
            return
        
        # 获取保存路径
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Conversation", 
            f"conversation_{self.current_conv_id}.md",
            "Markdown (*.md);;Text (*.txt);;HTML (*.html);;JSON (*.json)"
        )
        
        if filename:
            messages = self.history_manager.load_conversation_messages(self.current_conv_id)
            
            # 确定格式
            if filename.endswith('.md'):
                format_type = 'md'
            elif filename.endswith('.html'):
                format_type = 'html'
            elif filename.endswith('.json'):
                format_type = 'json'
            else:
                format_type = 'txt'
            
            success = conversation_exporter.export_conversation(messages, format_type, filename)
            
            if success:
                QMessageBox.information(self, "Export", "Conversation exported successfully!")
                self.update_status(f"Exported to {filename}")
            else:
                QMessageBox.warning(self, "Export", "Failed to export conversation.")
    
    def toggle_sidebar(self):
        """切换侧边栏显示"""
        self.sidebar_visible = not self.sidebar_visible
        if self.sidebar_visible:
            self.sidebar.show()
        else:
            self.sidebar.hide()
    
    def on_search_changed(self, text: str):
        """搜索变化处理"""
        if text:
            # 搜索对话
            results = search_manager.search_conversations(text, self.history_manager.load_conversations())
            self.history_list.clear()
            
            for conv in results:
                updated_time = datetime.fromisoformat(conv["updated_at"])
                self.history_list.add_conversation(conv["id"], conv["title"], updated_time)
        else:
            # 重新加载所有对话
            self.load_conversations()
    
    def focus_search(self):
        """聚焦搜索框"""
        self.search_input.setFocus()
        self.search_input.selectAll()
    
    def update_stats(self):
        """更新统计信息"""
        if self.stats_status is None:
            return  # 如果尚未初始化，则跳过
        stats = self.history_manager.get_statistics()
        
        stats_text = f"{stats['total_conversations']} conversations"
        self.stats_label.setText(stats_text)
        
        status_text = f"Conversations: {stats['total_conversations']} | Messages: {stats['total_messages']}"
        self.stats_status.setText(status_text)
    
    def update_status(self, message: str):
        """更新状态栏"""
        self.status_label.setText(message)
        
        # 3秒后清空状态
        QTimer.singleShot(3000, lambda: self.status_label.setText("Ready"))
    
    def open_settings(self):
        """打开设置对话框"""
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 重新应用主题
            self.apply_theme()
            self.update_status("Settings updated")
    
    def show_about(self):
        """显示关于对话框"""
        dialog = AboutDialog(self)
        dialog.exec()
    
    def show_welcome_message(self):
        """显示欢迎消息"""
        if not self.current_conv_id:
            welcome_msg = """Welcome to Teresa V2! 👋

I'm your AI assistant, ready to help with:
• Answering questions
• Writing and editing
• Code assistance
• Creative tasks
• General conversation

Start by typing a message below or use Ctrl+N for a new chat."""
            
            self.chat_display.add_message(welcome_msg, "Teresa", is_user=False)
    
    def show_notification(self, title: str, message: str):
        """显示通知"""
        if hasattr(self, 'tray_icon'):
            self.tray_icon.showMessage(title, message)
    
    def closeEvent(self, event):
        """关闭事件处理"""
        if config.behavior.auto_save:
            # 保存当前状态
            pass
        
        event.accept()
