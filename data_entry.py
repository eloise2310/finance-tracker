from datetime import datetime

date_format = "%d/%m/%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        today = datetime.today().strftime(date_format)
        print(f"Using today's date: {today}")  # Debugging: print today's date
        return today
    
    try:
        valid_date = datetime.strptime(date_str, date_format)
        print(f"Valid date entered: {valid_date.strftime(date_format)}")  # Debugging: print the valid date
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter the date in dd/mm/yyyy: ")
        return get_date(prompt, allow_default)

def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        print(f"Valid category: {CATEGORIES[category]}")  # Debugging: print the valid category
        return CATEGORIES[category]
    else:
        print("Invalid category. Please enter 'I' for Income or 'E' for Expense: ")
        return get_category()

def get_description():
    description = input("Enter a description: ")
    print(f"Description entered: {description}")  # Debugging: print the description
    return description

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be more than £0.00: ")
        print(f"Amount entered: £{amount:.2f}")  # Debugging: print the amount
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

