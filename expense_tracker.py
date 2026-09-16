from datetime import datetime
import json

def save_expenses():
      with open("expenses.json", "w") as file:
            json.dump(expenses, file, indent=4)

def load_expenses():
      try:
        with open("expenses.json", "r") as file:
                  return json.load(file)
      except FileNotFoundError:
            return []


expenses = load_expenses() 
if expenses:
    next_expense_id = max(expense["id"] for expense in expenses) + 1
else:
        next_expense_id = 1 


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
        global next_expense_id

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
                      

        expense = {
                "id" : next_expense_id,
                "date" : date,
                "category" : category,
                "description" : description,
                "amount" : amount
        }

        expenses.append(expense)

        save_expenses()

        print("Expense Added Succesfully")

        next_expense_id += 1  

def view_expenses():
        print("Here is your Expense:")
        if not expenses:
                print("No expenses found.")
        else:
                for item in expenses:
                        display_expense(item)

def search_expense():
        try:
              
                search_id = int(input("Enter Expense ID for your search:"))
        except ValueError:
                print("Invalid input. Please enter a valid Expense ID.")

        found = False
        print("Search Results :")
        for item in expenses:
                if search_id == item["id"]:
                        display_expense(item)
                        found = True
                        break
        
        if not found:
                print("Expense Not Found")
        
def delete_expense():
        while True:
                try:
                        del_expense_id = int(input("Enter Expense ID to delete the expense:"))
                except ValueError:
                        print("Invalid input. Please enter a valid Expense ID.")
                else:
                        break

        found = False
        for item in expenses:
                if del_expense_id == item["id"]:
                        found = True
                        expenses.remove(item)
                        save_expenses()
                        print("Expense deleted successfully.")
                        break

        if not found:
                print("Expense not found")

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
                