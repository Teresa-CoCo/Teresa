"""
Teresa V2 现代化UI组件库
包含自定义的聊天气泡、按钮、输入框等组件
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, 
    QPushButton, QLabel, QScrollArea, QFrame, QGraphicsDropShadowEffect,
    QListWidget, QListWidgetItem, QApplication, QTextBrowser, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal, QRect
from PyQt6.QtGui import (
    QPainter, QPalette, QFont, QFontMetrics, QPixmap, QIcon, 
    QTextOption, QTextDocument, QSyntaxHighlighter, QTextCharFormat, QBrush
)
import re
from datetime import datetime
from config import config

class ModernButton(QPushButton):
    """现代化按钮组件"""
    def __init__(self, text="", icon=None, style="primary"):
        super().__init__(text)
        self.style_type = style
        self.setup_style()
        
        if icon:
            self.setIcon(icon)
    
    def setup_style(self):
        colors = config.get_theme_colors()
        
        if self.style_type == "primary":
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {colors['accent']};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: {config.appearance.font_size}px;
                    font-weight: 500;
                    min-height: 20px;
                }}
                QPushButton:hover {{
                    background: {self._darken_color(colors['accent'], 10)};
                }}
                QPushButton:pressed {{
                    background: {self._darken_color(colors['accent'], 20)};
                }}
                QPushButton:disabled {{
                    background: {colors['border']};
                    color: {colors['text_muted']};
                }}
            """)
        elif self.style_type == "secondary":
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {colors['text_primary']};
                    border: 1px solid {colors['border']};
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: {config.appearance.font_size}px;
                }}
                QPushButton:hover {{
                    background: {colors['bg_tertiary']};
                }}
                QPushButton:pressed {{
                    background: {colors['border']};
                }}
            """)
    
    def _darken_color(self, color, percent):
        """使颜色变暗"""
        # 简单的颜色调暗实现
        return color  # 暂时返回原色

class ChatBubble(QFrame):
    """聊天气泡组件"""
    def __init__(self, message, sender, timestamp=None, is_user=True):
        super().__init__()
        self.message = message
        self.sender = sender
        self.timestamp = timestamp or datetime.now()
        self.is_user = is_user
        
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 消息内容
        self.content_widget = ChatMessageContent(self.message, self.is_user)
        layout.addWidget(self.content_widget)
        
        # 时间戳（可选）
        if config.appearance.show_timestamps:
            time_label = QLabel(self.timestamp.strftime("%H:%M"))
            time_label.setAlignment(Qt.AlignmentFlag.AlignRight if self.is_user else Qt.AlignmentFlag.AlignLeft)
            time_label.setStyleSheet(f"color: {config.get_theme_colors()['text_muted']}; font-size: 10px;")
            layout.addWidget(time_label)
        
        self.setLayout(layout)
    
    def setup_style(self):
        colors = config.get_theme_colors()
        
        if self.is_user:
            bg_color = colors['user_bubble']
            text_color = "white"
            alignment = "margin-left: 50px; margin-right: 10px;"
        else:
            bg_color = colors['ai_bubble']
            text_color = colors['text_primary']
            alignment = "margin-right: 50px; margin-left: 10px;"
        
        self.setStyleSheet(f"""
            QFrame {{
                background: {bg_color};
                border-radius: 12px;
                {alignment}
                margin-top: 5px;
                margin-bottom: 5px;
                padding: 0px;
            }}
        """)

class ChatMessageContent(QTextBrowser):
    """聊天消息内容组件，支持Markdown和代码高亮"""
    def __init__(self, message, is_user=True):
        super().__init__()
        self.is_user = is_user
        self.setOpenExternalLinks(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # 设置文本内容
        self.setMarkdown(message)
        
        # 调整大小
        self.document().setTextWidth(self.width())
        self.setFixedHeight(int(self.document().size().height() + 20))
        
        self.setup_style()
    
    def setup_style(self):
        colors = config.get_theme_colors()
        text_color = "white" if self.is_user else colors['text_primary']
        
        self.setStyleSheet(f"""
            QTextBrowser {{
                background: transparent;
                border: none;
                color: {text_color};
                font-size: {config.appearance.chat_font_size}px;
                font-family: {config.appearance.font_family};
                padding: 12px;
            }}
        """)

class ModernLineEdit(QLineEdit):
    """现代化输入框"""
    def __init__(self, placeholder=""):
        super().__init__()
        if placeholder:
            self.setPlaceholderText(placeholder)
        self.setup_style()
    
    def setup_style(self):
        colors = config.get_theme_colors()
        
        self.setStyleSheet(f"""
            QLineEdit {{
                background: {colors['bg_secondary']};
                border: 2px solid {colors['border']};
                border-radius: 8px;
                padding: 12px 16px;
                font-size: {config.appearance.font_size}px;
                color: {colors['text_primary']};
            }}
            QLineEdit:focus {{
                border-color: {colors['accent']};
                background: {colors['bg_primary']};
            }}
        """)

class ModernTextEdit(QTextEdit):
    """现代化多行输入框"""
    def __init__(self):
        super().__init__()
        self.setup_style()
    
    def setup_style(self):
        colors = config.get_theme_colors()
        
        self.setStyleSheet(f"""
            QTextEdit {{
                background: {colors['bg_secondary']};
                border: 2px solid {colors['border']};
                border-radius: 8px;
                padding: 12px;
                font-size: {config.appearance.font_size}px;
                color: {colors['text_primary']};
            }}
            QTextEdit:focus {{
                border-color: {colors['accent']};
                background: {colors['bg_primary']};
            }}
        """)

class ChatScrollArea(QScrollArea):
    """聊天滚动区域"""
    def __init__(self):
        super().__init__()
        self.setup_style()
        
        # 内容widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(0)
        self.content_layout.addStretch()  # 推到底部
        self.content_widget.setLayout(self.content_layout)
        
        self.setWidget(self.content_widget)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    
    def add_message(self, message, sender, is_user=True):
        """添加消息"""
        bubble = ChatBubble(message, sender, is_user=is_user)
        
        # 在stretch之前插入
        self.content_layout.insertWidget(self.content_layout.count() - 1, bubble)
        
        # 滚动到底部
        QTimer.singleShot(10, self.scroll_to_bottom)
    
    def scroll_to_bottom(self):
        """滚动到底部"""
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_messages(self):
        """清空所有消息"""
        while self.content_layout.count() > 1:  # 保留stretch
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def setup_style(self):
        colors = config.get_theme_colors()
        
        self.setStyleSheet(f"""
            QScrollArea {{
                background: {colors['bg_primary']};
                border: none;
                border-radius: 8px;
            }}
            QScrollBar:vertical {{
                background: {colors['bg_secondary']};
                width: 8px;
                border-radius: 4px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {colors['border']};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {colors['text_muted']};
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
        """)

class SidebarHistoryList(QListWidget):
    """侧边栏历史列表"""
    itemSelected = pyqtSignal(str)  # 选中项信号
    
    def __init__(self):
        super().__init__()
        self.setup_style()
        
        # 连接信号
        self.itemClicked.connect(self._on_item_clicked)
    
    def _on_item_clicked(self, item):
        """处理项目点击"""
        if hasattr(item, 'conversation_id'):
            self.itemSelected.emit(item.conversation_id)
    
    def add_conversation(self, conv_id, title, timestamp):
        """添加对话项"""
        item = QListWidgetItem()
        item.conversation_id = conv_id
        
        # 创建自定义widget
        widget = ConversationItem(title, timestamp)
        item.setSizeHint(widget.sizeHint())
        
        self.addItem(item)
        self.setItemWidget(item, widget)
    
    def setup_style(self):
        colors = config.get_theme_colors()
        
        self.setStyleSheet(f"""
            QListWidget {{
                background: {colors['bg_secondary']};
                border: none;
                border-radius: 8px;
                outline: none;
            }}
            QListWidget::item {{
                background: transparent;
                border: none;
                padding: 0px;
                margin: 2px;
            }}
            QListWidget::item:selected {{
                background: {colors['accent']};
                border-radius: 6px;
            }}
            QListWidget::item:hover {{
                background: {colors['bg_tertiary']};
                border-radius: 6px;
            }}
        """)

class ConversationItem(QWidget):
    """对话项组件"""
    def __init__(self, title, timestamp):
        super().__init__()
        self.title = title
        self.timestamp = timestamp
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(2)
        
        # 标题
        title_label = QLabel(self.title)
        title_label.setWordWrap(True)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {config.get_theme_colors()['text_primary']};
                font-size: {config.appearance.font_size}px;
                font-weight: 500;
            }}
        """)
        
        # 时间
        time_label = QLabel(self.timestamp.strftime("%m/%d %H:%M"))
        time_label.setStyleSheet(f"""
            QLabel {{
                color: {config.get_theme_colors()['text_muted']};
                font-size: {config.appearance.font_size - 2}px;
            }}
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(time_label)
        self.setLayout(layout)

class TypingIndicator(QWidget):
    """打字指示器动画"""
    def __init__(self):
        super().__init__()
        self.setFixedHeight(30)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.dots = 0
        
    def start_animation(self):
        """开始动画"""
        self.timer.start(500)
        self.show()
    
    def stop_animation(self):
        """停止动画"""
        self.timer.stop()
        self.hide()
    
    def paintEvent(self, event):
        """绘制动画"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        colors = config.get_theme_colors()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(Qt.GlobalColor.gray))
        
        # 绘制三个点
        for i in range(3):
            opacity = 1.0 if i <= self.dots else 0.3
            painter.setOpacity(opacity)
            painter.drawEllipse(10 + i * 15, 10, 8, 8)
        
        self.dots = (self.dots + 1) % 3
