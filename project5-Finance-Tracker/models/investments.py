import sqlite3
import os

DB_PATH = r"project5_Finance_Tracker\db\finance_tracker.db"


def get_all_investments():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    base_query = """SELECT name, type, details FROM assets WHERE type LIKE 'Investments';"""
        
    c.execute(base_query)
    results = c.fetchall()
    conn.close()
    return results

def get_investments_by_filter(filter_option):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    base_query = """SELECT name, type, details FROM assets WHERE type LIKE 'Investments'"""
    
    if filter_option == "Name Asc":
        base_query += "ORDER BY name ASC;"
    elif filter_option == "Name Desc":
        base_query += "ORDER BY name DESC;"
    elif filter_option == "Type Asc":
        base_query += "ORDER BY type ASC;"
    elif filter_option == "Type Desc":
        base_query += "ORDER BY type DESC;"
    elif filter_option == "Details Asc":
        base_query += "ORDER BY details ASC;"
    elif filter_option == "Details Desc":
        base_query += "ORDER BY details DESC;"
    else:
        base_query += "ORDER BY name DESC;"
        
    c.execute(base_query)
    results = c.fetchall()
    conn.close()
    return results

def insert_investment(name, type, details):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO assets (name, type, details)
        VALUES (?, ?, ?)""", (name, type, details))
    conn.commit()
    conn.close()