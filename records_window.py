"""Records window for the Student Budget Tracker.
Let the user view, add, edit and delete income and expense records.
Records are saved in data/records.json."""

import json
import tkinter as tk
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
            self.tree.insert("", "end", iid=record["id"], values=(record["date"], record["type"], record["amount"], record["category"], record["nature"]))
   
    def open_add_form(self):
        """Open the form for adding a new record."""
        print("Add button clicked")


if __name__ == "__main__":
    root = tk.Tk()
    app = RecordsWindow(root)
    root.mainloop()