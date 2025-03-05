import sqlite3
import json

DB_PATH = "receipts.db"

def init_db():
    """Initialize SQLite database and create receipts table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            receipt_id TEXT PRIMARY KEY,
            store_name TEXT,
            date TEXT,
            items TEXT,
            total REAL
        )
    """)
    conn.commit()
    conn.close()

def save_to_sqlite(data):
    """Store processed receipt data in SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO receipts (receipt_id, store_name, date, items, total)
            VALUES (?, ?, ?, ?, ?)
        """, (data["receipt_id"], data["store_name"], data["date"], json.dumps(data["items"]), data["total"]))
        conn.commit()
        conn.close()
        print(f"Data successfully saved to SQLite. Receipt ID: {data['receipt_id']}")
    except sqlite3.IntegrityError:
        print(f"Failed: Receipt ID {data['receipt_id']} already exists, avoiding duplicate storage.")
    except Exception as e:
        print(f"Error saving to SQLite: {e}")