import json
import os
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self):
        self.data_dir = Path("data")
        self.sessions_file = self.data_dir / "sessions.json"
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Create data directory and files if they don't exist"""
        self.data_dir.mkdir(exist_ok=True)
        if not self.sessions_file.exists():
            self.sessions_file.write_text("[]")
    
    def save_session(self, session_data: dict) -> bool:
        """Save a new session to the database"""
        try:
            sessions = self.get_sessions()
            session_data["id"] = len(sessions) + 1
            sessions.append(session_data)
            self.sessions_file.write_text(json.dumps(sessions, indent=2, default=str))
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
    
    def get_sessions(self) -> list:
        """Get all sessions from the database"""
        try:
            return json.loads(self.sessions_file.read_text())
        except Exception as e:
            print(f"Error reading sessions: {e}")
            return []

