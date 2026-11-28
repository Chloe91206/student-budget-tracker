import tkinter as tk
from tkinter import ttk

class AnalysisWindow(tk.Toplevel):
    """Window for displaying monthly spending analysis."""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Student Budget Tracker - Analysis")
        self.geometry("800x600")
        self.minsize(650, 450)

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

        self.month_var = tk.StringVar(value="2026-11")

        self.month_combo = ttk.Combobox(
            month_frame,
            textvariable=self.month_var,
            values=["2026-09", "2026-10", "2026-11"],
            state="readonly",
            width=15)
        self.month_combo.pack(side="left")

# Run this file independently for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    window = AnalysisWindow(root)
    window.protocol("WM_DELETE_WINDOW", root.destroy)

    root.mainloop()