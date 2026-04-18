# ============================================
# 💰 Expense Tracker - Main Script (FINAL)
# ============================================

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import os

# -------------------------
# 1. CREATE REALISTIC DATASET
# -------------------------
np.random.seed(42)

dates = pd.date_range(start="2024-01-01", periods=200)

data = []

for date in dates:

    # 💰 Monthly Salary (1st of every month)
    if date.day == 1:
        data.append([date, "Salary", np.random.randint(30000, 60000), "Income"])

    # 💸 Daily Expenses
    num_expenses = np.random.randint(1, 4)

    for _ in range(num_expenses):
        category = np.random.choice(['Food','Travel','Bills','Shopping','Rent'])
        amount = np.random.randint(100, 3000)
        data.append([date, category, amount, "Expense"])

# Create DataFrame
df = pd.DataFrame(data, columns=["Date", "Category", "Amount", "Type"])

# Save CSV
os.makedirs("data", exist_ok=True)
df.to_csv("data/expenses.csv", index=False)

print("✅ Realistic dataset created!")
print(df.head())


# -------------------------
# 2. CONNECT TO SQLITE DATABASE
# -------------------------
conn = sqlite3.connect("data/expenses.db")

df.to_sql("expenses", conn, if_exists="replace", index=False)

print("✅ Data stored in SQLite database successfully!")


# -------------------------
# 3. SQL ANALYSIS
# -------------------------

# 📊 Category-wise Spending
query1 = """
SELECT Category, SUM(Amount) as Total_Spending
FROM expenses
WHERE Type = 'Expense'
GROUP BY Category
ORDER BY Total_Spending DESC
"""
df_category = pd.read_sql(query1, conn)

print("\n📊 Category-wise Spending:")
print(df_category)


# 💰 Income vs Expense
query2 = """
SELECT Type, SUM(Amount) as Total
FROM expenses
GROUP BY Type
"""
df_type = pd.read_sql(query2, conn)

print("\n💰 Income vs Expense:")
print(df_type)


# 📈 Monthly Trend
query3 = """
SELECT strftime('%m', Date) as Month, SUM(Amount) as Total
FROM expenses
WHERE Type = 'Expense'
GROUP BY Month
ORDER BY Month
"""
df_month = pd.read_sql(query3, conn)

print("\n📈 Monthly Spending Trend:")
print(df_month)


# -------------------------
# 4. VISUALIZATION
# -------------------------
os.makedirs("outputs", exist_ok=True)

# 📊 Bar Chart
plt.figure(figsize=(8,5))
plt.bar(df_category['Category'], df_category['Total_Spending'])
plt.title("Category-wise Spending")
plt.xlabel("Category")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/category_spending.png")
plt.close()


# 🥧 Pie Chart
plt.figure(figsize=(6,6))
plt.pie(df_category['Total_Spending'],
        labels=df_category['Category'],
        autopct='%1.1f%%')
plt.title("Expense Distribution")
plt.savefig("outputs/expense_pie.png")
plt.close()


# 📈 Line Chart
plt.figure(figsize=(8,5))
plt.plot(df_month['Month'], df_month['Total'], marker='o')
plt.title("Monthly Expense Trend")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.grid()
plt.savefig("outputs/monthly_trend.png")
plt.close()

print("✅ Charts saved in outputs folder!")