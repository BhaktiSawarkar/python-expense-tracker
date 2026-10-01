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


@pytest.fixture
def sample_expense(test_database):
    database.add_expense(
        "2026-09-29",
        "Food",
        "Lunch",
        15.50
    )

    return database.get_expenses()[-1]


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

def test_get_expense_by_id(sample_expense):
    expense = sample_expense

    assert expense[0] == 1
    assert expense[1] == "2026-09-29"
    assert expense[2] == "Food"
    assert expense[3] == "Lunch"
    assert expense[4] == 15.50

def test_get_expense_by_id_not_found(test_database):
    expense = database.get_expense_by_id(999)

    assert expense is None

def test_delete_expense(sample_expense):
    expense_id = sample_expense[0]
    deleted = database.delete_expense(expense_id)

    assert deleted is True

    expense = database.get_expense_by_id(expense_id)

    assert expense is None

def test_delete_expense_not_found(test_database):
    deleted = database.delete_expense(999)

    assert deleted is False

def test_update_date(sample_expense):
    expense_id = sample_expense[0]
    updated = database.update_date(expense_id, "2026-09-30")

    assert updated is True

    expense = database.get_expense_by_id(expense_id)

    assert expense[1] == "2026-09-30"

def test_update_category(sample_expense):
    expense_id = sample_expense[0]
    updated = database.update_category(expense_id, "Restaurant")

    assert updated is True

    expense = database.get_expense_by_id(expense_id)

    assert expense[2] == "Restaurant"

def test_update_description(sample_expense):
    expense_id = sample_expense[0]
    updated = database.update_description(expense_id, "Dinner")

    assert updated is True

    expense = database.get_expense_by_id(expense_id)

    assert expense[3] == "Dinner"

def test_update_amount(sample_expense):
    expense_id = sample_expense[0]
    updated = database.update_amount(expense_id, 25.75)

    assert updated is True

    expense = database.get_expense_by_id(expense_id)

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