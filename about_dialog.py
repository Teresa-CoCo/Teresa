"""
Teresa V2 关于对话框
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextBrowser, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from config import config

class AboutDialog(QDialog):
    """关于对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Teresa V2")
        self.setModal(True)
        self.setFixedSize(500, 400)
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 顶部信息
        header_frame = QFrame()
        header_layout = QVBoxLayout()
        header_frame.setLayout(header_layout)
        
        # 应用图标和名称
        title_layout = QHBoxLayout()
        
        # 如果有图标文件
        # icon_label = QLabel()
        # icon_pixmap = QPixmap("assets/icon.png").scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
        # icon_label.setPixmap(icon_pixmap)
        # title_layout.addWidget(icon_label)
        
        title_info = QVBoxLayout()
        
        app_name = QLabel("Teresa V2")
        app_name.setFont(QFont(config.appearance.font_family, 18, QFont.Weight.Bold))
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        version_label = QLabel("Version 2.0.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("AI Chat Assistant")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {config.get_theme_colors()['text_muted']};")
        
        title_info.addWidget(app_name)
        title_info.addWidget(version_label)
        title_info.addWidget(subtitle)
        
        title_layout.addLayout(title_info)
        header_layout.addLayout(title_layout)
        
        layout.addWidget(header_frame)
        
        # 描述信息
        description = QTextBrowser()
        description.setMaximumHeight(200)
        description.setHtml(f"""
        <div style="color: {config.get_theme_colors()['text_primary']}; line-height: 1.6;">
            <p><b>Teresa V2</b> is a modern AI chat assistant built with Python and PyQt6.</p>
            
            <h3>Features:</h3>
            <ul>
                <li>🤖 Multiple AI provider support (DeepSeek, OpenAI, Claude)</li>
                <li>💾 Advanced conversation management with SQLite</li>
                <li>🎨 Modern, customizable UI with dark/light themes</li>
                <li>📁 Export conversations in multiple formats</li>
                <li>🔍 Smart search and conversation analysis</li>
                <li>⚡ Real-time streaming responses</li>
                <li>🔧 Extensive customization options</li>
                <li>📊 Conversation statistics and insights</li>
            </ul>
            
            <h3>Technologies Used:</h3>
            <ul>
                <li>Python 3.11+</li>
                <li>PyQt6 (GUI Framework)</li>
                <li>SQLite (Database)</li>
                <li>OpenAI API (AI Integration)</li>
            </ul>
        </div>
        """)
        
        layout.addWidget(description)
        
        # 版权信息
        copyright_frame = QFrame()
        copyright_layout = QVBoxLayout()
        copyright_frame.setLayout(copyright_layout)
        
        copyright_label = QLabel("© 2025 Teresa Development Team")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_label.setStyleSheet(f"color: {config.get_theme_colors()['text_muted']};")
        
        license_label = QLabel("Licensed under GPL v3")
        license_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        license_label.setStyleSheet(f"color: {config.get_theme_colors()['text_muted']};")
        
        copyright_layout.addWidget(copyright_label)
        copyright_layout.addWidget(license_label)
        
        layout.addWidget(copyright_frame)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        close_btn.setDefault(True)
        
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        # 应用样式
        self.apply_theme()
    
    def apply_theme(self):
        """应用主题"""
        colors = config.get_theme_colors()
        
        self.setStyleSheet(f"""
            QDialog {{
                background: {colors['bg_primary']};
                color: {colors['text_primary']};
            }}
            QFrame {{
                background: transparent;
            }}
            QTextBrowser {{
                background: {colors['bg_secondary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 10px;
            }}
            QPushButton {{
                background: {colors['accent']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: {config.appearance.font_size}px;
            }}
            QPushButton:hover {{
                background: {colors['accent']}dd;
            }}
            QPushButton:pressed {{
                background: {colors['accent']}aa;
            }}
        """)
