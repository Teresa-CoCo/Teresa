from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QLineEdit, QPushButton, QListWidget, QLabel, QSplitter, 
    QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QTextCursor
from TeresaV2_HistoryUI import HistoryManager
from openai import OpenAI
import os
import json
from datetime import datetime

class ChatWindow(QMainWindow):
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.history_manager = HistoryManager()
        self.current_conv_id = None
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        
        self.setWindowTitle("DeepSeek Chat")
        self.resize(1000, 700)
        
        self._setup_ui()
        self._load_conversations()
    
    def _setup_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        
        # 左侧历史面板
        self.history_panel = QWidget()
        history_layout = QVBoxLayout()
        self.history_panel.setLayout(history_layout)
        
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self._load_selected_conversation)
        history_layout.addWidget(QLabel("History"))
        history_layout.addWidget(self.history_list)
        
        new_chat_btn = QPushButton("New Chat")
        new_chat_btn.clicked.connect(self._start_new_chat)
        history_layout.addWidget(new_chat_btn)
        
        # 右侧聊天区域
        chat_panel = QWidget()
        chat_layout = QVBoxLayout()
        chat_panel.setLayout(chat_layout)
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        chat_layout.addWidget(self.chat_display)
        
        input_panel = QWidget()
        input_layout = QHBoxLayout()
        input_panel.setLayout(input_layout)
        
        self.message_input = QLineEdit()
        self.message_input.returnPressed.connect(self._send_message)
        input_layout.addWidget(self.message_input)
        
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self._send_message)
        input_layout.addWidget(send_btn)
        
        chat_layout.addWidget(input_panel)
        
        # 分割布局
        splitter = QSplitter()
        splitter.addWidget(self.history_panel)
        splitter.addWidget(chat_panel)
        splitter.setSizes([200, 800])
        
        main_layout.addWidget(splitter)
        self.setCentralWidget(main_widget)
    
    def _load_conversations(self):
        self.history_list.clear()
        conversations = self.history_manager.load_conversations()
        for conv in sorted(conversations, key=lambda x: x["updated_at"], reverse=True):
            date = datetime.fromisoformat(conv["updated_at"]).strftime("%m/%d %H:%M")
            self.history_list.addItem(f"{date} - {conv['title']}")
    
    def _start_new_chat(self):
        self.current_conv_id = None
        self.chat_display.clear()
        self.message_input.setFocus()
    
    def _load_selected_conversation(self):
        selected = self.history_list.currentRow()
        conversations = self.history_manager.load_conversations()
        
        if 0 <= selected < len(conversations):
            conv = sorted(conversations, key=lambda x: x["updated_at"], reverse=True)[selected]
            self.current_conv_id = conv["id"]
            self.chat_display.clear()
            
            for msg in conv["messages"]:
                if msg["role"] == "user":
                    self._append_message("You", msg["content"])
                elif msg["role"] == "assistant":
                    self._append_message("AI", msg["content"])
            
            self.message_input.setFocus()
    
    def _append_message(self, sender: str, message: str):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # 使用HTML换行标签 <br> 确保正确换行
        if sender == "You":
            cursor.insertHtml(
                f'<div style="color: blue; margin: 5px 0;">'
                f'<b>You:</b><br>{message.replace(chr(10), "<br>")}'
                f'</div>'
            )
        else:
            cursor.insertHtml(
                f'<div style="color: green; margin: 5px 0;">'
                f'<b>AI:</b><br>{message.replace(chr(10), "<br>")}'
                f'</div>'
            )
        
        cursor.insertHtml("<br>")  # 添加额外的换行
        self.chat_display.setTextCursor(cursor)
        self.chat_display.ensureCursorVisible()
    
    def _send_message(self):
        message = self.message_input.text().strip()
        if not message:
            return
        
        self._append_message("You", message)
        self.message_input.clear()
        
        # 准备消息历史
        messages = []
        
        # 如果是继续对话，加载历史
        if self.current_conv_id:
            conversations = self.history_manager.load_conversations()
            for conv in conversations:
                if conv["id"] == self.current_conv_id:
                    messages = conv["messages"]
                    break
        
        # 新对话初始化系统消息
        if not messages:
            messages = [{"role": "system", "content": "You are a helpful assistant."}]
            self.current_conv_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # 添加用户消息
        messages.append({"role": "user", "content": message})
        
        # 流式获取AI回复
        self._append_message("AI", "")
        ai_response = ""
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=True
            )
            
            cursor = self.chat_display.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.KeepAnchor)
            cursor.removeSelectedText()
            
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    ai_response += content
                    cursor.insertText(content)
                    self.chat_display.setTextCursor(cursor)
                    self.chat_display.ensureCursorVisible()
                    QApplication.processEvents()  # 保持UI响应
            
            # 保存完整对话
            messages.append({"role": "assistant", "content": ai_response})
            title = self.history_manager.generate_title(messages)
            is_new = len(messages) <= 3  # system + user + assistant
            
            self.history_manager.save_conversation(
                self.current_conv_id,
                title,
                messages,
                is_new
            )
            
            # 刷新历史列表
            self._load_conversations()
            
        except Exception as e:
            self._append_message("System", f"Error: {str(e)}")