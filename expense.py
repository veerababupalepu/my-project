import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Create the expenses table
cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
''')
conn.commit()

# Add a new expense
def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (Food, Travel, etc.): ")
    amount = float(input("Enter amount: "))
    description = input("Enter description (optional): ")

    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                   (date, category, amount, description))
    conn.commit()
    print("✅ Expense added!\n")

# Show summary by month and category
def show_summary():
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    if df.empty:
        print("⚠️ No expenses found.\n")
        return

    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    summary = df.groupby(['month', 'category'])['amount'].sum().unstack(fill_value=0)
    print("\n📊 Expense Summary:")
    print(summary.round(2), "\n")

# Plot monthly spending
def plot_expenses():
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    if df.empty:
        print("⚠️ No expenses to plot.\n")
        return

    df['date'] = pd.to_datetime(df['date'])
    monthly_total = df.groupby(df['date'].dt.to_period('M'))['amount'].sum()

    monthly_total.plot(kind='bar', color='skyblue')
    plt.title("📈 Monthly Spending")
    plt.xlabel("Month")
    plt.ylabel("Total Amount (INR)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main Menu
def menu():
    while True:
        print("======= Expense Tracker =======")
        print("1. Add Expense")
        print("2. Show Summary")
        print("3. Show Chart")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            show_summary()
        elif choice == '3':
            plot_expenses()
        elif choice == '4':
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Try again.\n")

# Run the app
if __name__ == "__main__":
    menu()
    conn.close()
