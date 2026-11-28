import tkinter as tk
import json
from tkinter import ttk

class AnalysisWindow(tk.Toplevel):
    """Window for displaying monthly spending analysis."""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Student Budget Tracker - Analysis")
        self.geometry("800x600")
        self.minsize(650, 450)

        self.records = self.load_records()
        self.create_widgets()

    def create_widgets(self):
        # Window title
        title_label = ttk.Label(
            self, 
            text="Monthly Spending Analysis", 
            font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        # Description
        description_label = ttk.Label(
            self, 
            text="View your income, expenses, and spending habits.")
        description_label.pack(pady=5)

        # Month selection
        month_frame = ttk.Frame(self)
        month_frame.pack(pady=20)

        month_label = ttk.Label(
            month_frame,
            text="Select Month:")
        month_label.pack(side="left", padx=10)

        self.month_var = tk.StringVar(value="2026-11")

        self.month_combo = ttk.Combobox(
            month_frame,
            textvariable=self.month_var,
            values=["2026-09", "2026-10", "2026-11"],
            state="readonly",
            width=15)
        self.month_combo.pack(side="left")

        # Financial summary
        self.summary_label = ttk.Label(
            self,
            text="",
            font=("Arial", 12))
        self.summary_label.pack(pady=20)

        # Update when the selected month changes
        update_button = ttk.Button(
            month_frame,
            text="Update",
            command=self.update_summary)
        update_button.pack(side="left", padx=10)

        # Display initial summary
        self.update_summary()

    def update_summary(self):
        """Update the monthly financial summary."""

        income, expenses, balance = self.calculate_summary()

        summary_text = (
            f"Total Income: ${income:.2f}\n"
            f"Total Expenses: ${expenses:.2f}\n"
            f"Balance: ${balance:.2f}"
        )
        self.summary_label.config(text=summary_text)

    def load_records(self):
        """Load transaction records from JSON."""

        try:
            with open("data/sample.json", "r") as file:
                records = json.load(file)
                return records

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def calculate_summary(self):
        """Calculate income, expenses, and balance."""

        selected_month = self.month_var.get()

        total_income = 0
        total_expenses = 0

        for record in self.records:

            if record["date"][:7] == selected_month:
                if record["type"] == "income":
                    total_income += record["amount"]
                elif record["type"] == "expense":
                    total_expenses += record["amount"]

        balance = total_income - total_expenses

        return total_income, total_expenses, balance
    
# Run this file independently for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    window = AnalysisWindow(root)
    window.protocol("WM_DELETE_WINDOW", root.destroy)

    root.mainloop()