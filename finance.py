import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv
import matplotlib.pyplot as plt


rupee = "\u20B9"

class FinanceTracker:
    def __init__(self):
        self.data = {
            "income": [],
            "expenses": [],
            "savings": 0,
            "budget": 0
        }
        if self.check_file_exists():
            self.load_data()

    def check_file_exists(self):
        try:
            with open("finance_data.csv", "r"):
                return True
        except FileNotFoundError:
            return False

    def get_expense_summary_by_description(self):
        expense_summary = {}
        for expense in self.data["expenses"]:
            description = expense["description"]
            amount = expense["amount"]
            if description in expense_summary:
                expense_summary[description] += amount
            else:
                expense_summary[description] = amount
        return expense_summary

    def load_data(self):
        try:
            with open("finance_data.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    item = {
                        "amount": float(row["amount"]),
                        "description": row["description"],
                        "date": row["date"]
                    }
                    if row["type"] == "income" and item not in self.data["income"]:
                        self.data["income"].append(item)
                    elif row["type"] == "expense" and item not in self.data["expenses"]:
                        self.data["expenses"].append(item)
        except FileNotFoundError:
            pass

    def save_data(self):
        with open("finance_data.csv", "w", newline='') as file:
            fieldnames = ["type", "amount", "description", "date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for income in self.data["income"]:
                writer.writerow({
                    "type": "income",
                    "amount": income["amount"],
                    "description": income["description"],
                    "date": income["date"]
                })
            for expense in self.data["expenses"]:
                writer.writerow({
                    "type": "expense",
                    "amount": expense["amount"],
                    "description": expense["description"],
                    "date": expense["date"]
                })

    def delete_all_data(self):
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete all data? This action cannot be undone.")
        if confirmation:
            self.data = {
                "income": [],
                "expenses": [],
                "savings": 0,
                "budget": 0
            }
            self.save_data()
            messagebox.showinfo("Success", "All data has been deleted.")
        else:
            messagebox.showinfo("Deletion Canceled", "Deletion canceled.")

    def record_income(self, amount, description):
        date = datetime.now().strftime("%Y-%m-%d")
        self.data["income"].append({
            "amount": amount,
            "description": description,
            "date": date
        })
        self.save_data()
        messagebox.showinfo("Success", "Income recorded successfully.")

    def record_expense(self, amount, description):
        date = datetime.now().strftime("%Y-%m-%d")
        self.data["expenses"].append({
            "amount": amount,
            "description": description,
            "date": date
        })
        self.save_data()
        messagebox.showinfo("Success", "Expense recorded successfully.")

    def edit_income(self, date, new_amount, new_description):
        for income in self.data["income"]:
            if income["date"] == date:
                income["amount"] = new_amount
                income["description"] = new_description
                self.save_data()
                messagebox.showinfo("Success", "Income record edited successfully.")
                return
        messagebox.showwarning("Warning", f"Income record for date {date} not found.")

    def edit_expense(self, date, new_amount, new_description):
        for expense in self.data["expenses"]:
            if expense["date"] == date:
                expense["amount"] = new_amount
                expense["description"] = new_description
                self.save_data()
                messagebox.showinfo("Success", "Expense record edited successfully.")
                return
        messagebox.showwarning("Warning", f"Expense record for date {date} not found.")

    def view_summary(self):
        summary = "\nFinancial Summary:\n"
        if not self.data["income"] and not self.data["expenses"]:
            summary += "Start spending to have a record...\n"
        else:
            summary += "Income:\n"
            for income in self.data["income"]:
                summary += f"{income['date']} - {income['description']}: {rupee}{income['amount']}\n"

            summary += "\nExpenses:\n"
            for expense in self.data["expenses"]:
                summary += f"{expense['date']} - {expense['description']}: {rupee}{expense['amount']}\n"

            total_income = sum(income["amount"] for income in self.data["income"])
            total_expenses = sum(expense["amount"] for expense in self.data["expenses"])

            current_budget = total_income - total_expenses
            self.data["savings"] += current_budget

            summary += f"\nTotal Income: {rupee}{total_income}\n"
            summary += f"Total Expenses: {rupee}{total_expenses}\n"
            summary += f"Budget: {rupee}{current_budget}\n"

            if current_budget > 4000:
                summary += "Safe spending pattern, can splurge more :)\n"
            elif 1000 <= current_budget <= 4000:
                summary += "Have adequate balance.\n"
            elif current_budget < 1000:
                summary += "Spend carefully :(\n"

        messagebox.showinfo("Financial Summary", summary)


class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.finance_tracker = FinanceTracker()
        self.create_widgets()  # Call create_widgets method to create GUI elements

    def create_widgets(self):
        # Set window size
        self.root.geometry("330x600")  # Set the initial size of the window to 330x600 pixels

        # Income widgets
        self.income_amount_label = tk.Label(self.root, text="Income Amount:")
        self.income_amount_entry = tk.Entry(self.root)
        self.income_description_label = tk.Label(self.root, text="Income Description:")
        self.income_description_entry = tk.Entry(self.root)
        self.income_button = tk.Button(self.root, text="Record Income", command=self.record_income)

        # Layout Income widgets with proper spacing
        self.income_amount_label.grid(row=0, column=0, padx=10, pady=5)
        self.income_amount_entry.grid(row=0, column=1, padx=10, pady=5)
        self.income_description_label.grid(row=1, column=0, padx=10, pady=5)
        self.income_description_entry.grid(row=1, column=1, padx=10, pady=5)
        self.income_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Expense widgets
        self.expense_amount_label = tk.Label(self.root, text="Expense Amount:")
        self.expense_amount_entry = tk.Entry(self.root)
        self.expense_description_label = tk.Label(self.root, text="Expense Description:")
        self.expense_description_entry = tk.Entry(self.root)
        self.expense_button = tk.Button(self.root, text="Record Expense", command=self.record_expense)

        # Layout Expense widgets with proper spacing
        self.expense_amount_label.grid(row=3, column=0, padx=10, pady=5)
        self.expense_amount_entry.grid(row=3, column=1, padx=10, pady=5)
        self.expense_description_label.grid(row=4, column=0, padx=10, pady=5)
        self.expense_description_entry.grid(row=4, column=1, padx=10, pady=5)
        self.expense_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Edit Income widgets
        self.edit_income_date_label = tk.Label(self.root, text="Edit Income Date:")
        self.edit_income_date_entry = tk.Entry(self.root)
        self.edit_income_amount_label = tk.Label(self.root, text="Edit Income Amount:")
        self.edit_income_amount_entry = tk.Entry(self.root)
        self.edit_income_description_label = tk.Label(self.root, text="Edit Income Description:")
        self.edit_income_description_entry = tk.Entry(self.root)
        self.save_edit_income_button = tk.Button(self.root, text="Edit Income", command=self.save_edit_income)

        # Layout Edit Income widgets with proper spacing
        self.edit_income_date_label.grid(row=6, column=0, padx=10, pady=5)
        self.edit_income_date_entry.grid(row=6, column=1, padx=10, pady=5)
        self.edit_income_amount_label.grid(row=7, column=0, padx=10, pady=5)
        self.edit_income_amount_entry.grid(row=7, column=1, padx=10, pady=5)
        self.edit_income_description_label.grid(row=8, column=0, padx=10, pady=5)
        self.edit_income_description_entry.grid(row=8, column=1, padx=10, pady=5)
        self.save_edit_income_button.grid(row=9, column=0, columnspan=2, pady=10)

        # Edit Expense widgets
        self.edit_expense_date_label = tk.Label(self.root, text="Edit Expense Date:")
        self.edit_expense_date_entry = tk.Entry(self.root)
        self.edit_expense_amount_label = tk.Label(self.root, text="Edit Expense Amount:")
        self.edit_expense_amount_entry = tk.Entry(self.root)
        self.edit_expense_description_label = tk.Label(self.root, text="Edit Expense Description:")
        self.edit_expense_description_entry = tk.Entry(self.root)
        self.save_edit_expense_button = tk.Button(self.root, text="Edit Expense", command=self.save_edit_expense)

        # Layout Edit Expense widgets with proper spacing
        self.edit_expense_date_label.grid(row=10, column=0, padx=10, pady=5)
        self.edit_expense_date_entry.grid(row=10, column=1, padx=10, pady=5)
        self.edit_expense_amount_label.grid(row=11, column=0, padx=10, pady=5)
        self.edit_expense_amount_entry.grid(row=11, column=1, padx=10, pady=5)
        self.edit_expense_description_label.grid(row=12, column=0, padx=10, pady=5)
        self.edit_expense_description_entry.grid(row=12, column=1, padx=10, pady=5)
        self.save_edit_expense_button.grid(row=13, column=0, columnspan=2, pady=10)

        # View Summary and Delete Data buttons
        self.view_summary_button = tk.Button(self.root, text="View Summary", command=self.view_summary)
        self.view_summary_button.grid(row=14, column=0, padx=10, pady=10, sticky="we")

        self.delete_data_button = tk.Button(self.root, text="Delete All Data", command=self.delete_all_data)
        self.delete_data_button.grid(row=14, column=1, padx=10, pady=10, sticky="we")

        # Pie Chart button
        self.pie_chart_button = tk.Button(self.root, text="Show Expense Pie Chart", command=self.show_expense_pie_chart)
        self.pie_chart_button.grid(row=15, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    def show_expense_pie_chart(self):
        expense_summary = self.finance_tracker.get_expense_summary_by_description()
        labels = list(expense_summary.keys())
        values = list(expense_summary.values())

        plt.figure(figsize=(8, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Expense Distribution')
        fig_manager = plt.get_current_fig_manager()
        fig_manager.set_window_title('Expense Report')
        plt.show()

    def record_income(self):
        amount = float(self.income_amount_entry.get())
        description = self.income_description_entry.get()
        self.finance_tracker.record_income(amount, description)

    def record_expense(self):
        amount = float(self.expense_amount_entry.get())
        description = self.expense_description_entry.get()
        self.finance_tracker.record_expense(amount, description)

    def save_edit_income(self):
        date = self.edit_income_date_entry.get()
        new_amount = float(self.edit_income_amount_entry.get())
        new_description = self.edit_income_description_entry.get()
        self.finance_tracker.edit_income(date, new_amount, new_description)
        self.view_summary()

    def save_edit_expense(self):
        date = self.edit_expense_date_entry.get()
        new_amount = float(self.edit_expense_amount_entry.get())
        new_description = self.edit_expense_description_entry.get()
        self.finance_tracker.edit_expense(date, new_amount, new_description)
        self.view_summary()

    def view_summary(self):
        self.finance_tracker.view_summary()

    def delete_all_data(self):
        self.finance_tracker.delete_all_data()


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    root.mainloop()
