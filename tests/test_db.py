import os
import tempfile
import sqlite3
from db import DB_PATH, init_db, insert_entry, fetch_entry_by_date, fetch_all_dates

def test_db_insert_and_fetch(tmp_path, monkeypatch):
    dbfile = tmp_path / "test_entries.db"
    monkeypatch.setattr("db.DB_PATH", str(dbfile))
    init_db()
    insert_entry("2025-09-20", "my journal", "intention", "a dream", "p1,p2,p3", "reflection text", "strategy text")
    dates = fetch_all_dates()
    assert "2025-09-20" in dates
    rec = fetch_entry_by_date("2025-09-20")
    assert rec["journal"] == "my journal"
    assert "reflection" in rec and rec["reflection"] == "reflection text"
