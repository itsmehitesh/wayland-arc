import sqlite3
import pandas as pd
import os

class TelemetryDatabase:
    """Manages high-frequency edge data collection and time-series history"""
    def __init__(self, db_path='data/wayland.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        os.makedirs('data', exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS process_telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                x_position REAL,
                bead_width REAL,
                voltage REAL,
                current REAL
            )
        ''')
        conn.commit()
        conn.close()

    def log_reading(self, x_pos, bead_width, voltage, current):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO process_telemetry (x_position, bead_width, voltage, current)
            VALUES (?, ?, ?, ?)
        ''', (x_pos, bead_width, voltage, current))
        conn.commit()
        conn.close()

    def fetch_recent(self, limit=100):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(f'''
            SELECT * FROM process_telemetry 
            ORDER BY timestamp DESC LIMIT {limit}
        ''', conn)
        conn.close()
        return df.sort_values('timestamp')