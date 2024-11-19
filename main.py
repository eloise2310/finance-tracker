import pandas as pd 
import csv 
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "category", "description", "amount"]
    FORMAT = "%d/%m/%Y"
    
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS) 
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, category, description, amount):
        new_entry = {
            "date": date,
            "category": category,
            "description": description,
            "amount": amount
        }
        with open(cls.CSV_FILE, "a", newline ="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
                
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary: ")
            print(f"Total Income: £{total_income:.2f}")
            print(f"Total Expense: £{total_expense:.2f}")
            print(f"Total remaining: £{(total_income - total_expense):.2f}")

            return filtered_df
        

# dont need as changed to using flask method
# def add():
#     CSV.initialize_csv()
#     date = get_date("Enter the date of the transaction (dd/mm/yyyy) or enter for todays date: ", allow_default=True)
#     category = get_category()
#     description = get_description(category)
#     amount = get_amount()
#     CSV.add_entry(date, category, description, amount)

# def plot_transactions(df):
#     df.set_index("date", inplace=True)

#     income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
#     expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)
#     expense_breakdown = expense_df.groupby("description")["amount"].sum().sort_values(ascending=False)

#     plt.figure(figsize=(10, 5))
#     expense_breakdown.plot(kind="bar", color="orange")
#     plt.xlabel("Description")
#     plt.ylabel("Amount")
#     plt.title("Expense Breakdown by Category")
#     plt.xticks(rotation=45)
#     plt.grid(True)
#     plt.show()

# def main():
#     while True:
#         print("\n1. Add a new transaction")
#         print("\n2. View transactions within a time frame")
#         print("\n3. Exit")
#         choice = input("Enter your choice (1-3)")

#         if choice == "1":
#             add()
#         elif choice == "2":
#             start_date = get_date("Enter the start date (dd/mm/yyyy): ")
#             end_date = get_date("Enter the end date (dd/mm/yyyy): ")
#             df = CSV.get_transactions(start_date, end_date)
#             if input("Do you want to see a graph? (y/n): ").lower() == "y":
#                 print("Plotting transactions...")
#                 plot_transactions(df)
#         elif choice == "3":
#             print("Exiting...")
#             break
#         else:
#             print("Invalid choice, please enter 1, 2 or 3.")

# flask routes
@app.route("/")
def index():
    finance_data = []

    with open("finance_data.csv", newline="", encoding="utf-8") as csvfile:
              csvreader = csv.DictReader(csvfile)
              for row in csvreader:
                  row['amount'] = float(row['amount'])
                  finance_data.append(row)

    return render_template("index.html", data=finance_data)

# get and post methods 
@app.route("/add", methods =["GET", "POST"])

# add a transaction using POST
def add_transaction():
    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        description = request.form["description"]
        amount = request.form["amount"]

        CSV.add_entry(date, category, description, float(amount))
        return redirected(url_for("index"))
    
    return render_template("add_transaction.html") # returns back to homepage

@app.route("/filter", methods =["GET", "POST"])
def filter_transactions():
    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        start_date = datetime.strptime(start_date, "%d/%m/%Y")
        end_date = datetime.strptime(end_date, "%d/%m/%Y") # puts start and end date in correct date format

        finance_data = CSV.get_transactions(start_date, end_date)
        return render_template("index.html", data = finance_data.to_dict(orient="record"))
    
    return render_template("filter_transactions.html")

@app.route("/plot")
def plot_transactions():
    finance_data = CSV.get_transactions()
    
    df = finance_data.copy()
    df.set_index("date", inplace=True)

    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_breakdown = expense_df.groupby("description")["amount"].sum().sort_values(ascending=False)

    # Plot the expense breakdown
    plt.figure(figsize=(10, 5))
    expense_breakdown.plot(kind="bar", color="orange")
    plt.xlabel("Description")
    plt.ylabel("Amount")
    plt.title("Expense Breakdown by Category")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.savefig("static/expense_plot.png")  # Save the plot as a static image file
    plt.close()

    return render_template('plot.html', plot_url='/static/expense_plot.png')

CSV.initialize_csv()



if __name__ == "__main__":
    # main()
    app.run(debug=True)