import os
from models.init_db import initialize_db
from ui.dashboard import launch_dashboard

DB_PATH = r"project5_Finance_Tracker\db\finance_tracker.db"

def main():
    
    if not os.path.exists(DB_PATH):
        initialize_db()
    
    launch_dashboard()

if __name__ == "__main__":
    main()
