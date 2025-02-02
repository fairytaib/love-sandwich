# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from pprint import pprint
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

    while True:
        print("Give some date pleeese\n")
        data_str = input("Enter your data here: ")
        print(f"\nData provided: {data_str}")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data

def validate_data(values):
    
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"Insert 6 Values. You provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again")
        return False

    return True

def calculate_surplus_data(sales_row):
    print("Calc Surplus")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[len(stock) -1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data
    
def update_worksheet(data, worksheet):
    print(f"Update {worksheet} Worksheet...\n")
    suprlus_worksheet = SHEET.worksheet(worksheet)
    suprlus_worksheet.append_row(data)
    print(f"{worksheet} Worksheet updated\n")

def get_last_5_sales():
    sales = SHEET.worksheet("sales")
    # column = sales.col_values(3)
    
    columns = []
    for item in range(1,7):
        column = sales.col_values(item)
        columns.append(column[-5:])

    return columns

def calculate_stockdata(data):
    new_stockdata = []

    for column in data:
        int_column = [(value) for value in column]
        average = sum(int_column / len(int_column))
        stock_num = average * 1.1
        new_stockdata.append(round(stock_num))
    
    return new_stockdata


def main():
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_sales
    stock_data = calculate_stockdata(sales_columns)
    update_worksheet(stock_data, "stock")
    

# main()

get_last_5_sales()