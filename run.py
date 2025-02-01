# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

SHEET = GSPREAD_CLIENT.open("love-sandwich")

def get_sales_data():
    print("Give some date pleeese\n")
    data_str = input("Enter your data here: ")
    print("Invalid input")
    print(f"\nData provided: {data_str}")

    sales_data = data_str.split(",")
    
    validate_data(sales_data)

def validate_data(values):
    
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"Insert 6 Values. You provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again")



get_sales_data()