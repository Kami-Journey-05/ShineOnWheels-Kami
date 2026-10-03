from util import *
from validation import *
from constants import *

MAINTENANCE_FILE = "maintenance.txt"


def read_all_records():
    """Reads maintenance.txt and returns a list of tuples.
       Each tuple = (equipment_id, equipment_name, status, date, notes)"""
    records = []
    try:
        file = open(MAINTENANCE_FILE, "r")
        for line in file:
            parts = line.strip().split(",")
            record = (parts[0], parts[1], parts[2], parts[3], parts[4])  # tuple
            records.append(record)
        file.close()
    except FileNotFoundError:
        pass
    return records


def save_all_records(records):
    """Takes a list of tuples and rewrites maintenance.txt"""
    file = open(MAINTENANCE_FILE, "w")
    for record in records:
        line = ",".join(record) + "\n"
        file.write(line)
    file.close()


def generate_new_id(records):
    """Creates a new equipment ID based on number of existing records"""
    new_id = "E" + str(len(records) + 1)
    return new_id


def log_maintenance_record():
    print("\n--- LOG NEW MAINTENANCE RECORD ---")

    records = read_all_records()

    name = input("Enter equipment name: ")
    status = input("Enter status (Working / Under Repair / Under Service): ")
    date = input("Enter date (DD/MM/YYYY): ")
    notes = input("Enter notes: ")

    new_id = generate_new_id(records)

    new_record = (new_id, name, status, date, notes)   # tuple
    records.append(new_record)

    save_all_records(records)

    print("Record logged! Equipment ID is:", new_id)


def update_maintenance_status():
    print("\n--- UPDATE EQUIPMENT STATUS ---")

    equipment_id = input("Enter equipment ID to update: ")
    records = read_all_records()

    updated_records = []
    found = False

    for record in records:
        if record[0] == equipment_id:
            found = True
            print("Current status:", record[2])
            new_status = input("Enter new status (Working / Under Repair / Under Service): ")
            new_date = input("Enter update date: ")
            new_notes = input("Enter notes: ")

            # Build a new tuple (tuples cannot be changed directly)
            updated_record = (record[0], record[1], new_status, new_date, new_notes)
            updated_records.append(updated_record)
        else:
            updated_records.append(record)

    if not found:
        print("Equipment ID not found.")
        return

    save_all_records(updated_records)
    print("Status updated successfully!")


def view_maintenance_records():
    print("\n--- ALL MAINTENANCE RECORDS ---")

    records = read_all_records()

    if len(records) == 0:
        print("No records found.")
        return

    for record in records:
        equipment_id, name, status, date, notes = record   # unpacking a tuple
        print("Equipment ID:", equipment_id)
        print("  Name:", name)
        print("  Status:", status)
        print("  Last Updated:", date)
        print("  Notes:", notes)
        print("-" * 30)


def count_status(records):
    """Counts how many equipment are in each status.
       Returns a tuple: (working_count, repair_count, service_count)"""
    working_count = 0
    repair_count = 0
    service_count = 0

    for record in records:
        status = record[2]
        if status == "Working":
            working_count = working_count + 1
        elif status == "Under Repair":
            repair_count = repair_count + 1
        elif status == "Under Service":
            service_count = service_count + 1

    return (working_count, repair_count, service_count)   # tuple


def generate_maintenance_report():
    print("\n--- MAINTENANCE SUMMARY REPORT ---")

    records = read_all_records()

    if len(records) == 0:
        print("No records found.")
        return

    working, repair, service = count_status(records)   # unpacking tuple

    print("Total Equipment:", len(records))
    print("Working:", working)
    print("Under Repair:", repair)
    print("Under Service:", service)

    print("\nEquipment needing attention:")
    needs_attention = False

    for record in records:
        if record[2] == "Under Repair" or record[2] == "Under Service":
            needs_attention = True
            print("  -", record[1], "(ID:", record[0], ") Status:", record[2])

    if not needs_attention:
        print("  None. All equipment is working fine.")


def maintenance_menu():
    while True:
        print("\n===== MAINTENANCE STAFF MENU =====")
        print("1. Log New Maintenance Record")
        print("2. Update Equipment Status")
        print("3. View All Maintenance Records")
        print("4. Generate Maintenance Summary Report")
        print("5. Back to Main Menu")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            log_maintenance_record()
        elif choice == "2":
            update_maintenance_status()
        elif choice == "3":
            view_maintenance_records()
        elif choice == "4":
            generate_maintenance_report()
        elif choice == "5":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    maintenance_menu()