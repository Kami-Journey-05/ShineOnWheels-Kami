from util import *
from validation import *
from constants import *

from admin import *
from booking import *
from customer import *
from accountant import *
from maintenance import *
  
def main_menu():
    """Main Menu"""
    initialize_files()
     
    
while True:
    print("=" * 50)
    print("\tSHINE-ON-WHEELS CAR WASH SYSTEM\t")
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
        print("\t\"Thank You for visiting Shine-On-Wheels!\"")
        print("\t\"Excellence in every Wash✨\"")
        break
    else:
        print("Invalid Choice")

if __name__ == "___main___":
    main_menu()