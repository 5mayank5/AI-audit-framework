import sqlite3
import json
import yaml
import os

class AuditDataStore:

    def __init__(self):
        with open("config.yaml") as f:
            config = yaml.safe_load(f)

        self.db_name = config["database"]["name"]
        self._initialize_database()

    def _initialize_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            results TEXT
        )
        """)

        conn.commit()
        conn.close()

    def save(self, data):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO audit (results) VALUES (?)",
            (json.dumps(data),)
        )

        conn.commit()
        conn.close()