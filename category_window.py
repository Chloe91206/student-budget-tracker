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

        # enter a category name
        name_label = tk.Label(self, text="Category name")
        name_label.grid(row=2, column=0, padx=15, pady=10)

        name_entry = tk.Entry(self, textvariable=self.name_var)
        name_entry.grid(row=2, column=1, columnspan=2, padx=15, pady=10)

        # add a new category
        add_button = tk.Button(self, text="Add", command=self.add_category)
        add_button.grid(row=3, column=0, padx=10, pady=10)

        # rename the selected category
        rename_button = tk.Button(self, text="Rename", command=self.rename_category)
        rename_button.grid(row=3, column=1, padx=10, pady=10)

        # delete the selected category
        delete_button = tk.Button(self, text="Delete", command=self.delete_category)
        delete_button.grid(row=3, column=2, padx=10, pady=10)

    # read saved categories
    def load_categories(self):
        with open("data/categories.json") as file:
            categories = json.load(file)

        return categories

    # save category list
    def save_categories(self, categories):
        with open("data/categories.json", "w") as file:
            json.dump(categories, file)

    # read saved records
    def load_records(self):
        with open("data/records.json") as file:
            records = json.load(file)

        return records
    
    # refresh category list
    def refresh_categories(self):

        # remove the old rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # show each saved category
        categories = self.load_categories()
        for category in categories:
            self.tree.insert("", "end", iid=category, values=(category,))

    # add a new category
    def add_category(self):
        name = self.name_var.get()

        #ask for a category name
        if name == "":
            messagebox.showerror("Missing name", "Please enter a category name.")
            return

        categories = self.load_categories()

        # reject an existing name
        if name in categories:
            messagebox.showerror("Duplicate category", "This category already exists.")
            return

        # save and display the new category
        categories.append(name)
        self.save_categories(categories)
        self.refresh_categories()
        self.name_var.set("")