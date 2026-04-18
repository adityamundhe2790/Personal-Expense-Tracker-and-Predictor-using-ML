# Expense Tracker App

# Personal Expense Tracker with Machine Learning Forecasting

## Overview

This project is an end-to-end **data-driven personal finance dashboard** built using Python and Streamlit. It enables users to monitor expenses, analyze financial behavior, and generate future expense forecasts using machine learning techniques.

The application integrates data processing, SQL-based analysis, interactive visualization, and predictive modeling into a single unified interface.

---

## Key Features

* Interactive dashboard for real-time financial monitoring
* Category-wise and temporal expense analysis
* SQL-based querying for structured data insights
* Dynamic filtering (category and transaction type)
* Machine learning–based expense forecasting
* Clean, responsive dark-themed user interface

---

## Tech Stack

* **Frontend / UI:** Streamlit
* **Data Processing:** Pandas, NumPy
* **Database:** SQLite
* **Visualization:** Plotly, Matplotlib
* **Machine Learning:** Scikit-learn (Linear Regression)

---

## Machine Learning Approach

A regression-based model is implemented to forecast future expenses:

* Feature engineering using time-based transformation (date → numerical scale)
* Model: Linear Regression
* Prediction horizon: Next 30 days
* Post-processing applied to ensure realistic variability and non-negative outputs

This provides a baseline predictive layer for financial planning.

---

## Project Structure

```
Personal-Expense-Tracker/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── expenses.csv
│   └── expenses.db
│
├── outputs/
│   ├── category_spending.png
│   ├── expense_pie.png
│   └── monthly_trend.png
│
├── screenshots/
│   ├── dashboard.png
│   ├── ml_prediction.png
│   └── filters.png
```

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/Personal-Expense-Tracker.git
cd Personal-Expense-Tracker
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app.py
```

---

## Future Scope

* Integration of advanced time-series models (ARIMA, LSTM)
* User authentication and personalized dashboards
* Cloud deployment for public access
* Budget optimization and recommendation system

---

## Author

Aditya Mundhe

---

## License

This project is open-source and available for academic and learning purposes.

