import mysql.connector #
from decimal import Decimal
from decimal import InvalidOperation #

def main():    
    while True:
        conn = mysql.connector.connect(#
                    host = "localhost",
                    user = "root",
                    database = "index_practice"
                )
        print("""
        ===== Account Management =====
        1. View accounts
        2. Add account
        3. Update balance
        4. Delete account
        5. Exit
        """)
        option = input("Choose an option: ")
        if option == "1":
            view_accounts(conn)
        elif option == "2":
            add_accounts(conn)
        elif option == "3":
            update_balance(conn)
        elif option == "4":
            delete_account(conn)
        elif option == "5":
            break
        else:
            print("Invalid option")

def view_accounts(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        for account in cursor.fetchall():
            print (account)
    except mysql.connector.Error as e:#
        print(f"Error: {e}")
    finally:
        if cursor is not None:
            cursor.close()

def add_accounts(conn):
    cursor = None
    try:
        user_id = int(input("Enter user's id: "))
        name = input("Enter user's name: ")
        balance = Decimal(input("Enter users's balance: "))
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (id, name, balance) VALUE (%s, %s, %s)", (user_id, name, balance))
        conn.commit()#
        print("Account added successfully")
    except (ValueError, InvalidOperation):
        print("Invalid input")
    except mysql.connector.Error as e:
        conn.rollback()#
        print(f"Error: {e}")
    finally:
        if cursor is not None:
            cursor.close()

def update_balance(conn):
    cursor = None
    try:
        user_id = int(input("Enter user's id: "))
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM accounts WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            print("Account not found")
            return
        balance = Decimal(input("Modify balance to: "))
        cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (balance, user_id))
        conn.commit()
        print("Balance has been modified")
    except (ValueError, InvalidOperation):
        print("Invalid input")
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        if cursor is not None:
            cursor.close()

def delete_account(conn):
    cursor = None
    try:
        user_id = int(input("Enter user's id: "))
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM accounts WHERE id = %s", (user_id, ))
        if not cursor.fetchone():
            print("Account not found")
            return
        while True:
            judgement = input("Are you sure to delete the account?(y/n): ")
            if judgement.lower() == "y":
                break
            elif judgement.lower() == "n":
                return
            else:
                print("Please enter y or n")
        cursor.execute("DELETE FROM accounts WHERE id = %s", (user_id, ))
        conn.commit()
        print("Account has been deleted")
    except (ValueError, InvalidOperation):
        print("Invalid input")
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        if cursor is not None:
            cursor.close()


if __name__ == "__main__":
    main()