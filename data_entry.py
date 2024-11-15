from datetime import datetime

date_format = "%d/%m/%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}
EXPENSE_DESCRIPTIONS = [
    "Food", "Entertainment", "Subscriptions", "Bills", "Petrol", 
    "Transport", "Healthcare", "Shopping", "Other"
]
INCOME_DESCRIPTIONS = [
    "Salary", "Bonus", "Gift", "Other"
]

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

def get_description(category):
    if category == "Expense":
        print("Select a description from the following options:")
        for i, desc in enumerate(EXPENSE_DESCRIPTIONS, 1):
            print(f"{i}. {desc}")
        try:
            selection = int(input(f"Enter the number of the description: "))
            if 1 <= selection <= len(EXPENSE_DESCRIPTIONS):
                description = EXPENSE_DESCRIPTIONS[selection - 1]
                print(f"Description entered: {description}")  # Debugging: print the description
                return description
            else:
                print("Invalid selection. Please enter a number between 1 and 9.")
                return get_description(category)
        except ValueError:
            print("Invalid input. Please enter a number.")
            return get_description(category)
    
    elif category == "Income":
        print("Select a description from the following options:")
        for i, desc in enumerate(INCOME_DESCRIPTIONS, 1):
            print(f"{i}. {desc}")
        try:
            selection = int(input(f"Enter the number of the description: "))
            if 1 <= selection <= len(INCOME_DESCRIPTIONS):
                description = INCOME_DESCRIPTIONS[selection - 1]
                print(f"Description entered: {description}")  # Debugging: print the description
                return description
            else:
                print("Invalid selection. Please enter a number between 1 and 4.")
                return get_description(category)
        except ValueError:
            print("Invalid input. Please enter a number.")
            return get_description(category)

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

