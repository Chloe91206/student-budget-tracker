"""Records window for the Student Budget Tracker.
Let the user view, add, edit and delete income and expense records.
Records are saved in data/records.json."""

import json
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class RecordsWindow(tk.Toplevel):
    """Window that shows all income and expense records in a table."""

    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("750x450")
        self.title("Records")
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        """Create the widgets in this window."""
        # Button bar above the table
        button_bar = ttk.Frame(self)
        button_bar.pack(fill="x", padx=10, pady=5)

        add_button = ttk.Button(button_bar, text="Add", command=self.open_add_form)
        add_button.pack(side="left")

        self.tree = ttk.Treeview(self, columns=("date", "type", "amount", "category", "nature"))

        self.tree.heading("date", text="Date")
        self.tree.heading("type", text="Type")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("category", text="Category")
        self.tree.heading("nature", text="Nature")

        self.tree.column("date", width=120)
        self.tree.column("type", width=100)
        self.tree.column("amount", width=100)
        self.tree.column("category", width=160)
        self.tree.column("nature", width=140)

        # Hide the default tree column
        self.tree.column("#0", stretch=tk.NO, minwidth=0, width=0)

        self.tree.pack(expand=True, fill="both")

    def load_records(self):
        """Load records from json file."""
        with open("data/records.json") as file:
            records = json.load(file)
        return records

    def refresh_table(self):
        """Clear the table and show all records."""
        # Remove old rows before adding new ones
        for item in self.tree.get_children():
            self.tree.delete(item)

        for record in self.load_records():
            self.tree.insert("", "end", iid=record["id"],
                             values=(record["date"], record["type"],
                                     record["amount"], record["category"],
                                     record["nature"]))
                                                                  
    def open_add_form(self):
        """Open the form for adding a new record."""
        RecordForm(self)


class RecordForm(tk.Toplevel):
    """A form window for adding or editing a record."""

    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("500x350")
        self.title("Add Record")
        self.create_widgets()

    def create_widgets(self):
        """Create the input fields in the form."""
        self.date_var = tk.StringVar()
        self.amount_var = tk.StringVar()

        date_label = tk.Label(self, text="Date (YYYY-MM-DD)")
        date_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        date_entry = tk.Entry(self, width=20, textvariable=self.date_var)
        date_entry.grid(row=0, column=1, padx=10, pady=5)

        amount_label = tk.Label(self, text="Amount")
        amount_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        amount_entry = tk.Entry(self, width=20, textvariable=self.amount_var)
        amount_entry.grid(row=1, column=1, padx=10, pady=5)

        # Type: income or expense
        self.type_var = tk.StringVar()
        self.type_var.set("expense")

        type_label = tk.Label(self, text="Type")
        type_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        type_frame = tk.Frame(self)
        type_frame.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        income_radio = tk.Radiobutton(type_frame, text="Income",
                                      variable=self.type_var, value="income")
        income_radio.pack(side="left")
        expense_radio = tk.Radiobutton(type_frame,
                                       text="Expense", variable=self.type_var, value="expense")
        expense_radio.pack(side="left")

        # Category: choose from a list
        self.category_var = tk.StringVar()

        category_label = tk.Label(self, text="Category")
        category_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        categories = ["Food", "Shopping", "Transportation",
                      "Entertainment", "Education", "Other"]
        category_box = ttk.Combobox(self, textvariable=self.category_var,
                                    values=categories, state="readonly")
        category_box.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Nature: necessary, unplanned or impulse
        self.nature_var = tk.StringVar()
        self.nature_var.set("Necessary")

        nature_label = tk.Label(self, text="Nature")
        nature_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        nature_frame = tk.Frame(self)
        nature_frame.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        necessary_radio = tk.Radiobutton(nature_frame, text="Necessary",
                                         variable=self.nature_var,
                                         value="Necessary")
        necessary_radio.pack(side="left")
        unplanned_radio = tk.Radiobutton(nature_frame, text="Unplanned",
                                         variable=self.nature_var,
                                         value="Unplanned")
        unplanned_radio.pack(side="left")
        impulse_radio = tk.Radiobutton(nature_frame, text="Impulse",
                                       variable=self.nature_var,
                                       value="Impulse")
        impulse_radio.pack(side="left")

        # Save and Cancel buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)

        save_button = tk.Button(button_frame, text="Save",
                                command=self.save_record)
        save_button.pack(side="left", padx=10)
        cancel_button = tk.Button(button_frame, text="Cancel",
                                  command=self.destroy)
        cancel_button.pack(side="left", padx=10)
    
    def save_record(self):
        """Save the record when Save is clicked."""
        date = self.date_var.get()
        amount_text = self.amount_var.get()
        category = self.category_var.get()

        # Check the date format, e.g. 2026-11-24
        if not re.match(r"^[0-9]{4,4}-[0-9]{2,2}-[0-9]{2,2}$", date):
            messagebox.showerror("Invalid date",
                                 "Please enter the date as YYYY-MM-DD.")
            return

        # Check the amount is a positive number
        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Invalid amount",
                                 "Please enter a number for the amount.")
            return
        if amount <= 0:
            messagebox.showerror("Invalid amount",
                                 "The amount must be more than 0.")
            return

        # Check a category was chosen
        if category == "":
            messagebox.showerror("Missing category",
                                 "Please choose a category.")
            return

        print("All good:", date, amount, category)

if __name__ == "__main__":
    root = tk.Tk()
    app = RecordsWindow(root)
    root.mainloop()