import sqlite3

DB_FILE = "seen.db"

conn = sqlite3.connect(DB_FILE)

conn.execute("""
CREATE TABLE IF NOT EXISTS seen (
    id TEXT PRIMARY KEY
)
""")

conn.commit()


def already_sent(item_id):
    cur = conn.execute(
        "SELECT 1 FROM seen WHERE id=?",
        (item_id,)
    )
    return cur.fetchone() is not None


def mark_sent(item_id):
    conn.execute(
        "INSERT OR IGNORE INTO seen(id) VALUES(?)",
        (item_id,)
    )
    conn.commit()
