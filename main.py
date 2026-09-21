from util import *
from validation import *
from constants import *

def admin_menu():
    print("Admin menu coming soon.....")
    
def booking_menu():
    print("Booking menu coming soon.....")
    
def customer_menu():
    print("Customer menu coming soon.....")
    
def accountant_menu():
    print("Accountant menu coing soon.....")
    
def maintenance_menu():
    print("Maintenance menu coming soon.....")
    
def main_menu():
    """Main Menu"""
    initialize_files()
     
while True:
    print("=" * 50)
    print("\tSHINEONWHEELS CAR WASH SYSTEM\t")
    print("=" * 50)
    print("1. System Administrator")
    print("2. Booking Officer")
    print("3. Customer")
    print("4. Accountant")
    print("5. Maintenance Staff")
    print("6. Exit system")
    print("=" * 50)

    choice = input("Enter your choice (1-6): ")

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
        print("Invalid Choice")

if __name__ == "___main___":
    main_menu()