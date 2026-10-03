from util import *
from validation import *
from constants import *

import math
import os
from datetime import datetime

PAYMENTS_FILE = "payments.txt"
BOOKINGS_FILE = "bookings.txt"
SERVICES_FILE = "services.txt"
SEP = "|"

P_ID, P_BOOKING, P_CUSTOMER, P_AMOUNT, P_METHOD, P_STATUS, P_DATE = range(7)
B_ID, B_CUSTOMER, B_SERVICE, B_DATE, B_TIME, B_STATUS = range(6)
S_ID, S_NAME, S_PRICE = range(3)

PAID = "Paid"
PARTIAL = "Partial"
METHODS = ["Cash", "Card", "Online Transfer"]
EPS = 0.005


def read_records(filename, min_fields):
    records = []
    if not os.path.exists(filename):
        return records
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = [x.strip() for x in line.split(SEP)]
            if len(fields) >= min_fields:
                records.append(fields)
    return records


def write_records(filename, records):
    with open(filename, "w") as f:
        for r in records:
            f.write(SEP.join(r) + "\n")


def append_record(filename, record):
    with open(filename, "a") as f:
        f.write(SEP.join(record) + "\n")


def load_payments():
    return read_records(PAYMENTS_FILE, 7)


def load_bookings():
    return read_records(BOOKINGS_FILE, 4)


def load_services():
    return read_records(SERVICES_FILE, 3)


def to_float(text):
    try:
        value = float(text)
        return value if math.isfinite(value) else 0.0
    except (ValueError, TypeError):
        return 0.0


def field(record, index):
    return record[index] if len(record) > index else ""


def next_payment_id():
    highest = 0
    for p in load_payments():
        try:
            highest = max(highest, int(p[P_ID].upper().replace("PAY", "")))
        except ValueError:
            pass
    return "PAY" + str(highest + 1).zfill(3)


def find_booking(booking_id):
    for b in load_bookings():
        if b[B_ID].lower() == booking_id.lower():
            return b
    return None


def is_cancelled(booking):
    return "cancel" in field(booking, B_STATUS).lower()


def service_price(service_id):
    for s in load_services():
        if s[S_ID].lower() == service_id.lower():
            return to_float(s[S_PRICE])
    return None


def total_paid_for(booking_id, payments=None):
    if payments is None:
        payments = load_payments()
    return sum(to_float(p[P_AMOUNT]) for p in payments
               if p[P_BOOKING].lower() == booking_id.lower())


def recompute_statuses(booking_id):
    booking = find_booking(booking_id)
    if booking is None:
        return
    price = service_price(booking[B_SERVICE]) or 0.0
    payments = load_payments()
    running = 0.0
    for p in payments:
        if p[P_BOOKING].lower() == booking_id.lower():
            running += to_float(p[P_AMOUNT])
            p[P_STATUS] = PAID if running >= price - EPS else PARTIAL
    write_records(PAYMENTS_FILE, payments)


def ask_amount(prompt, max_amount):
    while True:
        text = input(prompt).strip()
        try:
            amount = float(text)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if not math.isfinite(amount) or amount <= 0:
            print("Amount must be more than 0.")
        elif amount > max_amount + EPS:
            print("Amount is more than the balance (RM {:.2f}).".format(max_amount))
        else:
            return round(amount, 2)


def ask_method():
    for i, m in enumerate(METHODS, 1):
        print("  {}. {}".format(i, m))
    while True:
        choice = input("Choose payment method: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(METHODS):
            return METHODS[int(choice) - 1]
        print("Invalid choice.")


def print_payments(payments):
    print("\n{:<8} {:<10} {:<10} {:>10} {:<16} {:<8} {:<10}".format(
        "PayID", "BookingID", "Customer", "Amount", "Method", "Status", "Date"))
    print("-" * 77)
    for p in payments:
        print("{:<8} {:<10} {:<10} {:>10.2f} {:<16} {:<8} {:<10}".format(
            p[P_ID], p[P_BOOKING], p[P_CUSTOMER], to_float(p[P_AMOUNT]),
            p[P_METHOD], p[P_STATUS], p[P_DATE]))


def accountant_menu():
    while True:
        print("\n========== ACCOUNTANT MENU ==========")
        print("1. Record payment")
        print("2. Update payment")
        print("3. View all payments")
        print("4. Income summary")
        print("5. Outstanding payment list")
        print("6. Monthly financial summary")
        print("0. Back")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            record_payment()
        elif choice == "2":
            update_payment()
        elif choice == "3":
            view_all_payments()
        elif choice == "4":
            generate_income_summary()
        elif choice == "5":
            view_outstanding_payments()
        elif choice == "6":
            generate_monthly_financial_summary()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")


def record_payment():
    print("\n===== RECORD PAYMENT =====")
    booking_id = input("Enter booking ID: ").strip()
    booking = find_booking(booking_id)
    if booking is None:
        print("Booking not found.")
        return
    if is_cancelled(booking):
        print("This booking was cancelled. Payment cannot be recorded.")
        return

    price = service_price(booking[B_SERVICE])
    if price is None or price <= 0:
        print("Service price not found for", booking[B_SERVICE] + ". Cannot record payment.")
        return

    paid_so_far = total_paid_for(booking[B_ID])
    balance = price - paid_so_far
    if balance <= EPS:
        print("This booking has already been fully paid.")
        return

    print("Service price : RM {:.2f}".format(price))
    print("Already paid  : RM {:.2f}".format(paid_so_far))
    print("Balance due   : RM {:.2f}".format(balance))

    amount = ask_amount("Enter amount paid (RM): ", balance)
    method = ask_method()

    status = PAID if paid_so_far + amount >= price - EPS else PARTIAL
    payment_id = next_payment_id()
    date = datetime.now().strftime("%Y-%m-%d")

    append_record(PAYMENTS_FILE, [payment_id, booking[B_ID], booking[B_CUSTOMER],
                                  "{:.2f}".format(amount), method, status, date])
    print("Payment {} recorded. Status: {}".format(payment_id, status))
    if status == PARTIAL:
        print("Remaining balance: RM {:.2f}".format(balance - amount))


def update_payment():
    print("\n===== UPDATE PAYMENT =====")
    payment_id = input("Enter payment ID (e.g. PAY001): ").strip()
    payments = load_payments()
    payment = None
    for p in payments:
        if p[P_ID].lower() == payment_id.lower():
            payment = p
            break
    if payment is None:
        print("Payment not found.")
        return

    print_payments([payment])
    print("\n1. Change amount")
    print("2. Change payment method")
    print("0. Cancel")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        booking = find_booking(payment[P_BOOKING])
        price = service_price(booking[B_SERVICE]) if booking else None
        if price is None or price <= 0:
            print("Service price not found. Cannot change amount.")
            return
        others = total_paid_for(payment[P_BOOKING], payments) - to_float(payment[P_AMOUNT])
        max_allowed = price - others
        print("Maximum allowed for this payment: RM {:.2f}".format(max_allowed))
        payment[P_AMOUNT] = "{:.2f}".format(ask_amount("Enter new amount (RM): ", max_allowed))
    elif choice == "2":
        payment[P_METHOD] = ask_method()
    elif choice == "0":
        print("Update cancelled.")
        return
    else:
        print("Invalid choice.")
        return

    write_records(PAYMENTS_FILE, payments)
    recompute_statuses(payment[P_BOOKING])
    print("Payment {} updated.".format(payment[P_ID]))


def view_all_payments():
    print("\n===== ALL PAYMENTS =====")
    payments = load_payments()
    if not payments:
        print("No payment records found.")
        return
    print_payments(payments)
    print("\nTotal records:", len(payments))


def generate_income_summary():
    print("\n===== INCOME SUMMARY =====")
    payments = load_payments()
    if not payments:
        print("No payment records found.")
        return

    total_income = 0.0
    by_method = {}
    for p in payments:
        amount = to_float(p[P_AMOUNT])
        total_income += amount
        by_method[p[P_METHOD]] = by_method.get(p[P_METHOD], 0.0) + amount

    fully_paid = len(set(p[P_BOOKING].lower() for p in payments if p[P_STATUS] == PAID))
    outstanding, total_due = get_outstanding(payments)

    print("Total transactions      :", len(payments))
    print("Bookings fully paid     :", fully_paid)
    print("Total income received   : RM {:.2f}".format(total_income))
    print("Total outstanding       : RM {:.2f}".format(total_due))
    print("\nIncome by payment method:")
    for method, amt in sorted(by_method.items()):
        print("  {:<16} RM {:.2f}".format(method, amt))


def get_outstanding(payments):
    services = {s[S_ID].lower(): to_float(s[S_PRICE]) for s in load_services()}
    rows = []
    total_due = 0.0
    for b in load_bookings():
        if is_cancelled(b):
            continue
        price = services.get(b[B_SERVICE].lower(), 0.0)
        paid = total_paid_for(b[B_ID], payments)
        due = price - paid
        if due > EPS:
            rows.append((b, price, paid, due))
            total_due += due
    return rows, total_due


def view_outstanding_payments():
    print("\n===== OUTSTANDING PAYMENTS =====")
    rows, total_due = get_outstanding(load_payments())
    if not rows:
        print("No outstanding payments.")
        return

    print("\n{:<10} {:<10} {:<10} {:<12} {:>9} {:>9} {:>9}".format(
        "BookingID", "Customer", "Service", "Date", "Price", "Paid", "Due"))
    print("-" * 74)
    for b, price, paid, due in rows:
        print("{:<10} {:<10} {:<10} {:<12} {:>9.2f} {:>9.2f} {:>9.2f}".format(
            b[B_ID], b[B_CUSTOMER], b[B_SERVICE], field(b, B_DATE), price, paid, due))
    print("\nBookings with balance :", len(rows))
    print("Total due             : RM {:.2f}".format(total_due))


def generate_monthly_financial_summary():
    print("\n===== MONTHLY FINANCIAL SUMMARY =====")
    month = input("Enter month (YYYY-MM): ").strip()
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid format. Use YYYY-MM.")
        return

    payments = [p for p in load_payments() if p[P_DATE].startswith(month)]
    if not payments:
        print("No payments found for", month)
        return

    income = sum(to_float(p[P_AMOUNT]) for p in payments)
    settled = sum(1 for p in payments if p[P_STATUS] == PAID)
    by_method = {}
    for p in payments:
        by_method[p[P_METHOD]] = by_method.get(p[P_METHOD], 0.0) + to_float(p[P_AMOUNT])

    print_payments(payments)
    print("\nSummary for", month)
    print("Transactions          :", len(payments))
    print("Payments completing a booking :", settled)
    print("Partial payments      :", len(payments) - settled)
    print("Total income          : RM {:.2f}".format(income))
    print("Average per payment   : RM {:.2f}".format(income / len(payments)))
    print("Income by method:")
    for method, amt in sorted(by_method.items()):
        print("  {:<16} RM {:.2f}".format(method, amt))


if __name__ == "__main__":
    accountant_menu()