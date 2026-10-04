# =============================================
# MAINTENANCE.PY
# =============================================

from util import *
from validation import *
from constants import *
from datetime import datetime

# =============================================
# MAINTENANCE STAFF MENU
# =============================================

def maintenance_menu():
    """Maintenance Staff Menu"""
    while True:
        print("\n===== MAINTENANCE STAFF MENU =====")
        print("1. Log Maintenance Record")
        print("2. Update Equipment Status")
        print("3. View Maintenance Records")
        print("4. Generate Maintenance Summary")
        print("5. Back to Main Menu")
        print("="*40)
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            log_maintenance()
        elif choice == '2':
            update_equipment_status()
        elif choice == '3':
            view_maintenance_records()
        elif choice == '4':
            generate_maintenance_summary()
        elif choice == '5':
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice!")

# =============================================
# LOG MAINTENANCE RECORD
# =============================================

def log_maintenance():
    """Log maintenance record"""
    print("\n--- LOG MAINTENANCE RECORD ---")
    
    equipment_id = input("Equipment ID: ")
    if len(equipment_id.strip()) < 1:
        print("Equipment ID cannot be empty!")
        return
    
    equipment_name = input("Equipment Name: ")
    if len(equipment_name.strip()) < 2:
        print("Equipment name too short!")
        return
    
    print("\nActivity Type:")
    print("1. Service")
    print("2. Repair")
    print("3. Replacement")
    print("4. Inspection")
    activity_choice = input("Select activity (1-4): ")
    
    activity_map = {'1': 'Service', '2': 'Repair', '3': 'Replacement', '4': 'Inspection'}
    if activity_choice not in activity_map:
        print("Invalid activity!")
        return
    
    activity = activity_map[activity_choice]
    
    date = input("Date (DD/MM/YYYY): ")
    if validate_date(date) == False:
        print("Invalid date!")
        return
    
    notes = input("Notes: ")
    staff = input("Staff Name: ")
    
    # Record banao
    # Format: EquipmentID,EquipmentName,Status,Date,Notes,Staff
    record = equipment_id + "," + equipment_name + "," + activity + "," + date + "," + notes + "," + staff
    
    # Save karo (util.py se)
    append_file(maintenance_file, record)
    
    print("\n Maintenance record logged successfully!")
    print("   Equipment: " + equipment_name)
    print("   Activity: " + activity)

# =============================================
# UPDATE EQUIPMENT STATUS
# =============================================

def update_equipment_status():
    """Update equipment status"""
    print("\n--- UPDATE EQUIPMENT STATUS ---")
    
    equipment_id = input("Enter Equipment ID to update: ")
    
    # Records read karo (util.py se)
    records = read_file(maintenance_file)
    
    if len(records) == 0:
        print("No records found!")
        return
    
    new_status = input("Enter new status (Working / Under Repair / Under Service): ")
    new_date = input("Enter update date (DD/MM/YYYY): ")
    if validate_date(new_date) == False:
        print("Invalid date!")
        return
    new_notes = input("Enter notes: ")
    
    updated_lines = []
    found = False
    
    for record in records:
        parts = record.strip().split(",")
        
        if len(parts) >= 2:
            if parts[0] == equipment_id:
                # Update karo
                parts[2] = new_status
                parts[3] = new_date
                parts[4] = new_notes
                found = True
        
        line = ",".join(parts) + "\n"
        updated_lines.append(line)
    
    if found == False:
        print("Equipment ID not found!")
        return
    
    # Save karo (util.py se)
    write_file(maintenance_file, updated_lines)
    
    print("\n Equipment status updated successfully!")

# =============================================
# VIEW MAINTENANCE RECORDS
# =============================================

def view_maintenance_records():
    """View all maintenance records"""
    print("\n--- ALL MAINTENANCE RECORDS ---")
    
    # Records read karo (util.py se)
    records = read_file(maintenance_file)
    
    if len(records) == 0:
        print("No records to display.")
        return
    
    found_any = False
    
    for line in records:
        parts = line.strip().split(",")
        
        if len(parts) < 5:
            continue
        
        found_any = True
        print("Equipment ID: " + parts[0])
        print("Equipment Name: " + parts[1])
        print("Status: " + parts[2])
        print("Last Updated: " + parts[3])
        print("Notes: " + parts[4])
        if len(parts) > 5:
            print("Staff: " + parts[5])
        print("-" * 30)
    
    if not found_any:
        print("No records to display.")

# =============================================
# GENERATE MAINTENANCE SUMMARY
# =============================================

def generate_maintenance_summary():
    """Generate maintenance summary"""
    print("\n--- MAINTENANCE SUMMARY ---")
    
    records = read_file(maintenance_file)
    
    if len(records) == 0:
        print("No records found!")
        return
    
    total = 0
    equipment_status = {}
    activities = {}
    
    for record in records:
        parts = record.strip().split(",")
        
        if len(parts) < 3:
            continue
        
        total = total + 1
        equipment_id = parts[0]
        equipment_name = parts[1]
        status = parts[2]
        
        equipment_status[equipment_name] = status
        activities[status] = activities.get(status, 0) + 1
    
    print("\nTotal Records: " + str(total))
    
    print("\nEquipment Status:")
    print("-" * 40)
    for equipment in equipment_status:
        print(equipment + ": " + equipment_status[equipment])
    
    print("\nActivity Summary:")
    print("-" * 40)
    for activity in activities:
        print(activity + ": " + str(activities[activity]))
    
    print("=" * 40)