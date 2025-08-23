import json
import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import hashlib
from pathlib import Path

HISTORY_FILE = os.path.join("history", "conversations.json")
DATABASE_FILE = os.path.join("history", "conversations.db")

class HistoryManager:
    def __init__(self):
        self.history_dir = Path("history")
        self.history_dir.mkdir(exist_ok=True)
        
        # 初始化数据库
        self.init_database()
        
        # 如果JSON文件存在但数据库为空，迁移数据
        if os.path.exists(HISTORY_FILE) and not self.has_conversations():
            self.migrate_from_json()
    
    def init_database(self):
        """初始化SQLite数据库"""
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            
            # 创建对话表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    message_count INTEGER DEFAULT 0,
                    total_tokens INTEGER DEFAULT 0,
                    tags TEXT DEFAULT '',
                    is_favorite BOOLEAN DEFAULT 0,
                    is_archived BOOLEAN DEFAULT 0
                )
            """)
            
            # 创建消息表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    token_count INTEGER DEFAULT 0,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                )
            """)
            
            # 创建索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_updated ON conversations(updated_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_msg_conv ON messages(conversation_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_title ON conversations(title)")
            
            conn.commit()
    
    def migrate_from_json(self):
        """从JSON文件迁移数据到数据库"""
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            conversations = data.get("conversations", [])
            for conv in conversations:
                self.save_conversation_to_db(
                    conv["id"], 
                    conv["title"], 
                    conv["messages"], 
                    conv.get("created_at", datetime.now().isoformat()),
                    conv.get("updated_at", datetime.now().isoformat())
                )
            
            print(f"成功迁移 {len(conversations)} 个对话到数据库")
        except Exception as e:
            print(f"迁移数据失败: {e}")
    
    def has_conversations(self) -> bool:
        """检查数据库是否有对话记录"""
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM conversations")
            return cursor.fetchone()[0] > 0
    
    def load_conversations(self, limit: int = 100, offset: int = 0, 
                          search_query: str = "", is_favorite: bool = None,
                          is_archived: bool = False) -> List[Dict]:
        """从数据库加载对话列表"""
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT id, title, created_at, updated_at, message_count, 
                       total_tokens, tags, is_favorite, is_archived
                FROM conversations 
                WHERE is_archived = ?
            """
            params = [is_archived]
            
            # 添加搜索条件
            if search_query:
                query += " AND title LIKE ?"
                params.append(f"%{search_query}%")
            
            # 添加收藏过滤
            if is_favorite is not None:
                query += " AND is_favorite = ?"
                params.append(is_favorite)
            
            query += " ORDER BY updated_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            conversations = []
            for row in rows:
                conversations.append({
                    "id": row[0],
                    "title": row[1],
                    "created_at": row[2],
                    "updated_at": row[3],
                    "message_count": row[4],
                    "total_tokens": row[5],
                    "tags": row[6].split(",") if row[6] else [],
                    "is_favorite": bool(row[7]),
                    "is_archived": bool(row[8])
                })
            
            return conversations
    
    def load_conversation_messages(self, conversation_id: str) -> List[Dict]:
        """加载指定对话的消息"""
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT role, content, timestamp, token_count
                FROM messages 
                WHERE conversation_id = ? 
                ORDER BY id ASC
            """, (conversation_id,))
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    "role": row[0],
                    "content": row[1],
                    "timestamp": row[2],
                    "token_count": row[3]
                })
            
            return messages
    
    def save_conversation(self, conv_id: str, title: str, messages: List[Dict], is_new: bool):
        """保存对话（兼容性方法）"""
        if is_new:
            created_at = datetime.now().isoformat()
            updated_at = created_at
        else:
            # 获取原始创建时间
            created_at = self.get_conversation_created_time(conv_id)
            updated_at = datetime.now().isoformat()
        
        self.save_conversation_to_db(conv_id, title, messages, created_at, updated_at)
    
    def save_conversation_to_db(self, conv_id: str, title: str, messages: List[Dict], 
                               created_at: str, updated_at: str):
        """保存对话到数据库"""
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            
            # 计算统计信息
            message_count = len([m for m in messages if m["role"] in ["user", "assistant"]])
            total_tokens = sum(len(m["content"].split()) for m in messages)
            
            # 保存或更新对话记录
            cursor.execute("""
                INSERT OR REPLACE INTO conversations 
                (id, title, created_at, updated_at, message_count, total_tokens)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (conv_id, title, created_at, updated_at, message_count, total_tokens))
            
            # 删除旧消息
            cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
            
            # 保存新消息
            for msg in messages:
                token_count = len(msg["content"].split())
                timestamp = msg.get("timestamp", updated_at)
                
                cursor.execute("""
                    INSERT INTO messages (conversation_id, role, content, timestamp, token_count)
                    VALUES (?, ?, ?, ?, ?)
                """, (conv_id, msg["role"], msg["content"], timestamp, token_count))
            
            conn.commit()
    
    def get_conversation_created_time(self, conv_id: str) -> str:
        """获取对话创建时间"""
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT created_at FROM conversations WHERE id = ?", (conv_id,))
            result = cursor.fetchone()
            return result[0] if result else datetime.now().isoformat()
    
    def delete_conversation(self, conv_id: str):
        """删除对话"""
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
            cursor.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
            conn.commit()
    
    def toggle_favorite(self, conv_id: str) -> bool:
        """切换收藏状态"""
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT is_favorite FROM conversations WHERE id = ?", (conv_id,))
            result = cursor.fetchone()
            
            if result:
                new_status = not bool(result[0])
                cursor.execute("UPDATE conversations SET is_favorite = ? WHERE id = ?", 
                             (new_status, conv_id))
                conn.commit()
                return new_status
            return False
    
    def archive_conversation(self, conv_id: str, archived: bool = True):
        """归档对话"""
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE conversations SET is_archived = ? WHERE id = ?", 
                         (archived, conv_id))
            conn.commit()
    
    def add_tags(self, conv_id: str, tags: List[str]):
        """添加标签"""
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            tags_str = ",".join(tags)
            cursor.execute("UPDATE conversations SET tags = ? WHERE id = ?", 
                         (tags_str, conv_id))
            conn.commit()
    
    def search_conversations(self, query: str) -> List[Dict]:
        """搜索对话"""
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            
            # 搜索标题和消息内容
            cursor.execute("""
                SELECT DISTINCT c.id, c.title, c.created_at, c.updated_at, 
                       c.message_count, c.total_tokens, c.tags, c.is_favorite, c.is_archived
                FROM conversations c
                LEFT JOIN messages m ON c.id = m.conversation_id
                WHERE c.title LIKE ? OR m.content LIKE ?
                ORDER BY c.updated_at DESC
            """, (f"%{query}%", f"%{query}%"))
            
            rows = cursor.fetchall()
            conversations = []
            for row in rows:
                conversations.append({
                    "id": row[0],
                    "title": row[1],
                    "created_at": row[2],
                    "updated_at": row[3],
                    "message_count": row[4],
                    "total_tokens": row[5],
                    "tags": row[6].split(",") if row[6] else [],
                    "is_favorite": bool(row[7]),
                    "is_archived": bool(row[8])
                })
            
            return conversations
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            
            # 总对话数
            cursor.execute("SELECT COUNT(*) FROM conversations WHERE is_archived = 0")
            total_conversations = cursor.fetchone()[0]
            
            # 总消息数
            cursor.execute("SELECT COUNT(*) FROM messages")
            total_messages = cursor.fetchone()[0]
            
            # 收藏数
            cursor.execute("SELECT COUNT(*) FROM conversations WHERE is_favorite = 1")
            favorite_count = cursor.fetchone()[0]
            
            # 今天的对话数
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT COUNT(*) FROM conversations WHERE created_at LIKE ?", 
                         (f"{today}%",))
            today_conversations = cursor.fetchone()[0]
            
            return {
                "total_conversations": total_conversations,
                "total_messages": total_messages,
                "favorite_count": favorite_count,
                "today_conversations": today_conversations
            }
    
    def export_all_conversations(self) -> List[Dict]:
        """导出所有对话（用于备份）"""
        conversations = self.load_conversations(limit=99999)
        for conv in conversations:
            conv["messages"] = self.load_conversation_messages(conv["id"])
        return conversations
    
    def cleanup_old_conversations(self, days: int = 90):
        """清理旧对话"""
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        cutoff_iso = datetime.fromtimestamp(cutoff_date).isoformat()
        
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            
            # 获取要删除的对话ID
            cursor.execute("""
                SELECT id FROM conversations 
                WHERE updated_at < ? AND is_favorite = 0 AND is_archived = 1
            """, (cutoff_iso,))
            
            old_convs = cursor.fetchall()
            
            # 删除消息和对话
            for conv_id in old_convs:
                cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id[0],))
                cursor.execute("DELETE FROM conversations WHERE id = ?", (conv_id[0],))
            
            conn.commit()
            return len(old_convs)
    
    @staticmethod
    def generate_title(messages: List[Dict]) -> str:
        """生成对话标题"""
        for msg in messages:
            if msg["role"] == "user":
                content = msg["content"].strip()
                # 移除多余的空白字符
                content = " ".join(content.split())
                return (content[:30] + '...') if len(content) > 30 else content
        return "New Chat"