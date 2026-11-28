import json
import re
import tkinter as tk
from tkinter import messagebox


#create a separate window for monthly budgets
class BudgetWindow(tk.Toplevel) :
    
    #set window when it open
    def __init__(self, parent):
        super().__init__(parent)
        
        #set title and size
        self.title("Monthly Budget")
        self.geometry("450x350")
        
        #store the text entered in two input fields
        self.month_var = tk.StringVar()
        self.budgt_var = tk.StringVar()

        self.create_widges()

    #create the widgets
    def create_widgets(self):

        # enter the month
        month_label = tk.Label(self, text="Month (YYYY-MM)")
        month_label.grid(row=0, column=0, padx=15, pady=10)

        month_entry = tk.Entry(self, textvariable=self.month_var)
        month_entry.grid(row=0, column=1, padx=15, pady=10)
        
        # show the selected month's budget
        show_button = tk.Button(self,text="Show",command=self.show_budget)
        show_button.grid(row=1, column=1, pady=5)

        # add label for budget input
        budget_label = tk.Label(self, text="Monthly budget (CAD)")
        budget_label.grid(row=2, column=0, padx=15, pady=10)

        # connect budget input to budget_var
        budget_entry = tk.Entry(self, textvariable=self.budget_var)
        budget_entry.grid(row=2, column=1, padx=15, pady=10)

        # check and save the budget when clicked
        save_button = tk.Button(self,text="Save budget",command=self.save_budget)
        save_button.grid(row=3, column=1, pady=5)

        # create label - show the total income
        self.income_label = tk.Label(self, text="Total income:")
        self.income_label.grid(
            row=4, column=0, columnspan=2,
            padx=15, pady=10, sticky="w"
        )

        # create a label - show the total expenses
        self.expense_label = tk.Label(self, text="Total expenses:")
        self.expense_label.grid(
            row=5, column=0, columnspan=2,
            padx=15, pady=10, sticky="w"
        )

        # create a label - show the remaining budget
        self.remaining_label = tk.Label(self, text="Remaining budget:")
        self.remaining_label.grid(
            row=6, column=0, columnspan=2,
            padx=15, pady=10, sticky="w"
        )

    # check the month is valid or not
    def check_month(self):

        # get text 
        month = self.month_var.get()

        # require four digits, a dash, and two digits
        if not re.match(r"^[0-9]{4}-[0-9]{2}$", month):
            messagebox.showerror(
                "Invalid month",
                "Please enter a month as YYYY-MM."
            )
            return False
        
        month_number = int(month[5:7])
       
        # only allow months from 1 to 12
        if month_number < 1 or month_number > 12:
            messagebox.showerror(
                "Invalid month",
                "The month must be between 01 and 12."
            )
            return False

        return True   

    # read monthly budgets from json file
    def load_budgets(self):
        with open("data/budget.json") as file:
            budgets = json.load(file)

        return budgets

    # read income and expense from json file
    def load_records(self):
        with open("data/records.json") as file:
            records = json.load(file)

        return records 
        # display the saved budget for the selected month
    
    def show_budget(self):
        # stop if the month input is invalid
        if not self.check_month():
            return

        # get selected month and saved budgets
        month = self.month_var.get()
        budgets = self.load_budgets()

        # put saved budget into budget input
        if month in budgets:
            self.budget_var.set(budgets[month])
        else:
            self.budget_var.set("")

        self.update_totals()

    # check the budget input and save
    def save_budget(self):

        # stop if the month input is invalid
        if not self.check_month():
            return

        # get text 
        budget_text = self.budget_var.get()

        # ask user to enter a budget if input is empty
        if budget_text == "":
            messagebox.showerror(
                "Missing budget",
                "Please enter a budget."
            )
            return

        # convert text to a number
        try:
            budget = float(budget_text)

        