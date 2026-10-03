from util import *
from validation import *
from constants import *
MAINTENANCE_FILE = "maintenance.txt"


# ---------------------------------------------------------
# 1. DISPLAY MAINTENANCE MENU
# ---------------------------------------------------------

def maintenance_menu():
    while True:
        print("\n===== MAINTENANCE STAFF MENU =====")
        print("1. Log Maintenance Record")
        print("2. Update Equipment Status")
        print("3. View Maintenance Records")
        print("4. Generate Maintenance Summary")
        print("5. Back to Main Menu")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            log_maintenance()
        elif choice == "2":
            update_equipment_status()
        elif choice == "3":
            view_maintenance_records()
        elif choice == "4":
            generate_maintenance_summary()
        elif choice == "5":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


# ---------------------------------------------------------
# 2. UPDATE EQUIPMENT STATUS
# ---------------------------------------------------------

def update_equipment_status():
    print("\n--- UPDATE EQUIPMENT STATUS ---")

    equipment_id = input("Enter Equipment ID to update: ")

    try:
        file = open(MAINTENANCE_FILE, "r")
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        print("No maintenance records found.")
        return

    updated_lines = []
    found = False

    for line in lines:
        parts = line.strip().split(",")
        if parts[0] == equipment_id:
            found = True
            print("Current status:", parts[2])
            new_status = input("Enter new status (Working / Under Repair / Under Service): ")
            new_date = input("Enter update date (DD/MM/YYYY): ")
            new_notes = input("Enter notes: ")

            parts[2] = new_status
            parts[3] = new_date
            parts[4] = new_notes

            line = ",".join(parts) + "\n"

        updated_lines.append(line)

    if not found:
        print("Equipment ID not found.")
        return

    file = open(MAINTENANCE_FILE, "w")
    file.writelines(updated_lines)
    file.close()

    print("Equipment status updated successfully!")


# ---------------------------------------------------------
# 3. ADD (LOG) MAINTENANCE RECORD
# ---------------------------------------------------------

def log_maintenance():
    print("\n--- LOG NEW MAINTENANCE RECORD ---")

    equipment_name = input("Enter equipment name: ")
    status = input("Enter status (Working / Under Repair / Under Service): ")
    date = input("Enter date (DD/MM/YYYY): ")
    notes = input("Enter notes: ")

    try:
        file = open(MAINTENANCE_FILE, "r")
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        lines = []

    new_id = "E" + str(len(lines) + 1)

    record = new_id + "," + equipment_name + "," + status + "," + date + "," + notes + "\n"

    file = open(MAINTENANCE_FILE, "a")
    file.write(record)
    file.close()

    print("Maintenance record logged successfully!")
    print("Equipment ID:", new_id)


# ---------------------------------------------------------
# 4. SHOW ALL MAINTENANCE RECORDS
# ---------------------------------------------------------

def view_maintenance_records():
    print("\n--- ALL MAINTENANCE RECORDS ---")

    try:
        file = open(MAINTENANCE_FILE, "r")
    except FileNotFoundError:
        print("No maintenance records found.")
        return

    found_any = False

    for line in file:
        parts = line.strip().split(",")
        found_any = True
        print("Equipment ID:", parts[0])
        print("  Equipment Name:", parts[1])
        print("  Status:", parts[2])
        print("  Last Updated:", parts[3])
        print("  Notes:", parts[4])
        print("-" * 30)

    file.close()

    if not found_any:
        print("No records to display.")


# ---------------------------------------------------------
# 5. SHOW EQUIPMENT SUMMARY
# ---------------------------------------------------------

def generate_maintenance_summary():
    print("\n--- MAINTENANCE SUMMARY REPORT ---")

    try:
        file = open(MAINTENANCE_FILE, "r")
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        print("No maintenance records found.")
        return

    total_equipment = 0
    working_count = 0
    repair_count = 0
    service_count = 0

    for line in lines:
        parts = line.strip().split(",")
        total_equipment = total_equipment + 1
        status = parts[2]

        if status == "Working":
            working_count = working_count + 1
        elif status == "Under Repair":
            repair_count = repair_count + 1
        elif status == "Under Service":
            service_count = service_count + 1

    print("Total Equipment Records:", total_equipment)
    print("Working:", working_count)
    print("Under Repair:", repair_count)
    print("Under Service:", service_count)

    print("\nEquipment needing attention:")
    needs_attention = False

    for line in lines:
        parts = line.strip().split(",")
        if parts[2] == "Under Repair" or parts[2] == "Under Service":
            needs_attention = True
            print("  -", parts[1], "(ID:", parts[0], ") Status:", parts[2])

    if not needs_attention:
        print("  None. All equipment is working fine.")


# ---------------------------------------------------------
# RUN DIRECTLY FOR TESTING
# ---------------------------------------------------------

if __name__ == "__main__":
    maintenance_menu()