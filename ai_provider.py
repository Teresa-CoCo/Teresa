"""
Teresa V2 AI提供者模块
支持多种AI服务提供商
"""
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from openai import OpenAI
import json
from typing import List, Dict, Optional
from config import config

class AIProvider(QObject):
    """AI提供者基类"""
    
    response_ready = pyqtSignal(str)  # 响应完成
    stream_chunk = pyqtSignal(str)   # 流式响应块
    error_occurred = pyqtSignal(str)  # 错误发生
    
    def __init__(self):
        super().__init__()
        self.client = None
        self.threads = []  # 保存线程引用
        self.setup_client()
    
    def setup_client(self):
        """设置客户端"""
        api_config = config.api
        
        if api_config.provider == "deepseek":
            self.client = OpenAI(
                api_key=api_config.api_key,
                base_url="https://api.deepseek.com"
            )
        elif api_config.provider == "openai":
            self.client = OpenAI(api_key=api_config.api_key)
        # 可以添加更多提供商
    def generate_response(self, messages: List[Dict]):
        worker = AIWorker(self.client, messages, config.api)
        worker.response_ready.connect(self.response_ready.emit)
        worker.stream_chunk.connect(self.stream_chunk.emit)
        worker.error_occurred.connect(self.error_occurred.emit)
        thread = QThread()
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.start()
        self.threads.append(thread)

    def stop_all_threads(self):
        for thread in self.threads:
            if thread.isRunning():
                thread.quit()
                thread.wait()
        self.threads.clear()
    def closeEvent(self, event):
        if hasattr(self.ai_provider, "stop_all_threads"):
            self.ai_provider.stop_all_threads()
        event.accept()


class AIWorker(QObject):
    """AI工作线程"""
    
    response_ready = pyqtSignal(str)
    stream_chunk = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, client, messages, api_config):
        super().__init__()
        self.client = client
        self.messages = messages
        self.api_config = api_config
    
    def run(self):
        """执行AI请求"""
        try:
            if self.api_config.stream:
                self._stream_response()
            else:
                self._single_response()
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.finished.emit()
    
    def _stream_response(self):
        """流式响应"""
        try:
            response = self.client.chat.completions.create(
                model=self.api_config.model,
                messages=self.messages,
                temperature=self.api_config.temperature,
                max_tokens=self.api_config.max_tokens,
                stream=True
            )
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    self.stream_chunk.emit(content)
            
            self.response_ready.emit(full_response)
            
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def _single_response(self):
        """单次响应"""
        try:
            response = self.client.chat.completions.create(
                model=self.api_config.model,
                messages=self.messages,
                temperature=self.api_config.temperature,
                max_tokens=self.api_config.max_tokens
            )
            
            content = response.choices[0].message.content
            self.response_ready.emit(content)
            
        except Exception as e:
            self.error_occurred.emit(str(e))
    
