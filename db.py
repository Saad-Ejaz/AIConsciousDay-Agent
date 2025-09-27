import sqlite3
from sqlite3 import Connection

DB_PATH = "entries.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS entries (
id INTEGER PRIMARY KEY AUTOINCREMENT,
date TEXT,
journal TEXT,
intention TEXT,
dream TEXT,
priorities TEXT,
reflection TEXT,
strategy TEXT
);
"""

def get_conn() -> Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    conn.close()

def insert_entry(entry_date, journal, intention, dream, priorities, reflection, strategy):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO entries (date, journal, intention, dream, priorities, reflection, strategy) VALUES (?,?,?,?,?,?,?)",
        (entry_date, journal, intention, dream, priorities, reflection, strategy)
    )
    conn.commit()
    conn.close()

def fetch_entry_by_date(d):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT date, journal, intention, dream, priorities, reflection, strategy FROM entries WHERE date = ? ORDER BY id DESC", (d,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "date": row[0],
            "journal": row[1],
            "intention": row[2],
            "dream": row[3],
            "priorities": row[4],
            "reflection": row[5],
            "strategy": row[6]
        }
    return None

def fetch_all_dates():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT date FROM entries ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]
