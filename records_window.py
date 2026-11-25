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
        self.create_menu()
        self.refresh_table()

    def create_widgets(self):
        """Create the widgets in this window."""
        # Button bar above the table
        button_bar = ttk.Frame(self)
        button_bar.pack(fill="x", padx=10, pady=5)

        add_button = ttk.Button(button_bar, text="Add", command=self.open_add_form)
        add_button.pack(side="left")
        delete_button = ttk.Button(button_bar, text="Delete",
                                   command=self.delete_record)
        delete_button.pack(side="left", padx=5)

        # Choose a month, then click Show to filter the table
        self.month_var = tk.StringVar()
        self.month_var.set("All")
        show_button = ttk.Button(button_bar, text="Show",
                                 command=self.refresh_table)
        show_button.pack(side="right")
        self.month_box = ttk.Combobox(button_bar, textvariable=self.month_var,
                                      state="readonly", width=10)
        self.month_box.pack(side="right", padx=5)
        month_label = ttk.Label(button_bar, text="Month:")
        month_label.pack(side="right")

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

        # Double-click a row to edit it
        self.tree.bind("<Double-1>", self.open_edit_form)

    def create_menu(self):
        """Create the menu bar and keyboard shortcuts."""
        menubar = tk.Menu(self)
        records_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Records", menu=records_menu)

        records_menu.add_command(label="Add", command=self.open_add_form,
                                 accelerator="Ctrl+N")
        records_menu.add_command(label="Delete", command=self.delete_record,
                                 accelerator="Ctrl+D")
        records_menu.add_separator()
        records_menu.add_command(label="Close", command=self.destroy)
        self.config(menu=menubar)

        # Keyboard shortcuts
        self.bind("<Control-n>", lambda e: self.open_add_form())
        self.bind("<Control-d>", lambda e: self.delete_record()	)
        
    def load_records(self):
        """Load records from JSON file."""
        with open("data/records.json") as file:
            records = json.load(file)
        return records

    def refresh_table(self):
        """Clear the table and show all records for chosen month."""
        # Remove old rows before adding new ones
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = self.load_records()
        month = self.month_var.get()

        # Build the month list
        months = ["All"]
        for record in records:
            record_month = record["date"][0:7]
            if record_month not in months:
                months.append(record_month)
        self.month_box.config(values=months)

        # Only show records from the chosen month
        for record in records:
            if month == "All" or record["date"][0:7] == month:
                self.tree.insert("", "end", iid=record["id"],
                             values=(record["date"], record["type"],
                                     record["amount"], record["category"],
                                     record["nature"]))

    def open_edit_form(self, event):
        """Open the form to edit the record that was double-clicked."""
        selected = self.tree.selection()
        # Stop if no row was clicked
        if len(selected) == 0:
            return

        record_id = int(selected[0])
        for record in self.load_records():
            if record["id"] == record_id:
                RecordForm(self, record)
                                                                  
    def open_add_form(self):
        """Open the form for adding a new record."""
        RecordForm(self)

    def delete_record(self):
        """Delete the selected record after asking the user."""
        selected = self.tree.selection()
        # Stop if no row is selected
        if len(selected) == 0:
            messagebox.showinfo("No record selected",
                                "Please click a record first.")
            return

        # Ask before deleting
        sure = messagebox.askyesno("Delete record",
                                   "Delete this record?")
        if not sure:
            return

        # Keep every record except the one to delete
        record_id = int(selected[0])
        new_records = []
        for record in self.load_records():
            if record["id"] != record_id:
                new_records.append(record)

        with open("data/records.json", "w") as file:
            json.dump(new_records, file)

        self.refresh_table()


class RecordForm(tk.Toplevel):
    """A form window for adding or editing a record."""

    def __init__(self, parent, record=None):
        super().__init__(parent)
        self.parent = parent
        self.record = record

        self.geometry("500x350")
        if self.record is None:
            self.title("Add Record")
        else:
            self.title("Edit Record")
        self.create_widgets()

        # Fill in the form when editing
        if self.record is not None:
            self.date_var.set(self.record["date"])
            self.amount_var.set(self.record["amount"])
            self.type_var.set(self.record["type"])
            self.category_var.set(self.record["category"])
            self.nature_var.set(self.record["nature"])

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

        # Load all records, add the new one, then write them all back
        records = self.parent.load_records()
        if self.record is None:
            # Give the new record the next id number
            new_id = 1
            for record in records:
                if record["id"] >= new_id:
                    new_id = record["id"] + 1

            new_record = {"id": new_id,
                      "date": date,
                      "type": self.type_var.get(),
                      "amount": amount,
                      "category": category,
                      "nature": self.nature_var.get()}
            records.append(new_record)
        else:
            # Editing: find the record with the same id and change it
            for record in records:
                if record["id"] == self.record["id"]:
                    record["date"] = date
                    record["type"] = self.type_var.get()
                    record["amount"] = amount
                    record["category"] = category
                    record["nature"] = self.nature_var.get()

        with open("data/records.json", "w") as file:
            json.dump(records, file)

        # Show the new record in the table and close the form
        self.parent.refresh_table()
        self.destroy()
        

if __name__ == "__main__":
    root = tk.Tk()
    app = RecordsWindow(root)
    root.mainloop()