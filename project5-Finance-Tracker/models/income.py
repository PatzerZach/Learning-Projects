import sqlite3
import os

DB_PATH = r"project5_Finance_Tracker\db\finance_tracker.db"

def get_all_income():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    base_query = """SELECT i.id, i.date, i.source, i.amount, ba.name, a.name, i.recurring FROM income i
    LEFT OUTER JOIN bank_accounts ba
    ON i.account = ba.id
    LEFT OUTER JOIN assets a
    ON i.asset = a.id;"""
    
    c.execute(base_query)
    results = c.fetchall()
    conn.close()
    return results


def get_income_by_filter(filter_option):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    base_query = "SELECT date, source, amount, account, asset, recurring FROM income"
    
    if filter_option == "Date Asc":
        base_query += "ORDER BY date ASC;"
    elif filter_option == "Date Desc":
        base_query += "ORDER BY date DESC;"
    elif filter_option == "Amount Asc":
        base_query += "ORDER BY amount ASC;"
    elif filter_option == "Amount Desc":
        base_query += "ORDER BY amount DESC;"
    elif filter_option == "Source Asc":
        base_query += "ORDER BY source ASC;"
    elif filter_option == "Source Desc":
        base_query += "ORDER BY source DESC;"
    else:
        base_query += "ORDER BY date DESC;"
        
    c.execute(base_query)
    results = c.fetchall()
    conn.close()
    return results

def insert_income(amount, source, account, asset, date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO income (amount, source, account, asset, date)
        VALUES (?, ?, ?, ?, ?)""", (amount, source, account, asset, date))
    conn.commit()
    conn.close()