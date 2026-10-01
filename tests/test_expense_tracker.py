import expense_tracker


def test_show_menu(capsys):
    expense_tracker.show_menu()

    captured = capsys.readouterr()

    assert "Expense Tracker" in captured.out
    assert "1. Add Expense" in captured.out
    assert "7. Exit" in captured.out

def test_add_expense_empty_category(monkeypatch, capsys):
    inputs = iter([
        "2026-09-29",  # valid date
        "",            # empty category
        "Food",        # valid category
        "Lunch",       # description
        "15.50"        # amount
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr("expense_tracker.database.add_expense", lambda *args: None)

    expense_tracker.add_expense()

    captured = capsys.readouterr()

    assert "Category cannot be empty" in captured.out

def test_add_expense_empty_description(monkeypatch, capsys):
    inputs = iter([
        "2026-09-29",
        "Food",
        "",
        "Lunch",
        "15.50"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr(
        "expense_tracker.database.add_expense",
        lambda *args: None
    )

    expense_tracker.add_expense()

    captured = capsys.readouterr()

    assert "Description cannot be empty" in captured.out

def test_add_expense_negative_amount(monkeypatch, capsys):
    inputs = iter([
        "2026-09-29",
        "Food",
        "Lunch",
        "-10",
        "15.50"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr(
        "expense_tracker.database.add_expense",
        lambda *args: None
    )

    expense_tracker.add_expense()

    captured = capsys.readouterr()

    assert "Amount must be a positive number" in captured.out

def test_add_expense_invalid_amount(monkeypatch, capsys):
    inputs = iter([
        "2026-09-29",
        "Food",
        "Lunch",
        "abc",
        "15.50"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr(
        "expense_tracker.database.add_expense",
        lambda *args: None
    )

    expense_tracker.add_expense()

    captured = capsys.readouterr()

    assert "Invalid input for amount" in captured.out

def test_add_expense_invalid_date(monkeypatch, capsys):
    inputs = iter([
        "09-29-2026",
        "2026-09-29",
        "Food",
        "Lunch",
        "15.50"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr(
        "expense_tracker.database.add_expense",
        lambda *args: None
    )

    expense_tracker.add_expense()

    captured = capsys.readouterr()

    assert "Invalid date format" in captured.out

def test_get_valid_date(monkeypatch):
    inputs = iter([
        "invalid-date",
        "2026-09-29"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = expense_tracker.get_valid_date()

    assert result == "2026-09-29"    

def test_get_valid_category(monkeypatch):
    inputs = iter([
        "",
        "Food"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = expense_tracker.get_valid_category()

    assert result == "Food"

def test_get_valid_description(monkeypatch):
    inputs = iter([
        "",
        "Lunch"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = expense_tracker.get_valid_description()

    assert result == "Lunch"

def test_get_valid_amount(monkeypatch):
    inputs = iter([
        "abc",
        "-10",
        "15.50"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = expense_tracker.get_valid_amount()

    assert result == 15.50

def test_update_expense_date(monkeypatch):
    inputs = iter([
        "1",
        "1",
        "2026-09-30"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr(
        "expense_tracker.database.get_expense_by_id",
        lambda expense_id: (1, "2026-09-29", "Food", "Lunch", 15.50)
    )

    updated_values = {}

    def fake_update_date(expense_id, new_date):
        updated_values["expense_id"] = expense_id
        updated_values["new_date"] = new_date
        return True

    monkeypatch.setattr(
        "expense_tracker.database.update_date",
        fake_update_date
    )

    expense_tracker.update_expense()

    assert updated_values["expense_id"] == 1
    assert updated_values["new_date"] == "2026-09-30"

def test_update_expense_category(monkeypatch):
    inputs = iter([
        "1",
        "2",
        "Restaurant"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr(
        "expense_tracker.database.get_expense_by_id",
        lambda expense_id: (1, "2026-09-29", "Food", "Lunch", 15.50)
    )

    updated_values = {}

    def fake_update_category(expense_id, new_category):
        updated_values["expense_id"] = expense_id
        updated_values["category"] = new_category
        return True

    monkeypatch.setattr(
        "expense_tracker.database.update_category",
        fake_update_category
    )

    expense_tracker.update_expense()

    assert updated_values["expense_id"] == 1
    assert updated_values["category"] == "Restaurant"

def test_update_expense_description(monkeypatch):
    inputs = iter([
        "1",
        "3",
        "Dinner"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr(
        "expense_tracker.database.get_expense_by_id",
        lambda expense_id: (1, "2026-09-29", "Food", "Lunch", 15.50)
    )

    updated_values = {}

    def fake_update_description(expense_id, new_description):
        updated_values["expense_id"] = expense_id
        updated_values["description"] = new_description
        return True

    monkeypatch.setattr(
        "expense_tracker.database.update_description",
        fake_update_description
    )

    expense_tracker.update_expense()

    assert updated_values["expense_id"] == 1
    assert updated_values["description"] == "Dinner"

def test_update_expense_amount(monkeypatch):
    inputs = iter([
        "1",
        "4",
        "25.75"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr(
        "expense_tracker.database.get_expense_by_id",
        lambda expense_id: (1, "2026-09-29", "Food", "Lunch", 15.50)
    )

    updated_values = {}

    def fake_update_amount(expense_id, new_amount):
        updated_values["expense_id"] = expense_id
        updated_values["amount"] = new_amount
        return True

    monkeypatch.setattr(
        "expense_tracker.database.update_amount",
        fake_update_amount
    )

    expense_tracker.update_expense()

    assert updated_values["expense_id"] == 1
    assert updated_values["amount"] == 25.75
