import customtkinter as ctk
from datetime import datetime
from tkcalendar import DateEntry
from models.transactions import insert_transaction
from models.income import insert_income
from models.banks import get_all_banks, insert_bank_accounts
from models.credit_cards import get_all_credit_cards, insert_credit_cards
from models.stocks import insert_stocks
from models.investments import insert_investment
from models.assets_income_sources import insert_asset

class PopupForm(ctk.CTkToplevel):
    def __init__(self, master, form_type, dashboard_ref=None):
        super().__init__(master)
        self.dashboard = dashboard_ref
        self.form_type = form_type
        self.title(f"Add {form_type.capitalize()}")
        self.geometry("400x600")
        self.resizable(False, False)

        self.transient(master)
        self.grab_set()

        self.categories = [
            "Groceries",
            "Dining",
            "Utilities",
            "Gas",
            "Travel",
            "Subscriptions",
            "Entertainment",
            "Other",
            "+ Create New Category"
        ]
        
        self.type_categories = [
            "expense",
            "income",
            "transfer",
            "refund",
            "credit"
        ]
        self.bank_accounts = {}
        self.credit_cards = {}

        self.build_form()
        
    def build_form(self):
        if self.form_type == "transactions":
            self.build_transaction_form()
        elif self.form_type == "income":
            self.build_income_form()
        elif self.form_type == "stocks":
            self.build_stock_form()
        elif self.form_type == "investments":
            self.build_investments_form()
        elif self.form_type == "credit_cards":
            self.build_credit_cards_form()
        elif self.form_type == "assets":
            self.build_assets_form()
        elif self.form_type == "bank_accounts":
            self.build_bank_accounts_form()
        else:
            ctk.CTkLabel(self, text="Unknown Form Type").pack(pady=20)

    def get_bank_account_names(self):
        accounts = get_all_banks()  # [(id, name)]
        self.bank_accounts = {name: id for id, name, _ in accounts}
        return list(self.bank_accounts.keys())
    
    def get_credit_cards(self):
        cards = get_all_credit_cards()
        self.credit_cards = {name: id for id, name, *_ in cards}
        return list(self.credit_cards.keys())

    def on_category_selected(self, choice):
        if choice == "+ Create New Category":
            dialog = ctk.CTkInputDialog(text="Enter new category name:", title="New Category")
            new_category = dialog.get_input()
            if new_category and new_category not in self.categories:
                self.categories.insert(-1, new_category)  # Add before "+ Create New"
                self.category_dropdown.configure(values=self.categories)
                self.category_dropdown.set(new_category)


    def build_transaction_form(self):
        
        ctk.CTkLabel(self, text="Add Transaction").pack(pady=10)
        
        self.date = DateEntry(self, font=("Segoe UI", 16), width=30, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
        self.date.set_date(datetime.now())
        self.date.pack(pady=5)

        self.amount = ctk.CTkEntry(self, placeholder_text="Amount", height=50, width=300)
        self.amount.pack(pady=5)

        self.category_dropdown = ctk.CTkOptionMenu(
            self, values=self.categories, command=self.on_category_selected, height=50, width=300
        )
        self.category_dropdown.pack(pady=5)

        account_options = self.get_bank_account_names()
        self.account_dropdown = ctk.CTkOptionMenu(self, values=account_options, height=50, width=300)
        self.account_dropdown.pack(pady=5)
        
        payment_methods = self.get_credit_cards()
        self.payment_method_dropdown = ctk.CTkOptionMenu(self, values=payment_methods, height=50, width=300)
        self.payment_method_dropdown.pack(pady=5)
        
        self.type_dropdown = ctk.CTkOptionMenu(self, values=self.type_categories, command=self.on_category_selected, height=50, width=300)
        self.type_dropdown.pack(pady=5)

        self.note = ctk.CTkEntry(self, placeholder_text="Note", height=50, width=300)
        self.note.pack(pady=5)

        ctk.CTkButton(self, text="Submit", command=self.submit_transaction).pack(pady=10)

    def submit_transaction(self):
        try:
            amount = float(self.amount.get())
            category = self.category_dropdown.get()
            account_name = self.account_dropdown.get()
            account_id = self.bank_accounts.get(account_name)
            payment_method = self.payment_method_dropdown.get()
            payment = self.credit_cards.get(payment_method)
            type = self.type_dropdown.get()
            note = self.note.get()
            date = self.date.get()

            insert_transaction(amount, category, account_id, payment, type, note, date)
            print("Transaction saved successfully.")
            if self.dashboard:
                self.dashboard.refresh_all_sections()
            self.destroy()
        except Exception as e:
            print("Error submitting transaction:", e)

    # ----------------------------
    # Income Form (similar structure)
    # ----------------------------
    
    def get_asset_names(self):
        from models.assets_income_sources import get_all_assets_income  # You might already have this
        assets = get_all_assets_income()
        self.asset_thing = {name: id for id, name, _type, details in assets}
        return list(self.asset_thing.keys())


    def build_income_form(self):
        ctk.CTkLabel(self, text="Add Income").pack(pady=10)

        self.date = DateEntry(self, font=("Segoe UI", 16), width=30, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
        self.date.set_date(datetime.now())
        self.date.pack(pady=5)

        self.amount = ctk.CTkEntry(self, placeholder_text="Amount", height=50, width=300)
        self.amount.pack(pady=5)

        # Dropdown populated from assets
        asset_asset = self.get_asset_names()
        self.asset_dropdown = ctk.CTkOptionMenu(self, values=asset_asset, height=50, width=300)
        self.asset_dropdown.pack(pady=5)

        # Optional manual entry
        self.source_manual = ctk.CTkEntry(self, placeholder_text="Or enter custom source", height=50, width=300)
        self.source_manual.pack(pady=5)

        account_options = self.get_bank_account_names()
        self.account_dropdown = ctk.CTkOptionMenu(self, values=account_options, height=50, width=300)
        self.account_dropdown.pack(pady=5)

        ctk.CTkButton(self, text="Submit", command=self.submit_income).pack(pady=10)

    def submit_income(self):
        try:
            amount = float(self.amount.get())

            # Use manual source if filled, else use dropdown
            source = self.source_manual.get().strip() or self.asset_dropdown.get() 

            account_name = self.account_dropdown.get()
            account_id = self.bank_accounts.get(account_name)
            
            asset_name = self.asset_dropdown.get()
            asset = self.asset_thing.get(asset_name)

            date = self.date.get()

            insert_income(amount, source, account_id, asset, date)
            print("Transaction saved successfully.")
            if self.dashboard:
                self.dashboard.refresh_all_sections()
            self.destroy()
        except Exception as e:
            print("Error submitting income:", e)


    def build_stock_form(self):
        ctk.CTkLabel(self, text="Add Stocks").pack(pady=10)

        self.symbol = ctk.CTkEntry(self, placeholder_text="Stock Symbol", height=50, width=300)
        self.symbol.pack(pady=5)

        self.shares = ctk.CTkEntry(self, placeholder_text="# of Shares", height=50, width=300)
        self.shares.pack(pady=5)

        self.value = ctk.CTkEntry(self, placeholder_text="Value of Shares", height=50, width=300)
        self.value.pack(pady=5)

        ctk.CTkButton(self, text="Submit", command=self.submit_stocks).pack(pady=10)
        
    def submit_stocks(self):
        try:
            symbol = self.symbol.get()

            shares = self.shares.get()

            value = self.value.get()

            insert_stocks(symbol, shares, value)
            print("Transaction saved successfully.")
            if self.dashboard:
                self.dashboard.refresh_all_sections()
            self.destroy()
        except Exception as e:
            print("Error submitting income:", e)

    def build_investments_form(self):
        ctk.CTkLabel(self, text="Add Investment / Investment Account").pack(pady=10)

        self.name = ctk.CTkEntry(self, placeholder_text="Name of Investment / Investment Account", height=50, width=300)
        self.name.pack(pady=5)

        self.details = ctk.CTkEntry(self, placeholder_text="Details of Account / Investment", height=50, width=300)
        self.details.pack(pady=5)

        ctk.CTkButton(self, text="Submit", command=self.submit_investment).pack(pady=10)
        
    def submit_investment(self):
        try:
            name = self.name.get()

            type = "Investments"

            details = self.details.get()

            insert_investment(name, type, details)
            print("Transaction saved successfully.")
            if self.dashboard:
                self.dashboard.refresh_all_sections()
            self.destroy()
        except Exception as e:
            print("Error submitting income:", e)


    def build_credit_cards_form(self):
        ctk.CTkLabel(self, text="Add Credit Card").pack(pady=10)

        self.name = ctk.CTkEntry(self, placeholder_text="Name of Credit Card", height=50, width=300)
        self.name.pack(pady=5)

        self.cashback_categories = ctk.CTkEntry(self, placeholder_text="Categories of Cashback", height=50, width=300)
        self.cashback_categories.pack(pady=5)

        self.cashback_rates = ctk.CTkEntry(self, placeholder_text="Rate of Cashback Categories", height=50, width=300)
        self.cashback_rates.pack(pady=5)

        ctk.CTkButton(self, text="Submit", command=self.submit_credit_card).pack(pady=10)
        
    def submit_credit_card(self):
        try:
            name = self.name.get()

            cashback_categories = self.cashback_categories.get()

            cashback_rates = self.cashback_rates.get()

            insert_credit_cards(name, cashback_categories, cashback_rates)
            print("Transaction saved successfully.")
            if self.dashboard:
                self.dashboard.refresh_all_sections()
            self.destroy()
        except Exception as e:
            print("Error submitting income:", e)

    def build_assets_form(self):
        ctk.CTkLabel(self, text="Add Asset").pack(pady=10)

        self.name = ctk.CTkEntry(self, placeholder_text="Name of Asset", height=50, width=300)
        self.name.pack(pady=5)
        
        self.type = ctk.CTkEntry(self, placeholder_text="Type of Asset", height=50, width=300)
        self.type.pack(pady=5)

        self.details = ctk.CTkEntry(self, placeholder_text="Details of Asset", height=50, width=300)
        self.details.pack(pady=5)

        ctk.CTkButton(self, text="Submit", command=self.submit_asset).pack(pady=10)
        
    def submit_asset(self):
        try:
            name = self.name.get()

            type = self.type.get()

            details = self.details.get()

            insert_asset(name, type, details)
            print("Transaction saved successfully.")
            if self.dashboard:
                self.dashboard.refresh_all_sections()
            self.destroy()
        except Exception as e:
            print("Error submitting income:", e)


    def build_bank_accounts_form(self):
        ctk.CTkLabel(self, text="Add Bank Account").pack(pady=10)

        self.name = ctk.CTkEntry(self, placeholder_text="Name of Bank Account", height=50, width=300)
        self.name.pack(pady=5)

        self.type = ctk.CTkEntry(self, placeholder_text="Type of Bank Account", height=50, width=300)
        self.type.pack(pady=5)

        ctk.CTkButton(self, text="Submit", command=self.submit_bank_account).pack(pady=10)
        
    def submit_bank_account(self):
        try:
            name = self.name.get()

            type = self.type.get()

            insert_bank_accounts(name, type)
            print("Transaction saved successfully.")
            if self.dashboard:
                self.dashboard.refresh_all_sections()
            self.destroy()
        except Exception as e:
            print("Error submitting income:", e)
