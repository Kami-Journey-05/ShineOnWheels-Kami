from constants import *
from datetime import date, datetime

def read_file(filename):
    """ read data from file"""
    full_path = data_folder + "/" + filename
    try:
        with open(full_path, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []
def write_file(filename, data):
    """To write data in file"""
    full_path = data_folder + "/" + filename
    with open(full_path, "w") as file:
        file.writelines(data)

def append_file(filename, data):
    """To add data in file"""
    full_path = data_folder + "/" + filename
    with open(full_path, "a") as file:
        file.write(data + "\n")

def create_file_if_not_exist(filename):
    """To make new if file not exist"""
    full_path = data_folder + "/" + filename
    try:
        with open(full_path, "r") as file:
            pass
    except FileNotFoundError:
        with open(full_path, 'w') as file:
            pass

def log_operation(operation, detials):
    """To do Operation log """
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log_entry = timestamp + "," + operation + "," + detials
    full_path = data_folder + log_file
    with open(full_path, "a") as file:
        file.write(log_entry + "\n")

def initialize_files():
    create_file_if_not_exist(services_file)
    create_file_if_not_exist(booking_file)
    create_file_if_not_exist(customer_file)
    create_file_if_not_exist(payment_file)
    create_file_if_not_exist(maintenance_file)
    create_file_if_not_exist(log_file)