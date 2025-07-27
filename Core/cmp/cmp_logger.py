import sqlite3
from datetime import datetime

def log_action(agent, action_type, cost, status):
    conn = sqlite3.connect("cmp_log.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        agent TEXT,
        action TEXT,
        cost REAL,
        status TEXT
    )""")
    c.execute("INSERT INTO logs (timestamp, agent, action, cost, status) VALUES (?, ?, ?, ?, ?)",
              (datetime.now().isoformat(), agent, action_type, cost, status))
    conn.commit()
    conn.close()
