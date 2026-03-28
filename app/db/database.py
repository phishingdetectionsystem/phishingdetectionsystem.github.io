import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "phishing_logs.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            is_phishing INTEGER,
            confidence REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def log_prediction(url, is_phishing, confidence):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO logs (url, is_phishing, confidence)
        VALUES (?, ?, ?)
    """, (url, int(is_phishing), confidence))

    conn.commit()
    conn.close()


def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM logs")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE is_phishing=1")
    phishing = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE is_phishing=0")
    safe = cursor.fetchone()[0]

    conn.close()

    return total, phishing, safe
