from datetime import datetime
import sqlite3

def init_db():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()

init_db()

def show_menu():
        print("=" * 40)
        print(" Expense Tracker ".center(40))
        print("=" * 40)

        print("1. Add Expense")
        print("2. View Expense")
        print("3. Search Expense")
        print("4. Delete Expense")
        print("5. Exit")
        print("=" * 40)

def add_expense():        
        #Date validation
        while True:
            date = input("Enter date (YYYY-MM-DD): ")
            try:
                datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please enter date in YYYY-MM-DD format.")

        # Category validation
        while True:
            category = input("Enter the category: ")
            if category.strip() == "":
                print("Category cannot be empty. Please enter a valid category.")
            else:
                break

        # Description validation
        while True:
            description = input("Enter the description: ")
            if description.strip() == "":
                print("Description cannot be empty. Please enter a valid description.")
            else:
                break

        # Amount validation
        while True:
            try:
                amount = float(input("Enter the amount for the expense: "))
                if amount <= 0:
                    print("Amount must be a positive number. Please enter a valid amount.")
                else:
                    break
            except ValueError:
                print("Invalid input for amount. Please enter a valid amount.")


        connection = sqlite3.connect("expenses.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO expenses (date, category, description, amount)
            VALUES (?, ?, ?, ?)
        """, (date, category, description, amount))

        connection.commit()
        connection.close()

        print("Expense Added Successfully")

def view_expenses():
        print("Here is your Expense:")

        connection = sqlite3.connect("expenses.db")
        cursor = connection.cursor()

        cursor.execute(""" SELECT id, date, category, description, amount FROM expenses """)
        expenses = cursor.fetchall()

        connection.close()

        if not expenses:
                print("No expenses found.")
        else:
                for expense in expenses:
                        print("-" * 40)
                        print(f"ID          : {expense[0]}")
                        print(f"Date        : {expense[1]}")
                        print(f"Category    : {expense[2]}")
                        print(f"Description : {expense[3]}")
                        print(f"Amount      : ${expense[4]:.2f}")
                        print("-" * 40)

def search_expense():
        while True:
                try:
                        search_id = int(input("Enter Expense ID for your search: "))
                        break
                except ValueError:
                        print("Invalid input. Please enter a valid Expense ID.")

        connection = sqlite3.connect("expenses.db")
        cursor = connection.cursor()

        cursor.execute("""
        SELECT id, date, category, description, amount 
        FROM expenses 
        WHERE id = ? """, (search_id,))

        expense = cursor.fetchone()

        connection.close()

        print("Search Results:")

        if expense:
                print("-" * 40)
                print(f"ID          : {expense[0]}")
                print(f"Date        : {expense[1]}")
                print(f"Category    : {expense[2]}")
                print(f"Description : {expense[3]}")
                print(f"Amount      : ${expense[4]:.2f}")
                print("-" * 40)
        else:
                print("Expense Not Found")

def delete_expense():
        while True:
                try:
                        del_expense_id = int(input("Enter Expense ID to delete the expense:"))
                except ValueError:
                        print("Invalid input. Please enter a valid Expense ID.")
                else:
                        break

        connection = sqlite3.connect("expenses.db")
        cursor = connection.cursor()

        cursor.execute("""
        DELETE FROM expenses
        WHERE ID = ?
        """, (del_expense_id,))
        connection.commit()

        if cursor.rowcount > 0:
                print("Expense Deleted Successfully")
        else:
                print("Expense Not Found")
        connection.close()

def display_expense(expense):

    print("-" * 40)
    print(f"ID          : {expense['id']}")
    print(f"Date        : {expense['date']}")
    print(f"Category    : {expense['category']}")
    print(f"Description : {expense['description']}")
    print(f"Amount      : ${expense['amount']:.2f}")
    print("-" * 40)


def main():
        while True:
                show_menu()

                try:
                        choice = int(input(("Enter your choice for the menu:")))
                except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue
                if choice == 1:
                        add_expense()

                elif choice == 2:
                        view_expenses()
                elif choice == 3:
                        search_expense()
                elif choice == 4:
                        delete_expense()
                elif choice == 5:
                        break
                else:
                        print("Invalid Choice. Please Try Again!")

main()
                