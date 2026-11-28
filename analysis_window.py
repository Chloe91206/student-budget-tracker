import tinker as tk
from tinker import ttk

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

        