import pytest
import mysql.connector
from decimal import Decimal

from main import add_accounts, view_accounts, update_balance, delete_account


@pytest.fixture
def test_conn():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        database="account_management_test"
    )

    try:
        cursor = conn.cursor()

        try:
            # Setup: 清空测试数据
            cursor.execute("DELETE FROM accounts")
            conn.commit()
        finally:
            cursor.close()

        yield conn

    finally:
        try:
            # Teardown: 清理测试产生的数据
            conn.rollback()

            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM accounts")
                conn.commit()
            finally:
                cursor.close()

        finally:
            conn.close()


def test_account_lifecycle(test_conn):
    #调用项目函数，向真实 MySQL 插入账户
    result = add_accounts(
        test_conn,
        "Alice",
        Decimal("500.00")
    )
    cursor = test_conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM accounts WHERE name = %s",
            ("Alice",)
        )
        account = cursor.fetchone()
        assert account is not None
        user_id, name, balance = account
        # 检验插入
        assert result == f"Account {user_id} added successfully"
        assert name == "Alice"
        assert balance == Decimal("500.00")
        # 修改余额
        result = update_balance(
            test_conn, user_id, Decimal("800.00")
        )
        assert result == "Balance has been modified"
        cursor.execute("SELECT balance FROM accounts WHERE id = %s", (user_id, ))
        updated_balance = cursor.fetchone()[0]
        assert updated_balance == Decimal("800.00")
        # 删除账户
        result = delete_account(test_conn, user_id)
        assert result == "Account has been deleted"
        cursor.execute("SELECT id FROM accounts WHERE id = %s", (user_id, ))
        assert cursor.fetchone() is None

    finally:
        cursor.close()


def test_view_accounts_empty_integration(test_conn):
    # Fixture 已经保证测试开始前清空账户表
    result = view_accounts(test_conn)

    assert result == []     