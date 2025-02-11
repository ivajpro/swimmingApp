import sqlite3
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self):
        self.db_path = Path(__file__).parent / "swimming.db"
        self.conn = None
        self.initialize_database()

    def initialize_database(self):
        """Create database and tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()

        # Create swimming sessions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS swimming_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            duration INTEGER NOT NULL,
            distance REAL NOT NULL,
            stroke_type TEXT NOT NULL,
            notes TEXT
        )
        ''')

        self.conn.commit()

    def add_session(self, duration: int, distance: float, stroke_type: str, notes: str = ""):
        """Add a new swimming session to the database"""
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO swimming_sessions (date, duration, distance, stroke_type, notes)
        VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), duration, distance, stroke_type, notes))
        self.conn.commit()

    def get_all_sessions(self):
        """Retrieve all swimming sessions"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM swimming_sessions ORDER BY date DESC')
        return cursor.fetchall()

    def __del__(self):
        """Close database connection when object is destroyed"""
        if self.conn:
            self.conn.close()