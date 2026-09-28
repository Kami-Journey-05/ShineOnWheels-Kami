import os
from datetime import date, datetime
from constants import *


BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_FOLDER, data_folder)


def get_file_path(filename):
    return os.path.join(DATA_FOLDER, filename)


def ensure_data_folder():
    os.makedirs(DATA_FOLDER, exist_ok=True)


def read_file(filename):
    """Read all lines from a file."""
    full_path = get_file_path(filename)

    try:
        with open(full_path, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        return []


def write_file(filename, data):
    """Replace file contents with the supplied lines."""
    ensure_data_folder()
    full_path = get_file_path(filename)

    with open(full_path, "w", encoding="utf-8") as file:
        file.writelines(data)


def append_file(filename, data):
    """Append one record to a file."""
    ensure_data_folder()
    full_path = get_file_path(filename)

    with open(full_path, "a", encoding="utf-8") as file:
        file.write(data.rstrip("\r\n") + "\n")


def create_file_if_not_exist(filename):
    """Create a missing file without erasing existing data."""
    ensure_data_folder()
    full_path = get_file_path(filename)

    with open(full_path, "a", encoding="utf-8"):
        pass


def log_operation(operation, detials):
    """Save an operation with its timestamp."""
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log_entry = timestamp + "," + operation + "," + detials
    append_file(log_file, log_entry)


def initialize_files():
    create_file_if_not_exist(services_file)
    create_file_if_not_exist(booking_file)
    create_file_if_not_exist(customer_file)
    create_file_if_not_exist(payment_file)
    create_file_if_not_exist(maintenance_file)
    create_file_if_not_exist(log_file)