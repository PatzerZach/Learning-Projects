import customtkinter as ctk
from tkinter import ttk
from tkinter import Scrollbar
from models.income import get_income_by_filter, get_all_income
from models.transactions import get_transactions_by_filter, get_all_transactions
from models.investments import get_investments_by_filter, get_all_investments
from models.assets_income_sources import get_assets_income_sources_by_filter, get_all_assets_income
from models.stocks import get_all_stocks
from models.credit_cards import get_all_credit_cards, get_all_perks
from models.banks import get_all_banks


# ******** Make it so that the category filters you can type in a word to filter instead of just ascending  vs descending



def style_treeview():
    style = ttk.Style()
    style.theme_use("default")
    
    style.configure("Treeview",
        background="#1a1a1a",
        foreground="white",
        rowheight=25,
        fieldbackground="#1a1a1a",
        font=("Segoe UI", 12),
        bordercolor="#333333",
        borderwidth=0
    )
    
    style.configure("Treeview.Heading",
        font=("Segoe UI", 12, "bold"),
        background="#222222",
        foreground="white"
    )
    
    style.map("Treeview",
        background=[('selected', '#2a2a2a')],
        foreground=[('selected', 'white')]
    )


class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid(row=0, column=0, sticky="nsew")
        
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        style_treeview()
        
        self.create_income_section()
        self.create_stock_section()
        self.create_transactions_section()
        self.create_investments_section()
        self.create_credit_cards_section()
        self.create_credit_cards_perk_section()
        self.create_bank_accounts_section()
        self.create_assets_income_sources_section()
        
    def open_popup(self, form_type):
        from ui.popups import PopupForm
        PopupForm(self.master, form_type, dashboard_ref=self)
    
    def create_section_frame(self, title, show_add_button=False, form_type=None, filter_options=None, on_filter_change=None):
        frame = ctk.CTkFrame(self, corner_radius = 10)
        
        top_row = ctk.CTkFrame(frame, fg_color="transparent")
        top_row.pack(fill="x", padx=10, pady=(5, 0))
        
        top_row.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(top_row, text=title, font=("Segoe UI", 18, "bold"))
        label.grid(row=0, column=0, sticky="n")
        
        if filter_options:
            filter_menu = ctk.CTkOptionMenu(top_row, values=filter_options, width=120, bg_color="transparent", command=on_filter_change if on_filter_change else lambda val: print(f"Filter: {val}"))
            filter_menu.grid(row=0, column=1, padx=(10, 0))
        
        if show_add_button and form_type:
            add_button = ctk.CTkButton(top_row, text="+", width=75, height=20, font=("Segoe UI", 20, "bold"), corner_radius=5, anchor="center", command=lambda: self.open_popup(form_type))
            add_button.grid(row=0, column=2, padx=(10, 0))
        
        return frame
    
    def add_table_to_frame(self, frame, columns):
        container = ctk.CTkFrame(frame, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=10, pady=5)
        
        tree = ttk.Treeview(container, columns=columns, show="headings")
        #tree.column("#0", width=0, stretch=False)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)
            
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview, style="Vertical.TScrollbar")
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        
        def show_scrollbar(event=None):
            scrollbar.pack(side="right", fill="y")
        
        def hide_scrollbar(event=None):
            scrollbar.pack_forget()
            
        tree.bind("<Enter>", show_scrollbar)
        tree.bind("<Leave>", hide_scrollbar)
        container.bind("<Enter>", show_scrollbar)
        container.bind("<Leave>", hide_scrollbar)
        
        return tree
    
    def on_income_filter(self, selected):
        filtered_data = get_income_by_filter(selected)
        self.update_treeview(self.income_tree, filtered_data)
    
    def on_transactions_filter(self, selected):
        filtered_data = get_transactions_by_filter(selected)
        self.update_treeview(self.transactions_tree, filtered_data)
        
    def on_investments_filter(self, selected):
        filtered_data = get_investments_by_filter(selected)
        self.update_treeview(self.investments_tree, filtered_data)
        
    def on_assets_income_sources_filter(self, selected):
        filtered_data = get_assets_income_sources_by_filter(selected)
        self.update_treeview(self.assets_income_tree, filtered_data)
    
    def update_treeview(self, tree, new_data):
        tree.delete(*tree.get_children())
        for row in new_data:
            tree.insert("", "end", values=row)
    
    def create_income_section(self):
        frame = self.create_section_frame("Income", show_add_button=True, form_type="income", filter_options=["Date Desc", "Date Asc", "Amount Asc", "Amount Desc", "Source Asc", "Source Desc"], on_filter_change=self.on_income_filter)
        frame.grid(row=0, column=0, rowspan=4, padx=30, pady=20, sticky="nsew")
        self.income_tree = self.add_table_to_frame(frame, columns=["Date", "Source", "Amount", "Account", "Asset", "Recurring"])
        data = get_all_income()
        for row in data:
            self.income_tree.insert("", "end", values=row[1:])
    
    def create_stock_section(self):
        frame = self.create_section_frame("Stocks", show_add_button=True, form_type="stocks")
        frame.grid(row=4, column=0, rowspan=2, padx=30, pady=20, sticky="nsew")
        self.stock_tree = self.add_table_to_frame(frame, columns=["Symbol", "Shares", "Value"])
        data = get_all_stocks()
        for row in data:
            self.stock_tree.insert("", "end", values=row[1:])
    
    def create_transactions_section(self):
        frame = self.create_section_frame("Transactions", show_add_button=True, form_type="transactions", filter_options=["Date Desc", "Date Asc", "Amount Asc", "Amount Desc", "Category Asc", "Category Desc", "Account Asc", "Account Desc"], on_filter_change=self.on_transactions_filter)
        frame.grid(row=0, column=1, rowspan=4, columnspan=2, padx=30, pady=20, sticky="nsew")
        self.transactions_tree = self.add_table_to_frame(frame, columns=["Date", "Amount", "Category", "Account", "Payment Method", "Type", "Notes"])
        data = get_all_transactions()
        for row in data:
            self.transactions_tree.insert("", "end", values=row[1:])
    
    def create_investments_section(self):
        frame = self.create_section_frame("Investments / Investment Accounts", show_add_button=True, form_type="investments", filter_options=["Name Desc", "Name Asc", "Type Asc", "Type Desc", "Details Asc", "Details Desc"], on_filter_change=self.on_investments_filter)
        frame.grid(row=4, column=1, rowspan=2, columnspan=2, padx=30, pady=20, sticky="nsew")
        self.investments_tree = self.add_table_to_frame(frame, columns=["Name", "Type", "Details"])
        data = get_all_investments()
        for row in data:
            self.investments_tree.insert("", "end", values=row)
    
    def create_credit_cards_section(self):
        frame = self.create_section_frame("Credit Cards", show_add_button=True, form_type="credit_cards")
        frame.grid(row=0, column=3, padx=30, pady=20, sticky="nsew")
        self.credit_cards_tree = self.add_table_to_frame(frame, columns=["Card", "Cash Back Category", "Cash Back Rates"])
        data = get_all_credit_cards()
        for row in data:
            self.credit_cards_tree.insert("", "end", values=row[1:])
    
    def create_credit_cards_perk_section(self):
        frame = self.create_section_frame("Credit Card Perks")
        frame.grid(row=1, column=3, rowspan=2, padx=30, pady=20, sticky="nsew")
        self.credit_card_perks = self.add_table_to_frame(frame, columns=["Card", "Category", "Rate"])
        data = get_all_perks()
        for row in data:
            self.credit_card_perks.insert("", "end", values=row)
    
    def create_assets_income_sources_section(self):
        frame = self.create_section_frame("Assests / Income Sources", show_add_button=True, form_type="assets", filter_options=["Name Desc", "Name Asc", "Type Asc", "Type Desc"], on_filter_change=self.on_assets_income_sources_filter)
        frame.grid(row=3, column=3, rowspan=2, padx=30, pady=20, sticky="nsew")
        self.assets_income_tree = self.add_table_to_frame(frame, columns=["Name", "Type", "Details"])
        data = get_all_assets_income()
        for row in data:
            self.assets_income_tree.insert("", "end", values=row[1:])
    
    def create_bank_accounts_section(self):
        frame = self.create_section_frame("Bank Accounts", show_add_button=True, form_type="bank_accounts")
        frame.grid(row=5, column=3, padx=30, pady=20, sticky="nsew")
        self.bank_tree = self.add_table_to_frame(frame, columns=["Account", "Type"])
        data = get_all_banks()
        for row in data:
            self.bank_tree.insert("", "end", values=row[1:])
    
    def refresh_all_sections(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        self.create_income_section()
        self.create_stock_section()
        self.create_transactions_section()
        self.create_investments_section()
        self.create_credit_cards_section()
        self.create_credit_cards_perk_section()
        self.create_bank_accounts_section()
        self.create_assets_income_sources_section()
    

def launch_dashboard():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = ctk.CTk()
    app.title("Finance Tracker")
    #app.state("zoomed")
    
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)
    
    Dashboard(app)
    
    app.after(10, lambda: app.state("zoomed"))
    app.mainloop()