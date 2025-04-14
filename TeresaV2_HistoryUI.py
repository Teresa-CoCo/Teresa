import json
import os
from datetime import datetime
from typing import List, Dict

HISTORY_FILE = os.path.join("history", "conversations.json")

class HistoryManager:
    def __init__(self):
        os.makedirs("history", exist_ok=True)
        if not os.path.exists(HISTORY_FILE):
            self._init_history_file()
    
    def _init_history_file(self):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump({"conversations": []}, f, indent=2)
    
    def load_conversations(self) -> List[Dict]:
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("conversations", [])
        except:
            return []
    
    def save_conversation(self, conv_id: str, title: str, messages: List[Dict], is_new: bool):
        data = {"conversations": []}
        
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        now = datetime.now().isoformat()
        
        if is_new:
            data["conversations"].append({
                "id": conv_id,
                "title": title,
                "messages": messages,
                "created_at": now,
                "updated_at": now
            })
        else:
            for conv in data["conversations"]:
                if conv["id"] == conv_id:
                    conv["messages"] = messages
                    conv["updated_at"] = now
                    break
        
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def generate_title(messages: List[Dict]) -> str:
        for msg in messages:
            if msg["role"] == "user":
                content = msg["content"]
                return (content[:25] + '...') if len(content) > 25 else content
        return "New Chat"