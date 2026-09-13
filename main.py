import json
import os
from datetime import datetime


class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = []
        self.load_expenses()

    def load_expenses(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    self.expenses = json.load(file)
            except (json.JSONDecodeError, OSError):
                self.expenses = []
        else:
            self.expenses = []

    def save_expenses(self):
        try:
            with open(self.filename, "w") as file:
                json.dump(self.expenses, file, indent=4)
        except OSError:
            print("Error: Could not save expenses.")

    def add_expense(self):
        print("\n--- Add Expense ---")

        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                return

        except ValueError:
            print("Please enter a valid amount.")
            return

        category = input("Enter category: ").strip()
        description = input("Enter description: ").strip()

        if not category:
            print("Category cannot be empty.")
            return

        if not description:
            description = "No description"

        expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        self.expenses.append(expense)
        self.save_expenses()

        print("Expense added successfully.")

    def view_expenses(self):
        print("\n--- All Expenses ---")

        if not self.expenses:
            print("No expenses found.")
            return

        for index, expense in enumerate(self.expenses, start=1):
            print(
                f"{index}. "
                f"₹{expense['amount']:.2f} | "
                f"{expense['category']} | "
                f"{expense['description']} | "
                f"{expense['date']}"
            )

    def calculate_total(self):
        total = sum(expense["amount"] for expense in self.expenses)

        print(f"\nTotal Expenses: ₹{total:.2f}")

    def category_summary(self):
        print("\n--- Category Summary ---")

        if not self.expenses:
            print("No expenses found.")
            return

        summary = {}

        for expense in self.expenses:
            category = expense["category"]
            amount = expense["amount"]

            if category in summary:
                summary[category] += amount
            else:
                summary[category] = amount

        for category, amount in summary.items():
            print(f"{category}: ₹{amount:.2f}")

    def search_by_category(self):
        print("\n--- Search by Category ---")

        category = input("Enter category: ").strip().lower()

        found = False

        for expense in self.expenses:
            if expense["category"].lower() == category:
                print(
                    f"₹{expense['amount']:.2f} | "
                    f"{expense['description']} | "
                    f"{expense['date']}"
                )
                found = True

        if not found:
            print("No expenses found in this category.")

    def delete_expense(self):
        print("\n--- Delete Expense ---")

        if not self.expenses:
            print("No expenses found.")
            return

        self.view_expenses()

        try:
            choice = int(input("\nEnter expense number to delete: "))

            if choice < 1 or choice > len(self.expenses):
                print("Invalid expense number.")
                return

            deleted_expense = self.expenses.pop(choice - 1)
            self.save_expenses()

            print(
                f"Deleted: ₹{deleted_expense['amount']:.2f} "
                f"{deleted_expense['description']}"
            )

        except ValueError:
            print("Please enter a valid number.")

    def run(self):
        while True:
            print("\n==============================")
            print("       EXPENSE TRACKER")
            print("==============================")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Calculate Total")
            print("4. Category Summary")
            print("5. Search by Category")
            print("6. Delete Expense")
            print("7. Exit")
            print("==============================")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_expense()

            elif choice == "2":
                self.view_expenses()

            elif choice == "3":
                self.calculate_total()

            elif choice == "4":
                self.category_summary()

            elif choice == "5":
                self.search_by_category()

            elif choice == "6":
                self.delete_expense()

            elif choice == "7":
                print("Thank you for using Expense Tracker.")
                break

            else:
                print("Invalid choice. Please try again.")


tracker = ExpenseTracker()
tracker.run()