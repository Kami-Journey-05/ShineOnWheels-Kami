# =============================================
# BOOKING.PY
# =============================================

from util import *
from validation import *
from constants import *
from datetime import datetime

# =============================================
# BOOKING OFFICER MENU
# =============================================

def booking_menu():
    """Booking Officer Menu"""
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
        print("="*40)
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            register_customer()
        elif choice == '2':
            process_booking()
        elif choice == '3':
            cancel_booking()
        elif choice == '4':
            reschedule_booking()
        elif choice == '5':
            view_all_bookings()
        elif choice == '6':
            view_customer_history()
        elif choice == '7':
            view_available_services()
        elif choice == '8':
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please enter 1-8.")

# =============================================
# HELPER: CHECK IF CUSTOMER EXISTS
# =============================================

def customer_exists(customer_id):
    """Check if a customer ID exists"""
    customers = read_file(customer_file)
    
    for customer in customers:
        parts = customer.strip().split(",")
        
        if len(parts) < 1:
            continue
        
        if parts[0] == customer_id:
            return True
    
    return False

# =============================================
# REGISTER NEW CUSTOMER
# =============================================

def register_customer():
    """Register new customer"""
    print("\n--- REGISTER NEW CUSTOMER ---")

    name = valid_input("Name: ", validate_name, "Name must be 2+ chars, letters only")

    phone = valid_input("Phone (10-12 digits): ", validate_phone, "Phone must be 10-12 digits")

    email = valid_input("Email: ", validate_email, "Email must contain @ and .")
    
    address = input("Address: ")
    if len(address.strip()) < 2:
        print("Address too short!")
        return

    customers = read_file(customer_file)
    customer_id = "C" + str(len(customers) + 1)

    # current date for registration:
    from datetime import datetime
    registration_date = datetime.now().strftime("%d/%m/%Y")
    
    
    record = customer_id + "," + name + "," + phone + "," + email + "," + address + "," + registration_date

    append_file(customer_file, record)
    
    print("\n Customer registered successfully!")
    print("   Customer ID: " + customer_id)
    print("   Registration Date: " + registration_date)
# =============================================
# PROCESS NEW BOOKING
# =============================================

def process_booking():
    """Process new booking"""
    print("\n--- PROCESS NEW BOOKING ---")
    
    customer_id = input("Enter customer ID: ")
    
    if not customer_exists(customer_id):
        print("Customer ID not found. Please register first.")
        return
    
    view_available_services()
    
    services = read_file(services_file)
    if len(services) == 0:
        return
    
    try:
        choice = int(input("\nSelect service number: "))
        if choice < 1 or choice > len(services):
            print("Invalid selection!")
            return
    except:
        print("Invalid input!")
        return
    
    service_data = services[choice-1].strip().split(",")
    service_name = service_data[0]
    base_price = float(service_data[1])
    
    date = valid_input("Enter Date (DD/MM/YYYY): ", validate_date, "Date must be DD/MM/YYYY")
    
    time = valid_input("Enter Time (HH:MM): ", validate_time, "Time must be HH:MM")

    bookings = read_file(booking_file)
    booking_id = "BK-" + datetime.now().strftime("%Y%m%d") + "-" + str(len(bookings) + 1000)
    
    tax = base_price * tax_rate
    subtotal = base_price + tax
    
    record = booking_id + "," + customer_id + "," + service_name + "," + date + "," + time + ",Confirmed," + str(round(subtotal, 2))
    
    append_file(booking_file, record)
    
    print("\n Booking confirmed!")
    print("   Booking ID: " + booking_id)
    print("   Service: " + service_name)
    print("   Total: RM" + str(round(subtotal, 2)))

# =============================================
# CANCEL BOOKING
# =============================================

def cancel_booking():
    """Cancel booking"""
    print("\n--- CANCEL BOOKING ---")
    
    booking_id = input("Enter booking ID to cancel: ")
    
    bookings = read_file(booking_file)
    updated = []
    found = False
    
    for booking in bookings:
        parts = booking.strip().split(",")
        
        if len(parts) < 6:
            updated.append(booking)
            continue
        
        if parts[0] == booking_id:
            parts[5] = "Cancelled"
            found = True
        
        updated.append(",".join(parts) + "\n")
    
    if found == False:
        print("Booking not found!")
        return
    
    write_file(booking_file, updated)
    print("Booking cancelled successfully!")

# =============================================
# RESCHEDULE BOOKING
# =============================================

def reschedule_booking():
    """Reschedule booking"""
    print("\n--- RESCHEDULE BOOKING ---")
    
    booking_id = input("Enter booking ID to reschedule: ")
    
    bookings = read_file(booking_file)
    updated = []
    found = False
    
    for booking in bookings:
        parts = booking.strip().split(",")
        
        if len(parts) < 6:
            updated.append(booking)
            continue
        
        if parts[0] == booking_id:
            print("Current: " + parts[3] + " at " + parts[4])
            
            new_date = valid_input("New Date (DD/MM/YYYY): ", validate_date, "Date must be DD/MM/YYYY")
            
            new_time = valid_input("New Time (HH:MM): ", validate_time, "Time must be HH:MM")
            
            parts[3] = new_date
            parts[4] = new_time
            found = True
        
        updated.append(",".join(parts) + "\n")
    
    if found == False:
        print("Booking not found!")
        return
    
    write_file(booking_file, updated)
    print("Booking rescheduled successfully!")

# =============================================
# VIEW ALL BOOKINGS
# =============================================

def view_all_bookings():
    """View all bookings"""
    bookings = read_file(booking_file)
    
    if len(bookings) == 0:
        print("No bookings found!")
        return
    
    print("\n=== ALL BOOKINGS ===")
    for booking in bookings:
        print(booking.strip())

# =============================================
# VIEW CUSTOMER HISTORY
# =============================================

def view_customer_history():
    """View customer booking history"""
    print("\n--- CUSTOMER HISTORY ---")
    
    customer_id = input("Enter customer ID: ")
    
    bookings = read_file(booking_file)
    found = False
    
    print("\n=== BOOKINGS FOR " + customer_id + " ===")
    
    for booking in bookings:
        parts = booking.strip().split(",")
        
        if len(parts) < 2:
            continue
        
        if parts[1] == customer_id:
            found = True
            print(booking.strip())
    
    if found == False:
        print("No bookings found for this customer!")

# =============================================
# VIEW AVAILABLE SERVICES
# =============================================

def view_available_services():
    """View available services"""
    print("\n--- AVAILABLE SERVICES ---")
    
    services = read_file(services_file)
    
    if len(services) == 0:
        print("Services file not found.")
        return
    
    found_any = False
    
    for i, line in enumerate(services, 1):
        parts = line.strip().split(",")
        
        if len(parts) < 3:
            continue
        
        found_any = True
        print(str(i) + ". " + parts[0] + " - RM" + parts[1] + " (" + parts[2] + " mins)")
    
    if not found_any:
        print("No services to display.")