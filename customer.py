
# ---------- "CUSTOMER.PY" -----------

from util import *
from validation import *
from constants import *
from datetime import datetime
import random

#  ------ "CUSTOMER LOGIN" ---------

def authenticate_customer():
    """Customer login"""
    print("\n" + "="*50)
    print("-----CUSTOMER LOGIN-----")
    print("="*50)
    
    customer_id = input("Enter Customer ID : ")
    
    customers = read_file(customer_file)
    
    if len(customers) == 0:
        print("\n No customers registered yet!")
        return None
    
    for customer in customers:
        parts = customer.strip().split(",")
        #parts[0] = CustomerID
        #parts[1] = Name
        #parts[2] = Phone
        #parts[3] = Email
        #parts[4] = Register Date
        
        if len(parts) < 2:
            continue
        if parts[0] == customer_id:
            print("\n Login successful!")
            print("Welcome back, " + parts[1] + "!")
            print("Phone: " + parts[2])
            print("Email:"  + parts[3])
            return customer_id
    
    print("\n Customer ID not found!")
    return None

# 1. -------- "VIEW AVAILABLE SERVICES" ----------- 

def view_available_services():
    """View available services with slots"""
    services = read_file(services_file)
    
    if len(services) == 0:
        print("\n No services available!")
        return
    
    print("\n" + "="*60)
    print("\t\t\tAVAILABLE SERVICES\t")
    print("="*60)
    print("Service\t\t\tPrice\t  Duration\tSlots")
    print("-"*60)
    
    number = 1
    for service in services:
        parts = service.strip().split(",")
        #parts[0] = Service Name
        #parts[1] = Price
        #parts[2] = Duration
        #parts[3] = Capacity
        #parts[4] = Slots
        
        if len(parts) < 4:
            continue
        name = parts[0]
        price = parts[1]
        duration = parts[2]
        capacity = parts[3]
        print(str(number) + ". " + name + " "*(20-len(name)) + "RM" + price + " "*(10-len(price)) + duration + " mins\t" +  capacity  + "Slots")
        number = number + 1

# 2. ---------- "REQUEST BOOKING" -------------

def request_booking(customer_id):
    """Customer booking request"""
    print("\n--- REQUEST A BOOKING ---")
    
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
    
    date = input("Enter Date (DD/MM/YYYY): ")
    if validate_date(date) == False:
        print("Invalid date!")
        return
    
    time = input("Enter Time (HH:MM): ")
    if validate_time(time) == False:
        print("Invalid time!")
        return
    
    # ------- "Generate Booking ID" -------- 
    
    bookings = read_file(booking_file)
    booking_number = len(bookings) + 1000
    date_part = datetime.now().strftime("%Y%m%d")
    booking_id = "BK-" + date_part + "-" + str(booking_number)
    
    tax = base_price * tax_rate
    subtotal = base_price + tax
    
    new_booking = booking_id + "," + customer_id + "," + service_name + "," + date + "," + time + ",Confirmed," + str(round(subtotal, 2))
    append_file(booking_file, new_booking)
    
    log_operation("CUSTOMER_BOOKING", "Customer " + customer_id + " booked " + service_name)
    
    print("\n" + "=" * 30)
    print("\n Booking confirmed!")
    print("=" * 30)
    print("   Booking ID: " + booking_id)
    print("   Service: " + service_name)
    print("Date: " + date + " at " + time)
    print("Base Price: RM" + "{:.2f}".format(base_price))
    print("Tax (6%): RM " + str(round(tax, 2)))
    print("   Total: RM" + "{:.2f}".format(subtotal))
    print("=" * 30)
    
# 3. ----------- "Request Extension" -----------

def request_extension(customer_id):
    """Request an extension (reschedule)"""
    print("\n--- REQUEST AN EXTENSION ---")
    
    booking_id = input("Enter Booking ID: ")
    
    bookings = read_file(booking_file)
    updated = []
    found = False
    
    for booking in bookings:
        parts = booking.strip().split(",")
        # whats means of these parts that i used:
        # parts[0] = Booking ID
        # parts[1] = Customer ID
        # parts[2] = Service name
        # parts[3] = Date
        # parts[4] = Time
        # parts[5] = Status
        # parts[6] = Amount
        
        if len(parts) < 6:
            updated.append(booking)
            continue
        
        if parts[0] == booking_id and parts[1] == customer_id:
            print("Current: " + parts[3] + " at " + parts[4])
            
            new_date = input("New Date (DD/MM/YYYY): ")
            if validate_date(new_date) == False:
                print("Invalid date!")
                return
            
            new_time = input("New Time (HH:MM): ")
            if validate_time(new_time) == False:
                print("Invalid time!")
                return
            
            parts[3] = new_date
            parts[4] = new_time
            found = True
        
        updated.append(",".join(parts) + "\n")
    
    if found == False:
        print("Booking not found!")
        return
    
    write_file(booking_file, updated)
    print("Extension requested successfully!")


# 4. --------- "VIEW MY BOOKINGS" -----------

def view_my_bookings(customer_id):
    bookings = read_file(booking_file)
    
    print("\n MY BOOKINGS ")
    found = False
    for booking in bookings:
        parts = booking.strip().split(",")
        #parts[0] = BookingID
        #part[1] = CustomerID
        #parts[2] = ServiceName
        #parts[3] = Date
        #parts[4] = Time
        #parts[5] = Status
        #parts[6] = Amount
          
        if len(parts) < 6:
            continue
        if parts[1] == customer_id:
            found = True
            print(parts[0] + " | " + parts[2] + " | " + parts[3] + " | " + parts[5])
    if found == False:
        print("No bookings found!")

# 5. ------- "VIEW MY PAYMENTS History "---------

def view_my_payments(customer_id):
    # STEP 1: find the customer booking like
    bookings = read_file(booking_file)
    my_booking_ids = []
    for booking in bookings:
        parts = booking.strip().split(",")
        if len(parts) < 2:
            continue
        if parts[1] == customer_id:
            my_booking_ids.append(parts[0])
    
    payments = read_file(payment_file)
    
    print("Payment ID\tBooking ID\tAmount\tDate\tStatus")
    
    found = False
    total_paid = 0
    total_pending = 0
    
    for payment in payments:
        parts = payment.strip().split(",")
        if len(parts) < 4:
            continue
        payment_booking_id = parts[1]
        if payment_booking_id in my_booking_ids:
            found = True
            print(parts[0] + " | " + parts[1] + " | RM" + "{:.2f}".format(float(parts[2])) + " | " + parts[3] + " | " + parts[4])
            try:
                amount_float = float(parts[2])
                if parts[4] == "Completed":
                    total_paid = total_paid + amount_float
                else:
                    total_pending = total_pending + amount_float
            except:
                pass

    print("Total Paid: RM" + "{:.2f}".format(total_paid))
    print("Total Pending: RM" + "{:.2f}".format(total_pending))


# 6. ------- "VIEW MY LOYALTY" ----------

def view_my_loyalty(customer_id):
    bookings = read_file(booking_file)
    count = 0
    for booking in bookings:
        parts = booking.strip().split(",")
        if len(parts) < 2:
            continue
        if parts[1] == customer_id:
            count = count + 1
    print("\n LOYALTY STATUS")
    print("Total Bookings: " + str(count))
    if count >= 20:
        print("Tier: Platinum (15% discount)")
    elif count >= 10:
        print("Tier: Gold (10% discount)")
    elif count >= 5:
        print("Tier: Silver (5% discount)")
    else:
        print("Tier: Standard (0% discount)")

# 7. --------- "VIEW MY PROFILE" ---------

def view_my_profile(customer_id):
    """View customer profile - read from customers.txt"""
    customers = read_file(customer_file)
        
    print("\n" + "="*50)
    print("   MY PROFILE   ")
    print("="*50)
    
    for customer in customers:
        parts = customer.strip().split(",")
        # parts[0] = Customer ID
        # parts[1] = Name
        # parts[2] = Phone
        # parts[3] = Email
        # parts[4] = Address
        # parts[5] = Registra date
        
        if parts[0] == customer_id:
            print("Customer ID: " + parts[0])
            print("Name: " + parts[1])
            print("Phone: " + parts[2])
            print("Email: " + parts[3])
            if len(parts) > 4:
                print("Adress: " + parts[4])
            if len(parts) > 5:
                print("Register Date: " + parts[5])
            break
    
    print("="*50)
# 8. --------- "CUSTOMER MENU" ---------

def customer_menu():
    customer_id = authenticate_customer()
    if customer_id == None:
        return
    
    while True:
        print("\n" + "=" * 50)
        print("\n CUSTOMER MENU")
        print("1. View Available Services With Slots")
        print("2. Request a Booking")
        print("3. Request an Extension")
        print("4. View My Bookings")
        print("5. View Payment History")
        print("6. View My Loyalty Status")
        print("7. View My Profile")
        print("8. Back to Main Menu")
        print("=" * 50)
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            view_available_services()
        elif choice == '2':
            request_booking(customer_id)
        elif choice == '3':
            request_extension(customer_id)
        elif choice == '4':
            view_my_bookings(customer_id)
        elif choice == '5':
            view_my_payments(customer_id)
        elif choice == '6':
            view_my_loyalty(customer_id)
        elif choice == '7':
            view_my_profile(customer_id)
        elif choice == '8':
            print("Thank You!")
            break
        else:
            print("Invalid choice!")
    
    
    
    
    
    

    
    
   
        
      