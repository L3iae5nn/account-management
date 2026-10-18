from unittest.mock import MagicMock, call
from main import view_accounts, add_accounts, update_balance, delete_account
from decimal import Decimal
import mysql.connector
import pytest

@pytest.fixture
def mock_conn():
    return MagicMock()

def test_view_accounts(mock_conn):
    expected = [
        (1, "Alice", 500),
        (2, "Bob", 700)
    ]
    mock_conn.cursor.return_value.fetchall.return_value = expected
    result = view_accounts(mock_conn)
    assert result == expected
    mock_conn.cursor.return_value.close.assert_called_once()

def test_view_accounts_empty(mock_conn):
    mock_conn.cursor.return_value.fetchall.return_value = []
    result = view_accounts(mock_conn)
    assert result == []
    mock_conn.cursor.return_value.close.assert_called_once()

def test_add_accounts(mock_conn):
    mock_conn.cursor.return_value.lastrowid = 3
    result = add_accounts(mock_conn, "Alice", Decimal("500"))
    assert result == "Account 3 added successfully"
    mock_conn.cursor.return_value.execute.assert_called_once_with(
        "INSERT INTO accounts (name, balance) VALUE (%s, %s)", ("Alice", Decimal("500")) 
    )
    mock_conn.cursor.return_value.close.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_conn.rollback.assert_not_called()

def test_add_accounts_error(mock_conn):
    mock_conn.cursor.return_value.execute.side_effect = mysql.connector.Error
    with pytest.raises(mysql.connector.Error):
        add_accounts(mock_conn, "Alice", Decimal("500"))
    mock_conn.rollback.assert_called_once()    
    mock_conn.cursor.return_value.close.assert_called_once()
    mock_conn.commit.assert_not_called()

def test_update_balance_not_found(mock_conn):
    mock_conn.cursor.return_value.fetchone.return_value = None
    assert update_balance(mock_conn, 999, Decimal("500")) == "Account not found"
    mock_conn.cursor.return_value.execute.assert_called_once_with(
    "SELECT id FROM accounts WHERE id = %s",(999,))
    mock_conn.commit.assert_not_called()
    mock_conn.cursor.return_value.close.assert_called_once()

def test_update_balance(mock_conn):
    mock_conn.cursor.return_value.fetchone.return_value = (1, )
    assert update_balance(mock_conn, 1, Decimal("500")) == "Balance has been modified"
    mock_conn.cursor.return_value.execute.assert_has_calls([
        call("SELECT id FROM accounts WHERE id = %s", (1, )),
        call("UPDATE accounts SET balance = %s WHERE id = %s",(Decimal("500"), 1)),
    ])
    assert mock_conn.cursor.return_value.execute.call_count == 2
    mock_conn.commit.assert_called_once()
    mock_conn.cursor.return_value.close.assert_called_once()
    mock_conn.rollback.assert_not_called()

def test_delete_account(mock_conn):
    mock_conn.cursor.return_value.fetchone.return_value = (1, )
    assert delete_account(mock_conn, 1) == "Account has been deleted"
    mock_conn.cursor.return_value.execute.assert_has_calls([
        call("SELECT id FROM accounts WHERE id = %s", (1, )),
        call("DELETE FROM accounts WHERE id = %s", (1, ))
    ])
    assert mock_conn.cursor.return_value.execute.call_count == 2
    mock_conn.commit.assert_called_once()
    mock_conn.rollback.assert_not_called()
    mock_conn.cursor.return_value.close.assert_called_once()

def test_delete_account_not_found(mock_conn):
    mock_conn.cursor.return_value.fetchone.return_value = None
    assert delete_account(mock_conn, 999) == "Account not found"
    mock_conn.cursor.return_value.execute.assert_called_once_with(
        "SELECT id FROM accounts WHERE id = %s", (999, )
    )
    mock_conn.commit.assert_not_called()
    mock_conn.cursor.return_value.close.assert_called_once()
