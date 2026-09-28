import csv
import math
import os

from constants import *


# Store files inside the project's data folder.
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_FOLDER, data_folder)


def load_rows(filename):
    path = os.path.join(DATA_FOLDER, filename)

    try:
        with open(path, "r", newline="", encoding="utf-8") as file:
            return [
                row for row in csv.reader(file)
                if row and any(value.strip() for value in row)
            ]
    except FileNotFoundError:
        return []
    except (OSError, UnicodeError, csv.Error) as error:
        print("Could not read file:", error)
        return None


def save_rows(filename, rows):
    path = os.path.join(DATA_FOLDER, filename)
    temporary_path = path + ".tmp"

    try:
        os.makedirs(DATA_FOLDER, exist_ok=True)

        with open(
            temporary_path, "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        os.replace(temporary_path, path)
        return True

    except (OSError, UnicodeError, csv.Error) as error:
        print("Could not save file:", error)
        return False


def ask_name(prompt):
    while True:
        value = input(prompt).strip()

        if not value:
            print("The name cannot be empty.")
        elif "," in value or '"' in value:
            print("Do not use commas or double quotes.")
        else:
            return value


def ask_positive_number(prompt, whole_number=False):
    while True:
        value = input(prompt).strip()

        try:
            if whole_number:
                number = int(value)
            else:
                number = float(value)

            if number <= 0:
                print("Enter a number greater than zero.")
                continue

            if not whole_number and not math.isfinite(number):
                print("Enter a finite number.")
                continue

            if whole_number:
                return str(number)

            rounded = round(number, 2)

            if rounded <= 0:
                print("The price must be at least RM 0.01.")
                continue

            return f"{rounded:.2f}"

        except (ValueError, OverflowError):
            print("Enter a valid positive number.")


def name_exists(rows, name, ignored_index=None):
    for index, row in enumerate(rows):
        if index == ignored_index:
            continue

        if row[0].strip().casefold() == name.casefold():
            return True

    return False


def choose_service(rows):
    if not rows:
        print("No services available.")
        return None

    print("\nAVAILABLE SERVICES")

    for number, row in enumerate(rows, start=1):
        print(str(number) + ". " + " | ".join(row))

    while True:
        choice = input("Select service number (0 to cancel): ").strip()

        try:
            number = int(choice)

            if number == 0:
                return None

            if 1 <= number <= len(rows):
                return number - 1

        except ValueError:
            pass

        print("Choose one of the listed numbers.")


def add_service():
    print("\nADD SERVICE")

    rows = load_rows(services_file)
    if rows is None:
        return

    while True:
        name = ask_name("Service name: ")

        if name_exists(rows, name):
            print("A service with this name already exists.")
        else:
            break

    price = ask_positive_number("Price (RM): ")
    duration = ask_positive_number(
        "Duration in minutes: ", whole_number=True
    )
    capacity = ask_positive_number(
        "Capacity: ", whole_number=True
    )

    print("\nName:", name)
    print("Price: RM", price)
    print("Duration:", duration, "minutes")
    print("Capacity:", capacity)

    if input("Save this service? (y/n): ").strip().lower() != "y":
        print("Cancelled.")
        return

    rows.append([name, price, duration, capacity])

    if save_rows(services_file, rows):
        print("Service saved successfully.")


def update_service():
    print("\nUPDATE SERVICE")

    rows = load_rows(services_file)
    if rows is None:
        return

    index = choose_service(rows)
    if index is None:
        return

    old_name = rows[index][0]
    print("Selected service:", old_name)

    # Bookings identify services by name.
    # Keep that name unchanged to preserve existing links.
    print("The service name stays unchanged.")

    price = ask_positive_number("New price (RM): ")
    duration = ask_positive_number(
        "New duration in minutes: ", whole_number=True
    )
    capacity = ask_positive_number(
        "New capacity: ", whole_number=True
    )

    if input("Save changes? (y/n): ").strip().lower() != "y":
        print("Cancelled.")
        return

    rows[index] = [old_name, price, duration, capacity]

    if save_rows(services_file, rows):
        print("Service updated successfully.")


def remove_service():
    print("\nREMOVE SERVICE")

    rows = load_rows(services_file)
    if rows is None:
        return

    index = choose_service(rows)
    if index is None:
        return

    name = rows[index][0]
    bookings = load_rows(booking_file)

    if bookings is None:
        return

    # Preserve services referenced by booking history.
    for booking in bookings:
        if len(booking) < 3:
            print("A booking record is incomplete.")
            print("Check booking data before deleting services.")
            return

        if booking[2].strip().casefold() == name.strip().casefold():
            print("Cannot remove this service.")
            print("It is referenced by an existing booking.")
            return

    answer = input("Remove '" + name + "'? (y/n): ").strip().lower()

    if answer != "y":
        print("Cancelled.")
        return

    del rows[index]

    if save_rows(services_file, rows):
        print("Service removed successfully.")


def display_records(title, filename, headings=None):
    rows = load_rows(filename)

    if rows is None:
        return

    print("\n" + title)
    print("-" * 70)

    if not rows:
        print("No records available.")
        return

    if headings:
        print(" | ".join(headings))
        print("-" * 70)

    for number, row in enumerate(rows, start=1):
        print(str(number) + ". " + " | ".join(row))

    print("Total records:", len(rows))


def view_all_customers():
    display_records(
        "ALL CUSTOMERS",
        customer_file,
        ["Customer ID", "Name", "Phone", "Email", "Registration date"]
    )


def view_all_bookings():
    display_records(
        "ALL BOOKINGS",
        booking_file,
        [
            "Booking ID",
            "Customer ID",
            "Service",
            "Date",
            "Time",
            "Status",
            "Amount"
        ]
    )


def view_all_payments():
    display_records(
        "ALL PAYMENTS",
        payment_file,
        ["Payment ID", "Booking ID", "Amount", "Date", "Status"]
    )


def view_all_maintenance():
    # Show every field because maintenance format is not confirmed.
    display_records("ALL MAINTENANCE RECORDS", maintenance_file)


from datetime import datetime

# Defaults for dates without a saved override; change here when agreed.
DEFAULT_OPEN = "09:00"
DEFAULT_CLOSE = "17:00"
SCHEDULE_FILE = "schedules.txt"


def parse_day(value):
    return datetime.strptime(value.strip(), "%d/%m/%Y").date()


def time_minutes(value):
    parsed = datetime.strptime(value.strip(), "%H:%M")
    return parsed.hour * 60 + parsed.minute


def clock_text(value):
    return f"{value // 60:02d}:{value % 60:02d}"


def ask_day():
    while True:
        value = input("Date (DD/MM/YYYY, 0 to cancel): ").strip()
        if value == "0":
            return None
        try:
            return parse_day(value).strftime("%d/%m/%Y")
        except ValueError:
            print("Enter a valid date, for example 30/09/2026.")


def schedule_hours(day, rows):
    matches = [row for row in rows if row and parse_day(row[0]) == parse_day(day)]
    if len(matches) > 1:
        raise ValueError("Duplicate daily schedules.")
    if not matches:
        return time_minutes(DEFAULT_OPEN), time_minutes(DEFAULT_CLOSE)
    row = matches[0]
    if len(row) != 4:
        raise ValueError("Incomplete daily schedule.")
    if row[3].strip().lower() == "closed":
        return None
    if row[3].strip().lower() != "open":
        raise ValueError("Unknown schedule status.")
    start, end = time_minutes(row[1]), time_minutes(row[2])
    if end <= start:
        raise ValueError("Closing time must follow opening time.")
    return start, end


def manage_daily_schedule():
    print("\nMANAGE DAILY SCHEDULE")
    print("Default hours:", DEFAULT_OPEN, "to", DEFAULT_CLOSE)
    day = ask_day()
    if day is None:
        return
    rows = load_rows(SCHEDULE_FILE)
    if rows is None:
        return
    try:
        # Validate existing dates before replacing a record.
        others = [row for row in rows if parse_day(row[0]) != parse_day(day)]
    except (ValueError, IndexError):
        print("Check invalid dates in schedules.txt first.")
        return
    status = input("1. Set opening hours / 2. Close this day / 0. Cancel: ").strip()
    if status == "0":
        return
    if status == "2":
        record = [day, "", "", "closed"]
    elif status == "1":
        while True:
            try:
                start = time_minutes(input("Opening time (HH:MM): "))
                end = time_minutes(input("Closing time (HH:MM): "))
                if end <= start:
                    raise ValueError
                break
            except ValueError:
                print("Use valid same-day hours; closing must follow opening.")
        record = [day, clock_text(start), clock_text(end), "open"]
    else:
        print("Invalid choice.")
        return
    # Do not silently strand existing reservations on a changed day.
    bookings = load_rows(booking_file)
    if bookings is None:
        return
    try:
        for booking in bookings:
            if len(booking) < 6:
                raise ValueError
            if booking[5].strip().casefold() in ("cancelled", "canceled"):
                continue
            if parse_day(booking[3]) == parse_day(day):
                print("This day has bookings. Resolve them before changing its schedule.")
                return
    except ValueError:
        print("Check incomplete or invalid booking dates first.")
        return
    print("Proposed schedule:", " | ".join(record))
    if input("Save schedule? (y/n): ").strip().lower() == "y":
        if save_rows(SCHEDULE_FILE, others + [record]):
            print("Daily schedule saved.")


def calculate_slots(service, day, bookings, hours):
    duration, capacity = int(service[2]), int(service[3])
    if duration <= 0 or capacity <= 0:
        raise ValueError("Invalid service duration or capacity.")
    if hours is None:
        return []
    opening, closing = hours
    intervals = []
    for booking in bookings:
        if len(booking) < 6:
            raise ValueError("Incomplete booking record.")
        if booking[5].strip().casefold() in ("cancelled", "canceled"):
            continue
        if parse_day(booking[3]) != parse_day(day):
            continue
        if booking[2].strip().casefold() != service[0].strip().casefold():
            continue
        start = time_minutes(booking[4])
        intervals.append((start, start + duration))
    slots = []
    for start in range(opening, closing - duration + 1, duration):
        end = start + duration
        # Peak simultaneous use, including bookings starting off the slot grid.
        points = [start] + [a for a, b in intervals if start < a < end]
        peak = max(sum(a <= point < b for a, b in intervals) for point in points)
        slots.append((start, end, max(0, capacity - peak)))
    return slots


def view_available_slots(day=None):
    print("\nAVAILABLE TIME SLOTS")
    if day is None:
        day = ask_day()
    if day is None:
        return
    services = load_rows(services_file)
    bookings = load_rows(booking_file)
    schedules = load_rows(SCHEDULE_FILE)
    if any(rows is None for rows in (services, bookings, schedules)):
        return
    try:
        hours = schedule_hours(day, schedules)
        results = [(service[0], calculate_slots(service, day, bookings, hours))
                   for service in services]
    except (ValueError, IndexError) as error:
        print("Availability could not be calculated. Check data:", error)
        return
    print("Date:", day)
    if hours is None:
        print("Closed for this day.")
        return
    print("Hours:", clock_text(hours[0]), "to", clock_text(hours[1]))
    print("Capacity is per service. Existing bookings use the current service duration.")
    total = 0
    for name, slots in results:
        print("\n" + name)
        if not slots:
            print("No full service slot fits in these hours.")
        for start, end, remaining in slots:
            print(clock_text(start), "-", clock_text(end), "| Available places:", remaining)
            total += remaining
    if not services:
        print("No services available.")
    print("Total available booking places:", total)



def generate_overall_report():
    services = load_rows(services_file)
    customers = load_rows(customer_file)
    bookings = load_rows(booking_file)
    payments = load_rows(payment_file)
    maintenance = load_rows(maintenance_file)

    datasets = [services, customers, bookings, payments, maintenance]

    if any(rows is None for rows in datasets):
        print("Report cancelled because a file could not be read.")
        return

    revenue = 0.0
    invalid_payments = 0

    for payment in payments:
        if len(payment) < 5:
            invalid_payments += 1
            continue

        try:
            amount = float(payment[2])

            if not math.isfinite(amount) or amount < 0:
                raise ValueError

        except (ValueError, OverflowError):
            invalid_payments += 1
            continue

        if payment[4].strip().casefold() == "completed":
            revenue += amount

    print("\nOVERALL REPORT")
    print("=" * 50)
    print("Service packages:", len(services))
    print("Customers:", len(customers))
    print("Total bookings:", len(bookings))
    print("Payment records:", len(payments))
    print("Maintenance records:", len(maintenance))
    print(f"Revenue from completed payments: RM {revenue:.2f}")

    if invalid_payments:
        print("Payment records excluded:", invalid_payments)
        print("Revenue may be incomplete; check payment data.")

    print("\nBookings by status:")

    status_counts = {}

    for booking in bookings:
        if len(booking) >= 6:
            status = booking[5].strip() or "Unknown"
        else:
            status = "Incomplete record"

        status_counts[status] = status_counts.get(status, 0) + 1

    if not status_counts:
        print("No bookings available.")

    for status, count in status_counts.items():
        print(status + ":", count)

    print("\nService capacity settings:")

    if not services:
        print("No services available.")

    for service in services:
        if len(service) >= 4:
            print(service[0] + ":", service[3])
        else:
            print(service[0] + ": capacity not recorded")

    view_available_slots()
    print("=" * 50)


def admin_menu():
    while True:
        print("\nADMIN MENU")
        print("=" * 40)
        print("1. Add service")
        print("2. Update service")
        print("3. Remove service")
        print("4. View all customers")
        print("5. View all bookings")
        print("6. View all payments")
        print("7. View all maintenance")
        print("8. Generate overall report")
        print("9. Manage daily schedule")
        print("10. View available slots")
        print("0. Back / Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_service()
        elif choice == "2":
            update_service()
        elif choice == "3":
            remove_service()
        elif choice == "4":
            view_all_customers()
        elif choice == "5":
            view_all_bookings()
        elif choice == "6":
            view_all_payments()
        elif choice == "7":
            view_all_maintenance()
        elif choice == "8":
            generate_overall_report()
        elif choice == "9":
            manage_daily_schedule()
        elif choice == "10":
            view_available_slots()
        elif choice == "0":
            print("Leaving admin menu.")
            return
        else:
            print("Invalid choice. Enter a number from 0 to 10.")

        input("Press Enter to return to the admin menu...")


if __name__ == "__main__":
    admin_menu()