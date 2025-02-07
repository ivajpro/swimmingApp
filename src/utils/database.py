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
            # Read existing sessions
            sessions = self.get_sessions()
            
            # Add unique ID and timestamp
            session_data["id"] = len(sessions) + 1
            session_data["created_at"] = datetime.now().isoformat()
            
            # Add new session
            sessions.append(session_data)
            
            # Save updated data
            self.sessions_file.write_text(
                json.dumps(sessions, indent=2, default=str)
            )
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

    def delete_session(self, session_id: int) -> bool:
        """Delete a session by ID"""
        try:
            sessions = self.get_sessions()
            sessions = [s for s in sessions if s.get('id') != session_id]
            self.sessions_file.write_text(json.dumps(sessions, indent=2, default=str))
            return True
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False

    def update_session(self, session_data: dict) -> bool:
        """Update an existing session"""
        try:
            sessions = self.get_sessions()
            for i, session in enumerate(sessions):
                if session.get('id') == session_data['id']:
                    sessions[i] = session_data
                    self.sessions_file.write_text(
                        json.dumps(sessions, indent=2, default=str)
                    )
                    return True
            return False
        except Exception as e:
            print(f"Error updating session: {e}")
            return False

