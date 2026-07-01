import sqlite3

conn = sqlite3.connect("seen.db")
conn.execute("CREATE TABLE IF NOT EXISTS seen(id TEXT PRIMARY KEY)")
conn.commit()

def has_seen(i):
    cur = conn.execute("SELECT 1 FROM seen WHERE id=?", (i,))
    return cur.fetchone() is not None

def mark(i):
    conn.execute("INSERT OR IGNORE INTO seen VALUES(?)", (i,))
    conn.commit()
