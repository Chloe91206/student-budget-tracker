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

    # create and arrange the widgets
    def create_widgets(self):
        # show the saved categories
        category_label = tk.Label(self, text="Categories")
        category_label.grid(row=0, column=0, columnspan=3, padx=15, pady=10)

        self.tree = ttk.Treeview(self, columns=("category",), show="headings", selectmode="browse", height=8)
        self.tree.heading("category", text="Category")
        self.tree.column("category", width=350)
        self.tree.grid(row=1, column=0, columnspan=3, padx=15, pady=5)   
        