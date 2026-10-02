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


def get_valid_date():
    while True:
        date = input("Enter date (YYYY-MM-DD): ")

        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date

        except ValueError:
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")


def get_valid_category():
    while True:
        category = input("Enter the category: ")

        if category.strip() == "":
            print("Category cannot be empty. Please enter a valid category.")
        else:
            return category


def get_valid_description():
    while True:
        description = input("Enter the description: ")

        if description.strip() == "":
            print("Description cannot be empty. Please enter a valid description.")
        else:
            return description


def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter the amount for the expense: "))

            if amount <= 0:
                print("Amount must be a positive number. Please enter a valid amount.")
            else:
                return amount

        except ValueError:
            print("Invalid input for amount. Please enter a valid amount.")


def add_expense():
    # Date validation
    date = get_valid_date()

    # Category validation
    category = get_valid_category()

    # Description validation
    description = get_valid_description()

    # Amount validation
    amount = get_valid_amount()

    database.add_expense(date, category, description, amount)


def display_expense(expense):
    print("-" * 40)
    print(f"ID          : {expense[0]}")
    print(f"Date        : {expense[1]}")
    print(f"Category    : {expense[2]}")
    print(f"Description : {expense[3]}")
    print(f"Amount      : ${expense[4]:.2f}")
    print("-" * 40)


def view_expenses():
    print("Here is your Expense:")

    expenses = database.get_expenses()

    if not expenses:
        print("No expenses found.")
    else:
        for expense in expenses:
            display_expense(expense)


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
        display_expense(expense)
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

    if deleted:
        print("Expense Deleted Successfully")
    else:
        print("Expense Not Found")


def get_update_choice():
    while True:
        try:
            update_choice = int(input("Enter your choice for the update: "))

            if update_choice not in [1, 2, 3, 4]:
                print("Invalid choice. Please enter a number between 1 and 4.")
                continue

            return update_choice

        except ValueError:
            print("Invalid input. Please enter a number.")


def display_update_result(updated, field_name):
    if updated:
        print(f"{field_name} Updated Successfully")
    else:
        print(
            f"Failed to update {field_name.lower()}. "
            "Please check the expense ID and try again."
        )


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
        display_expense(expense)
        print("\n What would you like to update?")
        print("1. Date")
        print("2. Category")
        print("3. Description")
        print("4. Amount")

        update_choice = get_update_choice()

        if update_choice == 1:
            new_value = get_valid_date()
            updated = database.update_date(update_id, new_value)
            display_update_result(updated, "Date")

        elif update_choice == 2:
            new_value = get_valid_category()
            updated = database.update_category(update_id, new_value)
            display_update_result(updated, "Category")

        elif update_choice == 3:
            new_value = get_valid_description()
            updated = database.update_description(update_id, new_value)
            display_update_result(updated, "Description")

        elif update_choice == 4:
            new_value = get_valid_amount()
            updated = database.update_amount(update_id, new_value)
            display_update_result(updated, "Amount")
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
