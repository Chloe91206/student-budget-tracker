import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# create the category window
class CategoryWindow(tk.Toplevel):

    # set up window
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Category Management")
        self.geometry("450x400")

        self.name_var = tk.StringVar()

        # add starting categories
        categories = self.load_categories()

        if len(categories) == 0:
            categories = ["Food", "Shopping", "Transportation", "Entertainment", "Education", "Other"]
            self.save_categories(categories)

        self.create_widgets()
        self.refresh_categories()