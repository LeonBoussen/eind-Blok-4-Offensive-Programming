#this code is a filechecker, that checks files for phone numbers and emails
import os
import re
import openpyxl

#strip takes away quotes and spaces from the input
file_path = input("Enter the path to the file you want to check: ").strip('&').strip('"').strip("'")
#line below is temorary and overwrites the input for testing purposes, can be commented and uncommented
#file_path = "C:\Users\gijsd\OneDrive\Laptop Desktop\eind-Blok-4-Offensive-Programming\Fake_Contact_List.xlsx"
print(f"Checking file: {file_path}")

def check_file(file_path=file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Handle Excel files
    if file_path.endswith(".xlsx"):
        try:
            workbook = openpyxl.load_workbook(file_path)
            for sheet in workbook.worksheets:
                for row in sheet.iter_rows(values_only=True):
                    for cell in row:
                        if cell is not None:
                            text = str(cell)
                            phone_numbers = find_phone_numbers(text)
                            emails = find_emails(text)

                            for number in phone_numbers:
                                print(f"Phone number found: {number}")
                            for email in emails:
                                print(f"Email found: {email}")
        except Exception as e:
            print(f"Error reading Excel file: {e}")
    
    else:
        # Handle plain text files
        with open(file_path, 'r') as file:
            content = file.read()
            phone_numbers = find_phone_numbers(content)
            emails = find_emails(content)

            if phone_numbers:
                print("Phone numbers found:")
                for number in phone_numbers:
                    print(number)
            else:
                print("No phone numbers found.")

            if emails:
                print("Emails found:")
                for email in emails:
                    print(email)
            else:
                print("No emails found.")

def find_phone_numbers(content):
    phone_pattern = r'\+06\d{8}|\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
    return re.findall(phone_pattern, content)

def find_emails(content):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, content)

if __name__ == "_main_":
    try:
        check_file()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure the file path is correct and the file is accessible.")