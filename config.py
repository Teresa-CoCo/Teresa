"""
Teresa V2 配置管理模块
支持主题、API设置、快捷键等配置
"""
import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from PyQt6.QtCore import QSettings

@dataclass
class AppearanceConfig:
    theme: str = "dark"  # dark, light, auto
    font_family: str = "Segoe UI"
    font_size: int = 11
    chat_font_size: int = 13
    enable_animations: bool = True
    enable_blur_effects: bool = True
    accent_color: str = "#0078D4"
    chat_bubble_style: bool = True
    show_timestamps: bool = True
    show_word_count: bool = False

@dataclass
class BehaviorConfig:
    auto_save: bool = True
    save_interval: int = 30  # seconds
    max_history_items: int = 1000
    enable_notifications: bool = True
    enable_sound: bool = False
    auto_scroll: bool = True
    typing_indicator: bool = True
    smart_suggestions: bool = True
    auto_complete: bool = True

@dataclass
class APIConfig:
    provider: str = "deepseek"  # deepseek, openai, claude, local
    api_key: str = ""
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: int = 4000
    stream: bool = True
    timeout: int = 30

@dataclass
class ShortcutsConfig:
    send_message: str = "Ctrl+Return"
    new_chat: str = "Ctrl+N"
    clear_chat: str = "Ctrl+Shift+C"
    toggle_sidebar: str = "Ctrl+B"
    search_history: str = "Ctrl+F"
    export_chat: str = "Ctrl+E"
    settings: str = "Ctrl+,"

class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.join(os.path.expanduser("~"), ".teresa")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.settings = QSettings("Teresa", "TeresaV2")
        
        # 确保配置目录存在
        os.makedirs(self.config_dir, exist_ok=True)
        
        # 初始化默认配置
        self.appearance = AppearanceConfig()
        self.behavior = BehaviorConfig()
        self.api = APIConfig()
        self.shortcuts = ShortcutsConfig()
        
        # 加载现有配置
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 更新配置对象
                if "appearance" in data:
                    self.appearance = AppearanceConfig(**data["appearance"])
                if "behavior" in data:
                    self.behavior = BehaviorConfig(**data["behavior"])
                if "api" in data:
                    self.api = APIConfig(**data["api"])
                if "shortcuts" in data:
                    self.shortcuts = ShortcutsConfig(**data["shortcuts"])
        except Exception as e:
            print(f"加载配置失败: {e}")
            self.save_config()  # 保存默认配置
    
    def save_config(self):
        """保存配置到文件"""
        try:
            config_data = {
                "appearance": asdict(self.appearance),
                "behavior": asdict(self.behavior),
                "api": asdict(self.api),
                "shortcuts": asdict(self.shortcuts)
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def get_theme_colors(self) -> Dict[str, str]:
        """获取主题颜色配置"""
        if self.appearance.theme == "dark":
            return {
                "bg_primary": "#1e1e1e",
                "bg_secondary": "#2d2d30",
                "bg_tertiary": "#3e3e42",
                "text_primary": "#ffffff",
                "text_secondary": "#cccccc",
                "text_muted": "#969696",
                "accent": self.appearance.accent_color,
                "border": "#484848",
                "user_bubble": "#0078D4",
                "ai_bubble": "#2d2d30",
                "error": "#f44336",
                "success": "#4caf50",
                "warning": "#ff9800"
            }
        else:  # light theme
            return {
                "bg_primary": "#ffffff",
                "bg_secondary": "#f5f5f5",
                "bg_tertiary": "#e0e0e0",
                "text_primary": "#000000",
                "text_secondary": "#333333",
                "text_muted": "#666666",
                "accent": self.appearance.accent_color,
                "border": "#d0d0d0",
                "user_bubble": "#0078D4",
                "ai_bubble": "#f0f0f0",
                "error": "#f44336",
                "success": "#4caf50",
                "warning": "#ff9800"
            }
    
    def reset_to_defaults(self):
        """重置为默认配置"""
        self.appearance = AppearanceConfig()
        self.behavior = BehaviorConfig()
        self.api = APIConfig()
        self.shortcuts = ShortcutsConfig()
        self.save_config()

# 全局配置实例
config = ConfigManager()
