import mysql.connector #
from decimal import Decimal
from decimal import InvalidOperation #

def main():
    conn = None
    try:    
        conn = mysql.connector.connect(#
            host = "localhost",
            user = "root",
            database = "index_practice"
        )
        while True:
            print("""
            ===== Account Management =====
            1. View accounts
            2. Add account
            3. Update balance
            4. Delete account
            5. Exit
            """)
            option = input("Choose an option: ").strip()
            try:
                if option == "1":
                    view_results = view_accounts(conn)
                    if not view_results:
                        print("No accounts found")
                    else:
                        for result in view_results:
                            print(result)
                elif option == "2":
                    name = input("Enter user's name: ")
                    balance = Decimal(input("Enter users's balance: "))
                    add_results = add_accounts(conn, name, balance)
                    print(add_results)
                elif option == "3":
                    user_id = int(input("Enter user's id: "))
                    balance = Decimal(input("Modify balance to: "))
                    update_results = update_balance(conn, user_id, balance)
                    print(update_results)
                elif option == "4":
                    user_id = int(input("Enter user's id: "))
                    while True:
                        judgement = input("Are you sure to delete the account?(y/n): ")
                        if judgement.lower().strip() == "y":
                            delete_results = delete_account(conn, user_id)
                            print(delete_results)
                            break
                        elif judgement.lower().strip() == "n":
                            print("Deletion cancelled")
                            break
                        else:
                            print("Please enter y or n")
                elif option == "5":
                    print("Goodbye!")
                    break #之后执行finally
                else:
                    print("Invalid option")
            except (ValueError, InvalidOperation):#共用异常代码处理逻辑
                print("Invalid input")
            except mysql.connector.Error as e:
                print(f"Database error: {e}")
    except mysql.connector.Error as e:
        print(f"Connection error: {e}")
    finally:
        if conn is not None:
            conn.close()


def view_accounts(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        return(cursor.fetchall())
    finally:
        if cursor is not None:
            cursor.close()

def add_accounts(conn, name, balance):
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (name, balance) VALUE (%s, %s)", (name, balance))
        new_id = cursor.lastrowid
        conn.commit()#
        return(f"Account {new_id} added successfully")
    except mysql.connector.Error:
        conn.rollback()#
        raise
    finally:
        if cursor is not None:
            cursor.close()

def update_balance(conn, user_id, balance):
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM accounts WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return("Account not found")
        cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (balance, user_id))
        conn.commit()
        return("Balance has been modified")
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()

def delete_account(conn, user_id):
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM accounts WHERE id = %s", (user_id, ))
        if not cursor.fetchone():
            return("Account not found")
        cursor.execute("DELETE FROM accounts WHERE id = %s", (user_id, ))
        conn.commit()
        return("Account has been deleted")
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()


if __name__ == "__main__":
    main()