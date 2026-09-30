import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

import database

@pytest.fixture
def test_database():
    original_database = database.DATABASE_NAME

    database.DATABASE_NAME = "test_expenses.db"

    Path("test_expenses.db").unlink(missing_ok=True)

    database.init_db()

    yield

    database.DATABASE_NAME = original_database
    Path("test_expenses.db").unlink(missing_ok=True)

    

def test_add_expense(test_database):
    database.add_expense(
        "2026-09-29",
        "Food",
        "Lunch",
        15.50
    )

    expense = database.get_expenses()[-1]

    assert expense[1] == "2026-09-29"
    assert expense[2] == "Food"
    assert expense[3] == "Lunch"
    assert expense[4] == 15.50

def test_get_total_expenses(test_database):
    database.add_expense(
        "2026-09-29",
        "Food",
        "Lunch",
        15.50
    )

    database.add_expense(
        "2026-09-29",
        "Transport",
        "Uber",
        20.00
    )

    total = database.get_total_expenses()

    assert total == 35.50

def test_get_expense_by_id(test_database):
    database.add_expense(
        "2026-09-29",
        "Food",
        "Lunch",
        15.50
    )

    expense = database.get_expense_by_id(1)

    assert expense[0] == 1
    assert expense[1] == "2026-09-29"
    assert expense[2] == "Food"
    assert expense[3] == "Lunch"
    assert expense[4] == 15.50

def test_get_expense_by_id_not_found(test_database):
    expense = database.get_expense_by_id(999)

    assert expense is None

def test_delete_expense(test_database):
    database.add_expense(
        "2026-09-29",
        "Food",
        "Lunch",
        15.50
    )

    deleted = database.delete_expense(1)

    assert deleted is True

    expense = database.get_expense_by_id(1)

    assert expense is None

def test_delete_expense_not_found(test_database):
    deleted = database.delete_expense(999)

    assert deleted is False

def test_update_date(test_database):
    database.add_expense(
        "2026-09-29",
        "Food",
        "Lunch",
        15.50
    )

    updated = database.update_date(1, "2026-09-30")

    assert updated is True

    expense = database.get_expense_by_id(1)

    assert expense[1] == "2026-09-30"

def test_update_category(test_database):
    database.add_expense(
        "2026-09-29",
        "Food",
        "Lunch",
        15.50
    )

    updated = database.update_category(1, "Restaurant")

    assert updated is True

    expense = database.get_expense_by_id(1)

    assert expense[2] == "Restaurant"

def test_update_description(test_database):
    database.add_expense(
        "2026-09-29",
        "Food",
        "Lunch",
        15.50
    )

    updated = database.update_description(1, "Dinner")

    assert updated is True

    expense = database.get_expense_by_id(1)

    assert expense[3] == "Dinner"

def test_update_amount(test_database):
    database.add_expense(
        "2026-09-29",
        "Food",
        "Lunch",
        15.50
    )

    updated = database.update_amount(1, 25.75)

    assert updated is True

    expense = database.get_expense_by_id(1)

    assert expense[4] == 25.75

def test_get_expenses_by_category(test_database):
    database.add_expense(
        "2026-09-29",
        "Food",
        "Lunch",
        15.50
    )

    database.add_expense(
        "2026-09-30",
        "Food",
        "Dinner",
        25.00
    )

    database.add_expense(
        "2026-09-30",
        "Transport",
        "Uber",
        20.00
    )

    category_totals = database.get_expenses_by_category()

    assert ("Food", 40.50) in category_totals
    assert ("Transport", 20.00) in category_totals

def test_get_expenses(test_database):
    database.add_expense(
        "2026-09-29",
        "Food",
        "Lunch",
        15.50
    )

    database.add_expense(
        "2026-09-30",
        "Transport",
        "Uber",
        20.00
    )

    expenses = database.get_expenses()

    assert len(expenses) == 2
    assert expenses[0][2] == "Food"
    assert expenses[1][2] == "Transport"