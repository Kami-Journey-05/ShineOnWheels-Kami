from admin import admin_menu
from util import initialize_files


def booking_menu():
    print("Booking menu coming soon...")


def customer_menu():
    print("Customer menu coming soon...")


def accountant_menu():
    print("Accountant menu coming soon...")


def maintenance_menu():
    print("Maintenance menu coming soon...")


def main_menu():
    initialize_files()

    while True:
        print("\n" + "=" * 50)
        print("SHINEONWHEELS CAR WASH SYSTEM")
        print("=" * 50)
        print("1. System Administrator")
        print("2. Booking Officer")
        print("3. Customer")
        print("4. Accountant")
        print("5. Maintenance Staff")
        print("6. Exit system")
        print("=" * 50)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            admin_menu()
        elif choice == "2":
            booking_menu()
        elif choice == "3":
            customer_menu()
        elif choice == "4":
            accountant_menu()
        elif choice == "5":
            maintenance_menu()
        elif choice == "6":
            print("Thank You!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main_menu()