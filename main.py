import sys
import database
import ai_helper

def display_menu(logged_in):
    print("\n--------------------------------")
    print("      AI Expense Tracker")
    print("--------------------------------")
    if not logged_in:
        print("1. Login")
        print("2. Register")
        print("3. Exit")
    else:
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Logout")
        print("4. Exit")
    print("--------------------------------")

def main():
    # setup the db at startup
    database.init_db()
    current_user_id = None

    while True:
        display_menu(current_user_id is not None)
        try:
            choice = input("Enter your choice: ").strip()
        except EOFError:
            break

        if not current_user_id:
            # not logged in menu
            if choice == "1":
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                user_id = database.login_user(username, password)
                if user_id:
                    print(f"\nLogin successful. Welcome {username}!")
                    current_user_id = user_id
                else:
                    print("\nInvalid username or password.")
            elif choice == "2":
                username = input("Choose a username: ").strip()
                password = input("Choose a password: ").strip()
                if not username or not password:
                    print("\nUsername and password cannot be empty.")
                    continue
                if database.register_user(username, password):
                    print("\nRegistration complete. You can login now.")
                else:
                    print("\nThat username is already taken.")
            elif choice == "3":
                print("\nExiting...")
                sys.exit(0)
            else:
                print("\nInvalid choice.")
        else:
            # logged in menu
            if choice == "1":
                try:
                    amount = float(input("Amount ($): ").strip())
                    if amount <= 0:
                        raise ValueError()
                except ValueError:
                    print("\nPlease enter a valid positive number.")
                    continue
                
                description = input("Expense Description: ").strip()
                if not description:
                    print("\nDescription cannot be empty.")
                    continue
                
                print("\nRunning AI categorization...")
                category = ai_helper.categorize_expense(description)
                print(f"Assigned Category: {category}")
                
                database.add_expense(current_user_id, amount, description, category)
                print("Expense saved!")
                
            elif choice == "2":
                expenses = database.get_expenses(current_user_id)
                if not expenses:
                    print("\nNo expenses yet.")
                else:
                    print("\n" + "-"*65)
                    print(f"{'Date':<20} | {'Amount':<10} | {'Category':<15} | {'Description'}")
                    print("-" * 65)
                    for exp in expenses:
                        print(f"{exp['date']:<20} | ${exp['amount']:<9.2f} | {exp['category']:<15} | {exp['description']}")
                    print("-" * 65)
            elif choice == "3":
                print("\nLogged out.")
                current_user_id = None
            elif choice == "4":
                print("\nExiting...")
                sys.exit(0)
            else:
                print("\nInvalid choice.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
