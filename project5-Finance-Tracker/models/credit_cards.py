import sqlite3
import os

DB_PATH = r"project5_Finance_Tracker\db\finance_tracker.db"

def get_all_credit_cards():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    base_query = "SELECT id, name, cashback_categories, cashback_rates from credit_cards ORDER BY name DESC;"
    
    c.execute(base_query)
    results = c.fetchall()
    conn.close()
    
    return results

def get_all_perks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    base_query = """
        SELECT ccp.category, cc.name, ccp.rate
        FROM credit_card_perks ccp
        JOIN credit_cards cc ON ccp.card_id = cc.id
        WHERE ccp.rate = (
            SELECT MAX(rate)
            FROM credit_card_perks
            WHERE category = ccp.category
        )
        GROUP BY ccp.category;
    """
    
    c.execute(base_query)
    results = c.fetchall()
    conn.close()
    return results

def insert_credit_cards(name, cashback_categories, cashback_rates):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO credit_cards (name, cashback_categories, cashback_rates)
        VALUES (?, ?, ?)""", (name, cashback_categories, cashback_rates))
    card_id = c.lastrowid
    c.execute("""INSERT INTO credit_card_perks (card_id, category, rate)
        VALUES (?, ?, ?)""", (card_id, cashback_categories, cashback_rates))
    conn.commit()
    conn.close()