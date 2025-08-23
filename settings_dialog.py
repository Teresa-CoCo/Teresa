"""
Teresa V2 设置对话框
提供完整的配置界面
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QSpinBox, QCheckBox, QComboBox,
    QPushButton, QGroupBox, QSlider, QColorDialog, QFormLayout,
    QDialogButtonBox, QFileDialog, QMessageBox, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from config import config

class SettingsDialog(QDialog):
    """设置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.resize(600, 500)
        
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # 外观标签页
        self.setup_appearance_tab()
        
        # 行为标签页
        self.setup_behavior_tab()
        
        # API标签页
        self.setup_api_tab()
        
        # 快捷键标签页
        self.setup_shortcuts_tab()
        
        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.RestoreDefaults
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(self.restore_defaults)
        
        layout.addWidget(button_box)
    
    def setup_appearance_tab(self):
        """设置外观标签页"""
        widget = QWidget()
        layout = QFormLayout()
        widget.setLayout(layout)
        
        # 主题
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Auto"])
        layout.addRow("Theme:", self.theme_combo)
        
        # 字体
        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems([
            "Segoe UI", "Arial", "Consolas", "Courier New", "Times New Roman"
        ])
        layout.addRow("Font Family:", self.font_family_combo)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 20)
        layout.addRow("Font Size:", self.font_size_spin)
        
        self.chat_font_size_spin = QSpinBox()
        self.chat_font_size_spin.setRange(10, 24)
        layout.addRow("Chat Font Size:", self.chat_font_size_spin)
        
        # 动画效果
        self.animations_check = QCheckBox("Enable animations")
        layout.addRow(self.animations_check)
        
        self.blur_effects_check = QCheckBox("Enable blur effects")
        layout.addRow(self.blur_effects_check)
        
        # 聊天样式
        self.chat_bubbles_check = QCheckBox("Use chat bubble style")
        layout.addRow(self.chat_bubbles_check)
        
        self.timestamps_check = QCheckBox("Show timestamps")
        layout.addRow(self.timestamps_check)
        
        self.word_count_check = QCheckBox("Show word count")
        layout.addRow(self.word_count_check)
        
        # 强调色
        accent_layout = QHBoxLayout()
        self.accent_color_btn = QPushButton()
        self.accent_color_btn.setFixedSize(30, 30)
        self.accent_color_btn.clicked.connect(self.choose_accent_color)
        accent_layout.addWidget(self.accent_color_btn)
        accent_layout.addWidget(QLabel("Accent Color"))
        accent_layout.addStretch()
        layout.addRow(accent_layout)
        
        self.tab_widget.addTab(widget, "Appearance")
    
    def setup_behavior_tab(self):
        """设置行为标签页"""
        widget = QWidget()
        layout = QFormLayout()
        widget.setLayout(layout)
        
        # 自动保存
        self.auto_save_check = QCheckBox("Auto save conversations")
        layout.addRow(self.auto_save_check)
        
        self.save_interval_spin = QSpinBox()
        self.save_interval_spin.setRange(10, 300)
        self.save_interval_spin.setSuffix(" seconds")
        layout.addRow("Save Interval:", self.save_interval_spin)
        
        # 历史记录
        self.max_history_spin = QSpinBox()
        self.max_history_spin.setRange(100, 10000)
        layout.addRow("Max History Items:", self.max_history_spin)
        
        # 通知
        self.notifications_check = QCheckBox("Enable notifications")
        layout.addRow(self.notifications_check)
        
        self.sound_check = QCheckBox("Enable sound")
        layout.addRow(self.sound_check)
        
        # 聊天行为
        self.auto_scroll_check = QCheckBox("Auto scroll to new messages")
        layout.addRow(self.auto_scroll_check)
        
        self.typing_indicator_check = QCheckBox("Show typing indicator")
        layout.addRow(self.typing_indicator_check)
        
        self.smart_suggestions_check = QCheckBox("Enable smart suggestions")
        layout.addRow(self.smart_suggestions_check)
        
        self.auto_complete_check = QCheckBox("Enable auto complete")
        layout.addRow(self.auto_complete_check)
        
        self.tab_widget.addTab(widget, "Behavior")
    
    def setup_api_tab(self):
        """设置API标签页"""
        widget = QWidget()
        layout = QFormLayout()
        widget.setLayout(layout)
        
        # API提供商
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["DeepSeek", "OpenAI", "Claude", "Local"])
        layout.addRow("Provider:", self.provider_combo)
        
        # API密钥
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("API Key:", self.api_key_edit)
        
        # 基础URL
        self.base_url_edit = QLineEdit()
        layout.addRow("Base URL:", self.base_url_edit)
        
        # 模型
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        self.model_combo.addItems([
            "deepseek-chat", "gpt-3.5-turbo", "gpt-4", "claude-3-sonnet"
        ])
        layout.addRow("Model:", self.model_combo)
        
        # 温度
        temp_layout = QHBoxLayout()
        self.temperature_slider = QSlider(Qt.Orientation.Horizontal)
        self.temperature_slider.setRange(0, 100)
        self.temperature_label = QLabel("0.7")
        temp_layout.addWidget(self.temperature_slider)
        temp_layout.addWidget(self.temperature_label)
        layout.addRow("Temperature:", temp_layout)
        
        self.temperature_slider.valueChanged.connect(
            lambda v: self.temperature_label.setText(f"{v/100:.2f}")
        )
        
        # 最大令牌数
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(100, 8000)
        layout.addRow("Max Tokens:", self.max_tokens_spin)
        
        # 流式响应
        self.stream_check = QCheckBox("Enable streaming")
        layout.addRow(self.stream_check)
        
        # 超时
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(10, 120)
        self.timeout_spin.setSuffix(" seconds")
        layout.addRow("Timeout:", self.timeout_spin)
        
        self.tab_widget.addTab(widget, "API")
    
    def setup_shortcuts_tab(self):
        """设置快捷键标签页"""
        widget = QWidget()
        layout = QFormLayout()
        widget.setLayout(layout)
        
        # 创建快捷键输入框
        self.send_message_edit = QLineEdit()
        layout.addRow("Send Message:", self.send_message_edit)
        
        self.new_chat_edit = QLineEdit()
        layout.addRow("New Chat:", self.new_chat_edit)
        
        self.clear_chat_edit = QLineEdit()
        layout.addRow("Clear Chat:", self.clear_chat_edit)
        
        self.toggle_sidebar_edit = QLineEdit()
        layout.addRow("Toggle Sidebar:", self.toggle_sidebar_edit)
        
        self.search_history_edit = QLineEdit()
        layout.addRow("Search History:", self.search_history_edit)
        
        self.export_chat_edit = QLineEdit()
        layout.addRow("Export Chat:", self.export_chat_edit)
        
        self.settings_edit = QLineEdit()
        layout.addRow("Settings:", self.settings_edit)
        
        self.tab_widget.addTab(widget, "Shortcuts")
    
    def load_settings(self):
        """加载当前设置"""
        # 外观设置
        appearance = config.appearance
        
        theme_map = {"dark": 0, "light": 1, "auto": 2}
        self.theme_combo.setCurrentIndex(theme_map.get(appearance.theme, 0))
        
        self.font_family_combo.setCurrentText(appearance.font_family)
        self.font_size_spin.setValue(appearance.font_size)
        self.chat_font_size_spin.setValue(appearance.chat_font_size)
        self.animations_check.setChecked(appearance.enable_animations)
        self.blur_effects_check.setChecked(appearance.enable_blur_effects)
        self.chat_bubbles_check.setChecked(appearance.chat_bubble_style)
        self.timestamps_check.setChecked(appearance.show_timestamps)
        self.word_count_check.setChecked(appearance.show_word_count)
        
        # 设置强调色按钮颜色
        self.update_accent_color_button(appearance.accent_color)
        
        # 行为设置
        behavior = config.behavior
        self.auto_save_check.setChecked(behavior.auto_save)
        self.save_interval_spin.setValue(behavior.save_interval)
        self.max_history_spin.setValue(behavior.max_history_items)
        self.notifications_check.setChecked(behavior.enable_notifications)
        self.sound_check.setChecked(behavior.enable_sound)
        self.auto_scroll_check.setChecked(behavior.auto_scroll)
        self.typing_indicator_check.setChecked(behavior.typing_indicator)
        self.smart_suggestions_check.setChecked(behavior.smart_suggestions)
        self.auto_complete_check.setChecked(behavior.auto_complete)
        
        # API设置
        api = config.api
        provider_map = {"deepseek": 0, "openai": 1, "claude": 2, "local": 3}
        self.provider_combo.setCurrentIndex(provider_map.get(api.provider, 0))
        
        self.api_key_edit.setText(api.api_key)
        self.base_url_edit.setText(api.base_url)
        self.model_combo.setCurrentText(api.model)
        self.temperature_slider.setValue(int(api.temperature * 100))
        self.max_tokens_spin.setValue(api.max_tokens)
        self.stream_check.setChecked(api.stream)
        self.timeout_spin.setValue(api.timeout)
        
        # 快捷键设置
        shortcuts = config.shortcuts
        self.send_message_edit.setText(shortcuts.send_message)
        self.new_chat_edit.setText(shortcuts.new_chat)
        self.clear_chat_edit.setText(shortcuts.clear_chat)
        self.toggle_sidebar_edit.setText(shortcuts.toggle_sidebar)
        self.search_history_edit.setText(shortcuts.search_history)
        self.export_chat_edit.setText(shortcuts.export_chat)
        self.settings_edit.setText(shortcuts.settings)
    
    def save_settings(self):
        """保存设置"""
        # 保存外观设置
        theme_map = {0: "dark", 1: "light", 2: "auto"}
        config.appearance.theme = theme_map[self.theme_combo.currentIndex()]
        config.appearance.font_family = self.font_family_combo.currentText()
        config.appearance.font_size = self.font_size_spin.value()
        config.appearance.chat_font_size = self.chat_font_size_spin.value()
        config.appearance.enable_animations = self.animations_check.isChecked()
        config.appearance.enable_blur_effects = self.blur_effects_check.isChecked()
        config.appearance.chat_bubble_style = self.chat_bubbles_check.isChecked()
        config.appearance.show_timestamps = self.timestamps_check.isChecked()
        config.appearance.show_word_count = self.word_count_check.isChecked()
        
        # 保存行为设置
        config.behavior.auto_save = self.auto_save_check.isChecked()
        config.behavior.save_interval = self.save_interval_spin.value()
        config.behavior.max_history_items = self.max_history_spin.value()
        config.behavior.enable_notifications = self.notifications_check.isChecked()
        config.behavior.enable_sound = self.sound_check.isChecked()
        config.behavior.auto_scroll = self.auto_scroll_check.isChecked()
        config.behavior.typing_indicator = self.typing_indicator_check.isChecked()
        config.behavior.smart_suggestions = self.smart_suggestions_check.isChecked()
        config.behavior.auto_complete = self.auto_complete_check.isChecked()
        
        # 保存API设置
        provider_map = {0: "deepseek", 1: "openai", 2: "claude", 3: "local"}
        config.api.provider = provider_map[self.provider_combo.currentIndex()]
        config.api.api_key = self.api_key_edit.text()
        config.api.base_url = self.base_url_edit.text()
        config.api.model = self.model_combo.currentText()
        config.api.temperature = self.temperature_slider.value() / 100.0
        config.api.max_tokens = self.max_tokens_spin.value()
        config.api.stream = self.stream_check.isChecked()
        config.api.timeout = self.timeout_spin.value()
        
        # 保存快捷键设置
        config.shortcuts.send_message = self.send_message_edit.text()
        config.shortcuts.new_chat = self.new_chat_edit.text()
        config.shortcuts.clear_chat = self.clear_chat_edit.text()
        config.shortcuts.toggle_sidebar = self.toggle_sidebar_edit.text()
        config.shortcuts.search_history = self.search_history_edit.text()
        config.shortcuts.export_chat = self.export_chat_edit.text()
        config.shortcuts.settings = self.settings_edit.text()
        
        # 保存到文件
        config.save_config()
    
    def choose_accent_color(self):
        """选择强调色"""
        color = QColorDialog.getColor(QColor(config.appearance.accent_color), self)
        if color.isValid():
            config.appearance.accent_color = color.name()
            self.update_accent_color_button(color.name())
    
    def update_accent_color_button(self, color_name):
        """更新强调色按钮显示"""
        self.accent_color_btn.setStyleSheet(f"""
            QPushButton {{
                background: {color_name};
                border: 2px solid #ccc;
                border-radius: 4px;
            }}
        """)
    
    def restore_defaults(self):
        """恢复默认设置"""
        reply = QMessageBox.question(
            self, "Restore Defaults",
            "Are you sure you want to restore all settings to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            config.reset_to_defaults()
            self.load_settings()
    
    def accept(self):
        """确认并保存"""
        self.save_settings()
        super().accept()
