"""Records window for the Student Budget Tracker.
Let the user view, add, edit and delete income and expense records.
Records are saved in data/records.json."""

import tkinter as tk
from tkinter import ttk


class RecordsWindow(tk.Toplevel):
    """Window that shows all income and expense records in a table."""
   
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("750x450")
        self.title("Records")
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets in this window."""
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

        self.tree.column("#0", stretch=tk.NO, minwidth=0, width=0)

        self.tree.pack(expand=True, fill="both")


if __name__ == "__main__":
    root = tk.Tk()
    app = RecordsWindow(root)
    root.mainloop()

