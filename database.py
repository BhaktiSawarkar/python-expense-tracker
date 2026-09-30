import sqlite3

def get_connection():
    return sqlite3.connect("expenses.db")

def init_db():
    connection = get_connection()
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

def add_expense(date, category, description, amount):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO expenses (date, category, description, amount)
            VALUES (?, ?, ?, ?)
        """, (date, category, description, amount))

        connection.commit()

    except sqlite3.Error as error:
        connection.rollback()
        print("Database error:", error)

    finally:
        connection.close()

def get_expenses():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id, date, category, description, amount
            FROM expenses
        """)

        expenses = cursor.fetchall()
        return expenses

    except sqlite3.Error as error:
        print("Database error:", error)
        return []

    finally:
        connection.close()

def get_expense_by_id(expense_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id, date, category, description, amount
            FROM expenses
            WHERE id = ?
        """, (expense_id,))

        expense = cursor.fetchone()
        return expense

    except sqlite3.Error as error:
        print("Database error:", error)
        return None

    finally:
        connection.close()

def delete_expense(expense_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM expenses
            WHERE id = ?
        """, (expense_id,))

        connection.commit()

        deleted = cursor.rowcount > 0
        return deleted

    except sqlite3.Error as error:
        connection.rollback()
        print("Database error:", error)
        return False

    finally:
        connection.close()

def update_date(expense_id, new_date):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE expenses
            SET date = ?
            WHERE id = ?
        """, (new_date, expense_id))

        connection.commit()

        updated = cursor.rowcount > 0
        return updated

    except sqlite3.Error as error:
        connection.rollback()
        print("Database error:", error)
        return False

    finally:
        connection.close()

def update_category(expense_id, new_category):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE expenses
            SET category = ?
            WHERE id = ?
        """, (new_category, expense_id))

        connection.commit()

        updated = cursor.rowcount > 0
        return updated

    except sqlite3.Error as error:
        connection.rollback()
        print("Database error:", error)
        return False

    finally:
        connection.close()

def update_description(expense_id, new_description):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE expenses
            SET description = ?
            WHERE id = ?
        """, (new_description, expense_id))

        connection.commit()

        updated = cursor.rowcount > 0
        return updated

    except sqlite3.Error as error:
        connection.rollback()
        print("Database error:", error)
        return False

    finally:
        connection.close()

def update_amount(expense_id, new_amount):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE expenses
            SET amount = ?
            WHERE id = ?
        """, (new_amount, expense_id))

        connection.commit()

        updated = cursor.rowcount > 0
        return updated

    except sqlite3.Error as error:
        connection.rollback()
        print("Database error:", error)
        return False

    finally:
        connection.close()

def get_total_expenses():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
        """)

        total = cursor.fetchone()[0]

        if total is None:
            total = 0

        return total

    except sqlite3.Error as error:
        print("Database error:", error)
        return 0

    finally:
        connection.close()

def get_expenses_by_category():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            GROUP BY category
        """)

        category_totals = cursor.fetchall()
        return category_totals

    except sqlite3.Error as error:
        print("Database error:", error)
        return []

    finally:
        connection.close()