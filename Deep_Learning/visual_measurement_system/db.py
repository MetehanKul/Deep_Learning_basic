# db.py
import sqlite3
from datetime import datetime
from typing import Dict, Any

DB_PATH = "measurements.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY,
            part_name TEXT UNIQUE,
            metadata TEXT
        );
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY,
            part_name TEXT,
            measure_name TEXT,
            measured_value REAL,
            reference_value REAL,
            tolerance REAL,
            pass_fail INTEGER,
            timestamp TEXT
        );
    ''')
    conn.commit()
    conn.close()

def save_part(part_name: str, metadata: str = ""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO parts (part_name, metadata) VALUES (?,?)', (part_name, metadata))
    conn.commit()
    conn.close()

def save_measurement(record: Dict[str, Any]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO measurements
        (part_name, measure_name, measured_value, reference_value, tolerance, pass_fail, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        record['part_name'],
        record['measure_name'],
        record['measured_value'],
        record['reference_value'],
        record['tolerance'],
        1 if record['pass_fail'] else 0,
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
