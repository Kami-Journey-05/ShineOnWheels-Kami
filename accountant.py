# =============================================
# ACCOUNTANT.PY
# =============================================

from util import *
from validation import *
from constants import *
from datetime import datetime

def accountant_menu():
    """Accountant Menu"""
    while True:
        print("\n===== ACCOUNTANT MENU =====")
        print("1. Record Payment")
        print("2. View All Payments")
        print("3. Income Summary")
        print("4. Monthly Financial Report")
        print("5. Outstanding Payments")
        print("6. Back to Main Menu")
        print("="*40)
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            record_payment()
        elif choice == '2':
            view_all_payments()
        elif choice == '3':
            generate_income_summary()
        elif choice == '4':
            generate_monthly_financial_report()
        elif choice == '5':
            view_outstanding_payments()
        elif choice == '6':
            break
        else:
            print("Invalid choice!")

def record_payment():
    """Record a payment"""
    print("\n--- RECORD PAYMENT ---")
    
    booking_id = input("Enter Booking ID: ")
    
    # Booking SEARCH
    bookings = read_file(booking_file)
    
    booking_found = False
    amount = 0
    
    for booking in bookings:
        parts = booking.strip().split(",")
        if len(parts) < 2:
            continue
        if parts[0] == booking_id:
            booking_found = True
            print("Booking found: " + parts[2])
            amount = float(parts[6])
            break
    
    if booking_found == False:
        print("Booking not found!")
        return
    
    print("Amount: RM" + str(amount))
    confirm = input("Confirm payment? (y/n): ")
    
    if confirm.lower() != 'y':
        print("Cancelled.")
        return
    
    # Payment ID generate
    payments = read_file(payment_file)
    payment_id = "PAY-" + str(len(payments) + 1).zfill(3)
    date = datetime.now().strftime("%d/%m/%Y")
    
    # Save 
    new_payment = payment_id + "," + booking_id + "," + str(amount) + "," + date + ",Completed"
    append_file(payment_file, new_payment)
    
    print("Payment recorded!")
    print("Payment ID: " + payment_id)

def view_all_payments():
    """View all payments"""
    payments = read_file(payment_file)
    print("\n=== ALL PAYMENTS ===")
    for payment in payments:
        print(payment.strip())

def generate_income_summary():
    """Income summary"""
    payments = read_file(payment_file)
    total = 0
    count = 0
    for payment in payments:
        parts = payment.strip().split(",")
        if len(parts) >= 3:
            try:
                total = total + float(parts[2])
                count = count + 1
            except:
                pass
    
    print("\n=== INCOME SUMMARY ===")
    print("Total Revenue: RM" + str(round(total, 2)))
    print("Total Payments: " + str(count))

def generate_monthly_financial_report():
    """Monthly report"""
    print("\n=== MONTHLY REPORT ===")
    payments = read_file(payment_file)
    total = 0
    for payment in payments:
        parts = payment.strip().split(",")
        if len(parts) >= 3:
            try:
                total = total + float(parts[2])
            except:
                pass
    print("Total Revenue: RM" + str(round(total, 2)))

def view_outstanding_payments():
    """Outstanding payments"""
    print("\n=== OUTSTANDING PAYMENTS ===")
    bookings = read_file(booking_file)
    payments = read_file(payment_file)
    
    paid_bookings = []
    for payment in payments:
        parts = payment.strip().split(",")
        if len(parts) >= 2:
            paid_bookings.append(parts[1])
    
    for booking in bookings:
        parts = booking.strip().split(",")
        if len(parts) >= 2:
            if parts[0] not in paid_bookings:
                print(parts[0] + " - " + parts[2] + " - RM" + parts[6])