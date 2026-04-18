import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(layout="wide")

# -------------------------
# 🔥 INSANE UI CSS
# -------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 20% 20%, #1a0b2e, #0f0c29 60%);
    color: white;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b021a, #14052c);
    border-right: 1px solid rgba(255,255,255,0.05);
}
.card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0px 0px 30px rgba(138, 43, 226, 0.25);
    transition: 0.3s;
}
.card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0px 0px 40px rgba(168, 85, 247, 0.6);
}
.metric {
    font-size: 24px;
    font-weight: bold;
    color: #f5d0fe;
}
.small {
    color: #c084fc;
}
h1, h2, h3 {
    color: #e9d5ff;
}
.stButton>button {
    background: linear-gradient(135deg, #7c3aed, #c026d3);
    border-radius: 12px;
    color: white;
}
.block-container {
    padding: 2rem 3rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("data/expenses.csv")
df['Date'] = pd.to_datetime(df['Date'])

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("💰 Expense Tracker")

menu = st.sidebar.radio("Navigation", ["Dashboard", "Transactions"])

category = st.sidebar.multiselect(
    "Category",
    df['Category'].unique(),
    default=df['Category'].unique()
)

type_filter = st.sidebar.selectbox(
    "Type",
    ["All", "Expense", "Income"]
)

filtered = df[df['Category'].isin(category)]

if type_filter != "All":
    filtered = filtered[filtered['Type'] == type_filter]

# -------------------------
# ✅ UPDATED KPI FUNCTION
# -------------------------
def kpi_card(title, value, icon, is_currency=True):

    if is_currency:
        value_display = f"₹ {value:,.0f}"
    else:
        value_display = f"{int(value)}"

    return f"""
    <div class="card">
        <div class="small">{icon} {title}</div>
        <div class="metric">{value_display}</div>
    </div>
    """

# -------------------------
# DASHBOARD
# -------------------------
if menu == "Dashboard":

    st.markdown("""
    <h1 style='text-shadow:0 0 20px rgba(168,85,247,0.7);'>
    📊 Dashboard
    </h1>
    """, unsafe_allow_html=True)

    total_expense = filtered[filtered['Type']=="Expense"]['Amount'].sum()
    total_income = filtered[filtered['Type']=="Income"]['Amount'].sum()
    total_transactions = len(filtered)
    avg = filtered['Amount'].mean()

    # -------------------------
    # ✅ UPDATED KPI CARDS
    # -------------------------
    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(kpi_card("Total Expense", total_expense, "🔻", True), unsafe_allow_html=True)
    c2.markdown(kpi_card("Total Income", total_income, "🟢", True), unsafe_allow_html=True)
    c3.markdown(kpi_card("Transactions", total_transactions, "📊", False), unsafe_allow_html=True)
    c4.markdown(kpi_card("Average", avg, "⚡", True), unsafe_allow_html=True)

    st.markdown("##")

    # -------------------------
    # CHARTS
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📈 Expense Trend")

        trend = filtered.groupby('Date')['Amount'].sum().reset_index()
        fig = px.line(trend, x='Date', y='Amount')

        fig.update_layout(template="plotly_dark",
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          font=dict(color='white'))

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Category Distribution")

        cat = filtered.groupby('Category')['Amount'].sum().reset_index()
        fig2 = px.bar(cat, x='Category', y='Amount')

        fig2.update_layout(template="plotly_dark",
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           font=dict(color='white'))

        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------
    # PIE + INSIGHTS
    # -------------------------
    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🥧 Expense Share")

        pie = filtered[filtered['Type']=="Expense"].groupby('Category')['Amount'].sum().reset_index()
        fig3 = px.pie(pie, names='Category', values='Amount')

        fig3.update_layout(template="plotly_dark",
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           font=dict(color='white'))

        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💡 Insights")

        if not filtered.empty:
            top_cat = pie.loc[pie['Amount'].idxmax()]['Category']
            st.write(f"🔝 Top Category: **{top_cat}**")
            st.write(f"📊 Avg Transaction: ₹ {round(avg,2)}")

        st.markdown('</div>', unsafe_allow_html=True)
        # -------------------------
# 🤖 ML: FUTURE EXPENSE PREDICTION (FIXED)
# -------------------------
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.graph_objects as go

st.markdown("## 🤖 Future Expense Prediction")

# Prepare data (only expenses)
ml_df = filtered[filtered['Type'] == "Expense"].copy()

if len(ml_df) > 10:

    # Convert date to numeric
    ml_df['Days'] = (ml_df['Date'] - ml_df['Date'].min()).dt.days

    X = ml_df[['Days']]
    y = ml_df['Amount']

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Predict next 30 days
    future_days = np.arange(
        ml_df['Days'].max() + 1,
        ml_df['Days'].max() + 31
    ).reshape(-1, 1)

    predictions = model.predict(future_days)

    # 🔥 Add realistic variation
    noise = np.random.normal(0, 200, size=len(predictions))
    predictions = predictions + noise

    # 🔥 Avoid negative values
    predictions = np.maximum(predictions, 0)

    # Future dates
    future_dates = pd.date_range(
        start=ml_df['Date'].max(),
        periods=30
    )

    pred_df = pd.DataFrame({
        "Date": future_dates,
        "Predicted Expense": predictions
    })

    # Plot
    fig = go.Figure()

    # Actual
    fig.add_trace(go.Scatter(
        x=ml_df['Date'],
        y=ml_df['Amount'],
        mode='lines',
        name='Actual'
    ))

    # Predicted
    fig.add_trace(go.Scatter(
        x=pred_df['Date'],
        y=pred_df['Predicted Expense'],
        mode='lines',
        name='Predicted',
        line=dict(dash='dash')
    ))

    fig.update_layout(
        template="plotly_dark",
        title="Future Expense Forecast",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Not enough data for prediction")

    # -------------------------
    # RECENT TRANSACTIONS
    # -------------------------
    st.markdown("### 📋 Recent Transactions")
    st.dataframe(filtered.tail(10), use_container_width=True)

# -------------------------
# TRANSACTIONS PAGE
# -------------------------
if menu == "Transactions":
    st.title("📋 Transactions")
    st.dataframe(filtered, use_container_width=True)