#this code is a filechecker, that checks files for phone numbers and emails
import os
import re
import openpyxl
from docx import Document

#strip takes away quotes and spaces from the input
file_path = input("Enter the path to the file you want to check: ").strip('&').strip('"').strip("'")
file_path = os.path.normpath(file_path)

print(f"Checking file: {file_path}")

#Wordt gebruikt om te controleren of er een telefoonnummer of email is gevonden
found_any_phone = False
found_any_email = False

#leest het bestand uit, kijkt eerst naar bestand type
def check_file(file_path=file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Handle Excel files
    elif file_path.endswith(".xlsx"):
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
                                found_any_phone = True
                            for email in emails:
                                print(f"Email found: {email}")
                                found_any_email = True

        except Exception as e:
            print(f"Error reading Excel file: {e}")
    
    # Handle Word files
    elif file_path.endswith(".word") or file_path.endswith(".docx"):
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                text = para.text
                phone_numbers = find_phone_numbers(text)
                emails = find_emails(text)

                for number in phone_numbers:
                    print(f"Phone number found: {number}")
                    found_any_phone = True
                for email in emails:
                    print(f"Email found: {email}")
                    found_any_email = True

        except Exception as e:
            print(f"Error reading Word file: {e}")
            
    else:
        # Handle plain text files?
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
    phone_pattern = r'\+06\d{7,9}|\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
    return re.findall(phone_pattern, content)

def find_emails(content):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, content)

# Ensure correct main execution
if __name__ == "__main__":
    try:
        check_file(file_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure the file path is correct and the file is accessible.")