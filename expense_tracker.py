from datetime import datetime
import database

database.init_db()

def show_menu():
        print("=" * 40)
        print(" Expense Tracker ".center(40))
        print("=" * 40)

        print("1. Add Expense")
        print("2. View Expense")
        print("3. Search Expense")
        print("4. Delete Expense")
        print("5. Update Expense")
        print("6. Expense Summary")
        print("7. Exit")
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

        database.add_expense(date, category, description, amount)

def view_expenses():
        print("Here is your Expense:")

        expenses = database.get_expenses()

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

        expense = database.get_expense_by_id(search_id)

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

        deleted = database.delete_expense(del_expense_id)

        if deleted :
                print("Expense Deleted Successfully")
        else:
                print("Expense Not Found")      

def update_expense():
        print("Update Expense:")

        while True:
                try:
                        update_id = int(input("Enter Expense ID to update the expense: "))
                        break
                except ValueError:
                        print("Invalid input. Please enter a valid Expense ID.")

        expense = database.get_expense_by_id(update_id)
        if expense:
                 print("Expense Found:")
                 print(f"ID          : {expense[0]}")
                 print(f"Date        : {expense[1]}")
                 print(f"Category    : {expense[2]}")
                 print(f"Description : {expense[3]}")
                 print(f"Amount      : ${expense[4]:.2f}")

                 print("\n What would you like to update?")
                 print("1. Date")
                 print("2. Category")
                 print("3. Description")
                 print("4. Amount")

                 while True:
                        try:
                                update_choice = int(input("Enter your choice for the update: "))
                                if update_choice not in [1, 2, 3, 4]:
                                        print("Invalid choice. Please enter a number between 1 and 4.")
                                        continue
                                break
                        except ValueError:
                                print("Invalid input. Please enter a number.")

                 if update_choice == 1:
                        while True:
                                new_value = input("Enter new date (YYYY-MM-DD): ")
                                try:
                                        datetime.strptime(new_value, "%Y-%m-%d")
                                        break
                                except ValueError:
                                        print("Invalid date format. Please enter date in YYYY-MM-DD format.")

                        updated = database.update_date(update_id, new_value)
                        if updated:
                               print("Date Updated Successfully")
                        else:
                               print("Failed to update date. Please check the expense ID and try again.")

                 elif update_choice == 2:
                        while True:
                                new_value = input("Enter new category: ")
                                if new_value.strip() == "":
                                        print("Category cannot be empty. Please enter a valid category.")
                                else:
                                        break

                        updated = database.update_category(update_id, new_value)
                        if updated:
                               print("Category Updated Successfully")
                        else:
                                   print("Failed to update category. Please check the expense ID and try again.")
                
                 elif update_choice == 3:
                        while True:
                                new_value = input("Enter new description: ")
                                if new_value.strip() == "":
                                        print("Description cannot be empty. Please enter a valid description.")
                                else:
                                        break

                        updated = database.update_description(update_id, new_value)
                        if updated:
                               print("Description Updated Successfully")
                        else:
                               print("Failed to update description. Please check the expense ID and try again.")        
                 elif update_choice == 4:        
                        while True:
                                try:
                                        new_amount = float(input("Enter new amount: "))
                                        if new_amount <= 0:
                                                print("Amount must be a positive number. Please enter a valid amount.")
                                                continue
                                        break
                                except ValueError:
                                        print("Invalid input for amount. Please enter a valid amount.")
                        updated = database.update_amount(update_id, new_amount)
                        if updated:
                               print("Amount Updated Successfully")                             
                        else:
                               print("Failed to update amount. Please check the expense ID and try again.")
        else: 
                print("Expense Not Found")

def expense_summary():
        total = database.get_total_expenses()
        category_totals = database.get_expenses_by_category()

        print("=" * 40)
        print(" Expense Summary ".center(40))
        print("=" * 40)

        print(f"Total Expenses: ${total:.2f}")

        print("\nExpenses by Category:")

        for category, amount in category_totals:
                print(f"{category:<15} ${amount:.2f}")

        print("=" * 40)

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
                        update_expense()
                elif choice == 6:
                        expense_summary()
                elif choice == 7:
                        print("Exiting the program. Goodbye!")
                        break
                else:
                        print("Invalid Choice. Please Try Again!")

if __name__ == "__main__":
    main()
                