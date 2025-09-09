import sqlite3
import os


DB_PATH = r"project5_Finance_Tracker\db\finance_tracker.db"


def get_all_transactions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    base_query = """
    SELECT 
        t.id AS id, 
        t.date AS date, 
        t.amount AS amount, 
        t.category AS category, 
        ba.name AS account, 
        cc.name AS payment_method, 
        t.type AS type, 
        t.notes AS notes 
    FROM transactions t
    LEFT OUTER JOIN bank_accounts ba
    ON t.account = ba.id
    LEFT OUTER JOIN credit_cards cc
    ON t.payment_method = cc.id
    
    UNION ALL
    
    SELECT
        i.id AS ID,
        i.date AS date,
        i.amount AS amount,
        i.source AS category,
        ba.name AS account,
        NULL AS payment_method,
        'Income' AS type,
        NULL AS notes
    FROM income i
    LEFT JOIN bank_accounts ba ON i.account = ba.id;
    """
        
    c.execute(base_query)
    results = c.fetchall()
    conn.close()
    return results


def get_transactions_by_filter(filter_option):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    base_query = "SELECT date, amount, category, account, payment_method, type, notes FROM transactions"
    
    if filter_option == "Date Asc":
        base_query += "ORDER BY date ASC;"
    elif filter_option == "Date Desc":
        base_query += "ORDER BY date DESC;"
    elif filter_option == "Amount Asc":
        base_query += "ORDER BY amount ASC;"
    elif filter_option == "Amount Desc":
        base_query += "ORDER BY amount DESC;"
    elif filter_option == "Category Asc":
        base_query += "ORDER BY category ASC;"
    elif filter_option == "Category Desc":
        base_query += "ORDER BY category DESC;"
    elif filter_option == "Account Asc":
        base_query += "ORDER BY account ASC;"
    elif filter_option == "Account Desc":
        base_query += "ORDER BY account DESC;"
    else:
        base_query += "ORDER BY date DESC;"
        
    c.execute(base_query)
    results = c.fetchall()
    conn.close()
    return results

def insert_transaction(amount, category, account_id, payment, type, note, date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO transactions (amount, category, account, payment_method, type, notes, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (amount, category, account_id, payment, type, note, date))
    conn.commit()
    conn.close()