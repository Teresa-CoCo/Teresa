import os
import json
from datetime import datetime
from typing import List, Dict, Optional

HISTORY_FILE = "history/conversation_history.json"

def ensure_history_dir():
    """确保历史目录存在"""
    os.makedirs("history", exist_ok=True)
    
    # 初始化历史文件如果不存在
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump({"conversations": []}, f, ensure_ascii=False, indent=2)

def save_new_conversation(messages: List[Dict], title: str):
    """保存新对话到历史文件"""
    ensure_history_dir()
    
    conversation = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "title": title,
        "messages": messages,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # 读取现有数据
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 追加新对话
    data["conversations"].append(conversation)
    
    # 写回文件
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return conversation["id"]

def update_conversation(conversation_id: str, new_messages: List[Dict]):
    """更新已有对话"""
    ensure_history_dir()
    
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 查找并更新对话
    for conv in data["conversations"]:
        if conv["id"] == conversation_id:
            conv["messages"] = new_messages
            conv["updated_at"] = datetime.now().isoformat()
            break
    
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_conversations() -> List[Dict]:
    """加载所有历史对话"""
    ensure_history_dir()
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("conversations", [])
    except:
        return []

def generate_title(messages: List[Dict]) -> str:
    """生成对话标题"""
    for msg in messages:
        if msg["role"] == "user":
            content = msg["content"]
            return content[:30] + ("..." if len(content) > 30 else "")
    return "未命名对话"