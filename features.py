"""
Teresa V2 高级功能模块
包含插件系统、快捷操作、智能建议等
"""
import os
import json
import re
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal, QThread, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMenu
from PyQt6.QtGui import QShortcut, QKeySequence, QAction
import hashlib

class SmartSuggestions:
    """智能建议系统"""
    
    def __init__(self):
        self.suggestions_db = []
        self.load_suggestions()
    
    def load_suggestions(self):
        """加载建议数据库"""
        suggestions_file = "data/suggestions.json"
        if os.path.exists(suggestions_file):
            try:
                with open(suggestions_file, 'r', encoding='utf-8') as f:
                    self.suggestions_db = json.load(f)
            except:
                self.suggestions_db = []
        
        # 默认建议
        if not self.suggestions_db:
            self.suggestions_db = [
                {"trigger": "翻译", "suggestion": "请帮我翻译以下内容："},
                {"trigger": "解释", "suggestion": "请详细解释一下："},
                {"trigger": "总结", "suggestion": "请帮我总结以下内容："},
                {"trigger": "代码", "suggestion": "请帮我写一段代码："},
                {"trigger": "优化", "suggestion": "请帮我优化以下内容："},
                {"trigger": "分析", "suggestion": "请帮我分析一下："},
                {"trigger": "比较", "suggestion": "请帮我比较："},
                {"trigger": "推荐", "suggestion": "请推荐一些："},
            ]
    
    def get_suggestions(self, input_text: str) -> List[str]:
        """获取智能建议"""
        suggestions = []
        input_lower = input_text.lower()
        
        for item in self.suggestions_db:
            if item["trigger"].lower() in input_lower:
                suggestions.append(item["suggestion"])
        
        return suggestions[:5]  # 最多返回5个建议

class QuickActions:
    """快捷操作系统"""
    
    def __init__(self):
        self.actions = {
            "新建对话": self.new_chat,
            "导出对话": self.export_chat,
            "清空历史": self.clear_history,
            "切换主题": self.toggle_theme,
            "设置": self.open_settings,
            "关于": self.show_about,
        }
    
    def new_chat(self):
        """新建对话"""
        pass
    
    def export_chat(self):
        """导出对话"""
        pass
    
    def clear_history(self):
        """清空历史"""
        pass
    
    def toggle_theme(self):
        """切换主题"""
        pass
    
    def open_settings(self):
        """打开设置"""
        pass
    
    def show_about(self):
        """显示关于"""
        pass

class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self.plugins = {}
        self.plugins_dir = "plugins"
        os.makedirs(self.plugins_dir, exist_ok=True)
        self.load_plugins()
    
    def load_plugins(self):
        """加载插件"""
        # 这里可以实现动态插件加载
        pass
    
    def register_plugin(self, name: str, plugin_class):
        """注册插件"""
        self.plugins[name] = plugin_class

class ChatAnalyzer:
    """对话分析器"""
    
    def __init__(self):
        self.conversation_stats = {}
    
    def analyze_conversation(self, messages: List[Dict]) -> Dict[str, Any]:
        """分析对话内容"""
        stats = {
            "total_messages": len(messages),
            "user_messages": 0,
            "ai_messages": 0,
            "total_words": 0,
            "avg_message_length": 0,
            "topics": [],
            "sentiment": "neutral",
            "conversation_type": "general"
        }
        
        user_words = 0
        ai_words = 0
        
        for msg in messages:
            if msg["role"] == "user":
                stats["user_messages"] += 1
                words = len(msg["content"].split())
                user_words += words
                stats["total_words"] += words
            elif msg["role"] == "assistant":
                stats["ai_messages"] += 1
                words = len(msg["content"].split())
                ai_words += words
                stats["total_words"] += words
        
        if stats["total_messages"] > 0:
            stats["avg_message_length"] = stats["total_words"] / stats["total_messages"]
        
        # 分析主题
        stats["topics"] = self._extract_topics(messages)
        
        return stats
    
    def _extract_topics(self, messages: List[Dict]) -> List[str]:
        """提取对话主题"""
        # 简单的关键词提取
        keywords = []
        for msg in messages:
            if msg["role"] == "user":
                content = msg["content"].lower()
                # 这里可以实现更复杂的主题提取算法
                words = re.findall(r'\b\w+\b', content)
                keywords.extend(words)
        
        # 统计词频并返回前5个
        word_count = {}
        for word in keywords:
            if len(word) > 3:  # 只考虑长度大于3的词
                word_count[word] = word_count.get(word, 0) + 1
        
        return sorted(word_count.keys(), key=lambda x: word_count[x], reverse=True)[:5]

class ConversationExporter:
    """对话导出器"""
    
    def __init__(self):
        self.formats = ["txt", "md", "html", "json", "pdf"]
    
    def export_conversation(self, messages: List[Dict], format: str, filename: str) -> bool:
        """导出对话"""
        try:
            if format == "txt":
                return self._export_txt(messages, filename)
            elif format == "md":
                return self._export_markdown(messages, filename)
            elif format == "html":
                return self._export_html(messages, filename)
            elif format == "json":
                return self._export_json(messages, filename)
            elif format == "pdf":
                return self._export_pdf(messages, filename)
            return False
        except Exception as e:
            print(f"导出失败: {e}")
            return False
    
    def _export_txt(self, messages: List[Dict], filename: str) -> bool:
        """导出为TXT格式"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Teresa V2 对话导出\\n")
            f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
            
            for msg in messages:
                if msg["role"] == "user":
                    f.write(f"用户: {msg['content']}\\n\\n")
                elif msg["role"] == "assistant":
                    f.write(f"AI: {msg['content']}\\n\\n")
        return True
    
    def _export_markdown(self, messages: List[Dict], filename: str) -> bool:
        """导出为Markdown格式"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Teresa V2 对话导出\\n\\n")
            f.write(f"**导出时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
            
            for msg in messages:
                if msg["role"] == "user":
                    f.write(f"## 用户\\n\\n{msg['content']}\\n\\n")
                elif msg["role"] == "assistant":
                    f.write(f"## AI助手\\n\\n{msg['content']}\\n\\n")
        return True
    
    def _export_html(self, messages: List[Dict], filename: str) -> bool:
        """导出为HTML格式"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Teresa V2 对话导出</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .message {{ margin: 10px 0; padding: 15px; border-radius: 8px; }}
                .user {{ background: #e3f2fd; text-align: right; }}
                .assistant {{ background: #f5f5f5; }}
                .timestamp {{ color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <h1>Teresa V2 对话导出</h1>
            <p class="timestamp">导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        """
        
        for msg in messages:
            if msg["role"] == "user":
                html_content += f'<div class="message user"><strong>用户:</strong><br>{msg["content"]}</div>'
            elif msg["role"] == "assistant":
                html_content += f'<div class="message assistant"><strong>AI助手:</strong><br>{msg["content"]}</div>'
        
        html_content += "</body></html>"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return True
    
    def _export_json(self, messages: List[Dict], filename: str) -> bool:
        """导出为JSON格式"""
        export_data = {
            "export_time": datetime.now().isoformat(),
            "messages": messages
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        return True
    
    def _export_pdf(self, messages: List[Dict], filename: str) -> bool:
        """导出为PDF格式（需要额外依赖）"""
        # 这里需要安装 reportlab 或其他PDF库
        # 暂时返回False
        return False

class NotificationManager(QObject):
    """通知管理器"""
    
    notification_requested = pyqtSignal(str, str)  # title, message
    
    def __init__(self):
        super().__init__()
        self.enabled = True
    
    def show_notification(self, title: str, message: str):
        """显示通知"""
        if self.enabled:
            self.notification_requested.emit(title, message)
    
    def enable_notifications(self, enabled: bool):
        """启用/禁用通知"""
        self.enabled = enabled

class ShortcutManager:
    """快捷键管理器"""
    
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.shortcuts = {}
        self.setup_default_shortcuts()
    
    def setup_default_shortcuts(self):
        """设置默认快捷键"""
        from config import config
        shortcuts_config = config.shortcuts
        
        self.register_shortcut("send_message", shortcuts_config.send_message, None)
        self.register_shortcut("new_chat", shortcuts_config.new_chat, None)
        self.register_shortcut("clear_chat", shortcuts_config.clear_chat, None)
        self.register_shortcut("toggle_sidebar", shortcuts_config.toggle_sidebar, None)
        self.register_shortcut("search_history", shortcuts_config.search_history, None)
        self.register_shortcut("export_chat", shortcuts_config.export_chat, None)
        self.register_shortcut("settings", shortcuts_config.settings, None)
    
    def register_shortcut(self, name: str, key_sequence: str, callback: Callable):
        """注册快捷键"""
        if name in self.shortcuts:
            self.shortcuts[name].setEnabled(False)
        
        shortcut = QShortcut(QKeySequence(key_sequence), self.parent)
        if callback:
            shortcut.activated.connect(callback)
        
        self.shortcuts[name] = shortcut
    
    def update_shortcut(self, name: str, new_key_sequence: str):
        """更新快捷键"""
        if name in self.shortcuts:
            self.shortcuts[name].setKey(QKeySequence(new_key_sequence))

class SearchManager:
    """搜索管理器"""
    
    def __init__(self):
        self.search_history = []
        self.load_search_history()
    
    def search_conversations(self, query: str, conversations: List[Dict]) -> List[Dict]:
        """搜索对话"""
        if not query:
            return conversations
        
        query_lower = query.lower()
        results = []
        
        for conv in conversations:
            # 搜索标题
            if query_lower in conv["title"].lower():
                results.append(conv)
                continue
            
            # 搜索消息内容
            for msg in conv["messages"]:
                if query_lower in msg["content"].lower():
                    results.append(conv)
                    break
        
        # 记录搜索历史
        self.add_to_search_history(query)
        return results
    
    def add_to_search_history(self, query: str):
        """添加到搜索历史"""
        if query and query not in self.search_history:
            self.search_history.insert(0, query)
            self.search_history = self.search_history[:20]  # 保持最近20条
            self.save_search_history()
    
    def load_search_history(self):
        """加载搜索历史"""
        try:
            if os.path.exists("data/search_history.json"):
                with open("data/search_history.json", 'r', encoding='utf-8') as f:
                    self.search_history = json.load(f)
        except:
            self.search_history = []
    
    def save_search_history(self):
        """保存搜索历史"""
        os.makedirs("data", exist_ok=True)
        try:
            with open("data/search_history.json", 'w', encoding='utf-8') as f:
                json.dump(self.search_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存搜索历史失败: {e}")

# 全局实例
smart_suggestions = SmartSuggestions()
quick_actions = QuickActions()
plugin_manager = PluginManager()
chat_analyzer = ChatAnalyzer()
conversation_exporter = ConversationExporter()
notification_manager = NotificationManager()
search_manager = SearchManager()
