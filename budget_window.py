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
        show_button = tk.Button(
            self,
            text="Show",
            command=self.show_budget
        )
        show_button.grid(row=1, column=1, pady=5)