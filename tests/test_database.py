import pytest
from src.utils.database import Database
from pathlib import Path
import json

def test_database_initialization():
    db = Database()
    assert db.sessions_file.exists()
    data = json.loads(db.sessions_file.read_text())
    assert isinstance(data, dict)
    assert "sessions" in data
    assert isinstance(data["sessions"], list)

def test_get_sessions_with_legacy_data(tmp_path):
    db = Database()
    # Create legacy format data
    db.sessions_file.write_text(json.dumps([{"id": 1, "date": "2024-02-08"}]))
    sessions = db.get_sessions()
    assert isinstance(sessions, list)
    assert len(sessions) == 1