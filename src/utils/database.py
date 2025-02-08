import json
import os
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self):
        self.data_dir = Path("data")
        self.sessions_file = self.data_dir / "sessions.json"
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Ensure data directory and files exist"""
        self.data_dir.mkdir(exist_ok=True)
        if not self.sessions_file.exists():
            self._write_empty_db()
    
    def _write_empty_db(self):
        """Initialize empty database structure"""
        self.sessions_file.write_text(json.dumps({"sessions": []}, indent=2))
    
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
                json.dumps({"sessions": sessions}, indent=2, default=str)
            )
            return True
            
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
    
    def get_sessions(self) -> list:
        """Get all sessions from the database"""
        try:
            if not self.sessions_file.exists():
                self._write_empty_db()
                return []
            
            data = json.loads(self.sessions_file.read_text())
            if isinstance(data, list):
                # Handle legacy data format
                return data
            return data.get("sessions", [])
        except Exception as e:
            print(f"Error loading sessions: {e}")
            # Backup corrupted file
            if self.sessions_file.exists():
                backup_path = self.sessions_file.with_suffix('.json.bak')
                self.sessions_file.rename(backup_path)
            # Create new empty database
            self._write_empty_db()
            return []

    def delete_session(self, session_id: int) -> bool:
        """Delete a session by ID"""
        try:
            sessions = self.get_sessions()
            original_length = len(sessions)
            sessions = [s for s in sessions if s.get('id') != session_id]
            
            # Only write if we actually removed a session
            if len(sessions) < original_length:
                self.sessions_file.write_text(json.dumps({"sessions": sessions}, indent=2, default=str))
                return True
            return False
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
                        json.dumps({"sessions": sessions}, indent=2, default=str)
                    )
                    return True
            return False
        except Exception as e:
            print(f"Error updating session: {e}")
            return False

    def validate_session_data(self, session_data: dict) -> bool:
        """Validate session data before saving"""
        required_fields = ["date", "sets"]
        if not all(field in session_data for field in required_fields):
            return False
            
        # Validate sets
        for set_data in session_data.get("sets", []):
            if "stroke" not in set_data:
                return False
            # Validate mixed stroke format
            if set_data["stroke"].startswith("mix"):
                strokes = set_data.get("mixed_strokes", [])
                valid_strokes = ["freestyle", "backstroke", "breaststroke", "butterfly"]
                if not strokes or not all(s in valid_strokes for s in strokes):
                    return False
        
        return True

