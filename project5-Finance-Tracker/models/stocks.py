import sqlite3
import os

DB_PATH = r"project5_Finance_Tracker\db\finance_tracker.db"

def get_all_stocks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    base_query = """SELECT id, symbol, shares, value FROM stocks;"""
        
    c.execute(base_query)
    results = c.fetchall()
    conn.close()
    return results

def insert_stocks(symbol, shares, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO stocks (symbol, shares, value)
        VALUES (?, ?, ?)""", (symbol, shares, value))
    conn.commit()
    conn.close()