from util import *
from validation import *
from constants import *



CUSTOMERS_FILE = "customers.txt"
BOOKINGS_FILE = "bookings.txt"
SERVICES_FILE = "services.txt"


# ---------------------------------------------------------
# 1. DISPLAY BOOKING OFFICER MENU
# ---------------------------------------------------------

def booking_menu():
    while True:
        print("\n===== BOOKING OFFICER MENU =====")
        print("1. Register New Customer")
        print("2. Process New Booking")
        print("3. Cancel Booking")
        print("4. Reschedule Booking")
        print("5. View All Bookings")
        print("6. View Customer History")
        print("7. View Available Services")
        print("8. Back to Main Menu")

        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            register_customer()
        elif choice == "2":
            process_booking()
        elif choice == "3":
            cancel_booking()
        elif choice == "4":
            reschedule_booking()
        elif choice == "5":
            view_all_bookings()
        elif choice == "6":
            view_customer_history()
        elif choice == "7":
            view_available_services()
        elif choice == "8":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


# ---------------------------------------------------------
# 2. REGISTER NEW CUSTOMER
# ---------------------------------------------------------

def register_customer():
    print("\n--- REGISTER NEW CUSTOMER ---")

    name = input("Enter customer name: ")
    phone = input("Enter phone number: ")
    address = input("Enter address: ")

    # Read existing customers to generate a new ID
    try:
        file = open(CUSTOMERS_FILE, "r")
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        lines = []

    new_id = "C" + str(len(lines) + 1)

    record = new_id + "," + name + "," + phone + "," + address + "\n"

    file = open(CUSTOMERS_FILE, "a")
    file.write(record)
    file.close()

    print("Customer registered successfully!")
    print("Customer ID:", new_id)


# ---------------------------------------------------------
# Helper: check if a customer ID exists
# ---------------------------------------------------------

def customer_exists(customer_id):
    try:
        file = open(CUSTOMERS_FILE, "r")
    except FileNotFoundError:
        return False

    for line in file:
        parts = line.strip().split(",")
        if parts[0] == customer_id:
            file.close()
            return True

    file.close()
    return False


# ---------------------------------------------------------
# 3. PROCESS NEW BOOKING
# ---------------------------------------------------------

def process_booking():
    print("\n--- PROCESS NEW BOOKING ---")

    customer_id = input("Enter customer ID: ")

    if not customer_exists(customer_id):
        print("Customer ID not found. Please register the customer first.")
        return

    service = input("Enter service type: ")
    date = input("Enter booking date (DD/MM/YYYY): ")
    time = input("Enter booking time: ")

    try:
        file = open(BOOKINGS_FILE, "r")
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        lines = []

    new_id = "B" + str(len(lines) + 1)
    status = "Confirmed"

    record = (new_id + "," + customer_id + "," + service + "," +
              date + "," + time + "," + status + "\n")

    file = open(BOOKINGS_FILE, "a")
    file.write(record)
    file.close()

    print("Booking created successfully!")
    print("Booking ID:", new_id)


# ---------------------------------------------------------
# 4. CANCEL EXISTING BOOKING
# ---------------------------------------------------------

def cancel_booking():
    print("\n--- CANCEL BOOKING ---")

    booking_id = input("Enter booking ID to cancel: ")

    try:
        file = open(BOOKINGS_FILE, "r")
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        print("No bookings found.")
        return

    updated_lines = []
    found = False

    for line in lines:
        parts = line.strip().split(",")
        if parts[0] == booking_id:
            parts[5] = "Cancelled"
            found = True
            line = ",".join(parts) + "\n"
        updated_lines.append(line)

    if not found:
        print("Booking ID not found.")
        return

    file = open(BOOKINGS_FILE, "w")
    file.writelines(updated_lines)
    file.close()

    print("Booking", booking_id, "has been cancelled.")


# ---------------------------------------------------------
# 5. RESCHEDULE BOOKING (change date/time)
# ---------------------------------------------------------

def reschedule_booking():
    print("\n--- RESCHEDULE BOOKING ---")

    booking_id = input("Enter booking ID to reschedule: ")

    try:
        file = open(BOOKINGS_FILE, "r")
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        print("No bookings found.")
        return

    updated_lines = []
    found = False

    for line in lines:
        parts = line.strip().split(",")
        if parts[0] == booking_id:
            new_date = input("Enter new date (DD/MM/YYYY): ")
            new_time = input("Enter new time: ")
            parts[3] = new_date
            parts[4] = new_time
            found = True
            line = ",".join(parts) + "\n"
        updated_lines.append(line)

    if not found:
        print("Booking ID not found.")
        return

    file = open(BOOKINGS_FILE, "w")
    file.writelines(updated_lines)
    file.close()

    print("Booking", booking_id, "has been rescheduled.")


# ---------------------------------------------------------
# 6. VIEW ALL BOOKINGS
# ---------------------------------------------------------

def view_all_bookings():
    print("\n--- ALL BOOKINGS ---")

    try:
        file = open(BOOKINGS_FILE, "r")
    except FileNotFoundError:
        print("No bookings found.")
        return

    found_any = False

    for line in file:
        parts = line.strip().split(",")
        found_any = True
        print("Booking ID:", parts[0])
        print("  Customer ID:", parts[1])
        print("  Service:", parts[2])
        print("  Date:", parts[3])
        print("  Time:", parts[4])
        print("  Status:", parts[5])
        print("-" * 30)

    file.close()

    if not found_any:
        print("No bookings found.")


# ---------------------------------------------------------
# 7. VIEW ONE CUSTOMER'S BOOKING HISTORY
# ---------------------------------------------------------

def view_customer_history():
    print("\n--- CUSTOMER BOOKING HISTORY ---")

    customer_id = input("Enter customer ID: ")

    if not customer_exists(customer_id):
        print("Customer ID not found.")
        return

    try:
        file = open(BOOKINGS_FILE, "r")
    except FileNotFoundError:
        print("No booking history found.")
        return

    found_any = False

    for line in file:
        parts = line.strip().split(",")
        if parts[1] == customer_id:
            found_any = True
            print("Booking ID:", parts[0])
            print("  Service:", parts[2])
            print("  Date:", parts[3])
            print("  Time:", parts[4])
            print("  Status:", parts[5])
            print("-" * 30)

    file.close()

    if not found_any:
        print("This customer has no booking history yet.")


# ---------------------------------------------------------
# 8. VIEW AVAILABLE SERVICES (WITH SLOTS)
# ---------------------------------------------------------

def view_available_services():
    print("\n--- AVAILABLE SERVICES ---")

    try:
        file = open(SERVICES_FILE, "r")
    except FileNotFoundError:
        print("Services file not found.")
        return

    found_any = False

    for line in file:
        parts = line.strip().split(",")
        # Expected format: service_name,price,available_slots
        service_name = parts[0]
        price = parts[1]
        slots = parts[2]

        if int(slots) > 0:
            found_any = True
            print("Service:", service_name)
            print("  Price: RM" + price)
            print("  Available Slots:", slots)
            print("-" * 30)

    file.close()

    if not found_any:
        print("No services with available slots right now.")


# ---------------------------------------------------------
# RUN DIRECTLY FOR TESTING
# ---------------------------------------------------------

if __name__ == "__main__":
    booking_menu()
