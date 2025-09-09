import sqlite3
import os

DB_PATH = r"project5_Finance_Tracker\db\finance_tracker.db"

def initialize_db():
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.executescript("""
        CREATE TABLE "credit_cards" (
        "id"	INTEGER NOT NULL UNIQUE,
        "name"	TEXT,
        "cashback_categories"	TEXT,
        "cashback_rates"	TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
        );
    
        CREATE TABLE "bank_accounts" (
        "id"	INTEGER NOT NULL UNIQUE,
        "name"	TEXT,
        "type"	TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
        );
        
        CREATE TABLE "assets" (
        "id"	INTEGER NOT NULL UNIQUE,
        "name"	TEXT,
        "type"	TEXT,
        "details"	TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
        );
        
        CREATE TABLE "income" (
        "id"	INTEGER NOT NULL UNIQUE,
        "amount"	REAL,
        "source"	TEXT,
        "date"	TEXT,
        "account"	INTEGER,
        "recurring"	TEXT,
        "asset"	INTEGER,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("account") REFERENCES "bank_accounts"("id"),
        FOREIGN KEY("asset") REFERENCES "assets"("id")
        );
        
        CREATE TABLE "stocks" (
        "id"	INTEGER NOT NULL UNIQUE,
        "symbol"	TEXT,
        "shares"	INTEGER,
        "value"	REAL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );
        
        CREATE TABLE "credit_card_perks" (
        "id"	INTEGER NOT NULL UNIQUE,
        "card_id"	INTEGER,
        "category"	TEXT,
        "rate"	REAL,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("card_id") REFERENCES "credit_cards"("id")
        );
        
        CREATE TABLE "transactions" (
        "id"	INTEGER NOT NULL UNIQUE,
        "amount"	REAL NOT NULL,
        "category"	TEXT,
        "date"	TEXT,
        "payment_method"	INTEGER,
        "account"	INTEGER,
        "notes"	TEXT,
        "type"	TEXT,
        "recurring"	TEXT,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("account") REFERENCES "bank_accounts"("id"),
        FOREIGN KEY("payment_method") REFERENCES "credit_cards"("id")
        );
    """)
    
    conn.commit()
    conn.close()