import pandas as pd 
import csv 
from datetime import datetime, timedelta
import os
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
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, cls.FORMAT)
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, cls.FORMAT)

        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)

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

# Flask routes
@app.route("/")
def index():
    finance_data = []

    with open("finance_data.csv", newline="", encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            row['amount'] = float(row['amount'])
            finance_data.append(row)

    return render_template("index.html", data=finance_data)

@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        description = request.form["description"]
        amount = request.form["amount"]

        CSV.add_entry(date, category, description, float(amount))
        return redirect(url_for("index"))
    
    return render_template("add_transaction.html")  # returns back to homepage

@app.route("/filter", methods=["GET", "POST"])
def filter_transactions():
    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        # Redirect to the plot page with the selected date range
        return redirect(url_for('filter_transactions', start_date=start_date, end_date=end_date))
    
    return render_template("filter_transactions.html")

@app.route('/plot')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

def plot_transactions():
    # Retrieve start_date and end_date from the URL parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        # Default to a fixed date range (e.g., last 30 days)
        start_date = (datetime.now() - timedelta(days=30)).strftime('%d/%m/%Y')
        end_date = datetime.now().strftime('%d/%m/%Y')

    # Fetch the transaction data
    finance_data = CSV.get_transactions(start_date, end_date)

    # Create a plot
    plt.figure(figsize=(10, 5))

    # Plot expense breakdown by description
    expense_df = finance_data[finance_data["category"] == "Expense"]
    expense_breakdown = expense_df.groupby("description")["amount"].sum().sort_values(ascending=False)
    expense_breakdown.plot(kind="bar", color="orange")

    plt.xlabel("Description")
    plt.ylabel("Amount")
    plt.title("Expense Breakdown by Category")
    plt.xticks(rotation=45)
    plt.grid(True)

    # Save the plot as an image file in the 'static' folder
    plot_path = os.path.join('static', 'transactions_plot.png')
    plt.savefig(plot_path)

    # Close the plot after saving it
    plt.close()

    # Render the template and pass the plot path to it
    return render_template('plot.html', plot_url=plot_path)

# Initialize CSV when the app starts
CSV.initialize_csv()

if __name__ == "__main__":
    app.run(debug=True)
