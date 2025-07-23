import sqlite3
from typing import Optional

def init_db(db_path="civicvoice.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_text TEXT,
            language TEXT,
            location TEXT,
            consent INTEGER,
            image BLOB,
            image_caption TEXT,
            audio BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            username TEXT
        )
    ''')
    # Add username column if it doesn't exist (for migration)
    try:
        c.execute('ALTER TABLE submissions ADD COLUMN username TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    conn.commit()
    conn.close()

def insert_submission(issue_text: str, language: str, location: str, consent: bool, image: Optional[bytes], image_caption: Optional[str], audio: Optional[bytes], username: Optional[str], db_path="civicvoice.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO submissions (issue_text, language, location, consent, image, image_caption, audio, username)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (issue_text, language, location, int(consent), image, image_caption, audio, username))
    conn.commit()
    conn.close()

def fetch_all_submissions(db_path="civicvoice.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM submissions ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def count_submissions(db_path="civicvoice.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM submissions')
    count = c.fetchone()[0]
    conn.close()
    return count 