import sqlite3
import os

DB_PATH = r"project5_Finance_Tracker\db\finance_tracker.db"

def get_all_banks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    base_query = "SELECT id, name, type FROM bank_accounts ORDER BY name DESC;"
    
    c.execute(base_query)
    results = c.fetchall()
    conn.close()
    
    return results

def insert_bank_accounts(name, type):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO bank_accounts (name, type)
        VALUES (?, ?)""", (name, type))
    conn.commit()
    conn.close()