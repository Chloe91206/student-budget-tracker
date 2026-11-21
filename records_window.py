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


if __name__ == "__main__":
    root = tk.Tk()
    app = RecordsWindow(root)
    root.mainloop()

