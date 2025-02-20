from typing import List
import sqlite3

class Migration:
    def __init__(self, version: int, up: str, down: str):
        self.version = version
        self.up = up
        self.down = down

class MigrationManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.migrations: List[Migration] = [
            Migration(
                version=1,
                up="""
                ALTER TABLE swimming_sessions 
                ADD COLUMN pool_length INTEGER DEFAULT 25
                """,
                down="ALTER TABLE swimming_sessions DROP COLUMN pool_length"
            )
        ]