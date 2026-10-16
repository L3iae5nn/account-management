while True:
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
        print("View accounts")
    elif option == "2":
        print("Add account")
    elif option == "3":
        print("Update balance")
    elif option == "4":
        print("Delete account")
    elif option == "5":
        break
    else:
        print("Invalid option")