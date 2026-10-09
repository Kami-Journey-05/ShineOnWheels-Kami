#1. Name Validation:
def validate_name(name):
    """Length: 2+ chars, Format: letters + spaces"""
    correct_name = name.replace(" ", "")
    return correct_name.isalpha() and len(name.strip()) >=2

#2. Phone validation:
def validate_phone(phone):
    """Length: 10-12 digit, Type: numbers only"""
    corect_phone = phone.replace(" ", " ")
    return corect_phone.isdigit() and len(corect_phone) >= 10

#3. Email validation:
def validate_email(email):
    """Format: @ and . is must"""
    return "@" and "." in email

#4. Date validation:
def validate_date(date_str):
    """Date validate karo - DD/MM/YYYY format"""
    parts = date_str.split("/")
    
    if len(parts) != 3:
        return False
    
    try:
        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])
    except:
        return False
    
    if day < 1 or day > 31:
        return False
    
    if month < 1 or month > 12:
        return False
    
    if year < 2025:
        return False
    
    return True

#5. Time format:
def validate_time(time_str):
    """Format: HH:MM, Type: numbers"""
    try:
        hour, minute = time_str.split(":")
        return int(hour) >= 0 and int(hour) <= 23 and int(minute) >= 0 and int(minute) <= 59
    except:
        return False
    
#6. Price validation:
def validate_price(price):
    """Type: Positive number"""
    try:
        return float(price) > 0
    except:
        return False
    
#7. Duration validation:
def validate_duration(duration):
    """Type: positive number"""
    try:
        return int(duration) > 0
    except:
        return False
    
#8. Valid input:
def valid_input(prompt, validation_func, error_msg):
    """Untill valid input not come"""
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        print("Error: " + error_msg)