import streamlit as st

# --- Custom CSS to Change Focus Color to Green ---
st.markdown(
    """
    <style>
    input:focus, select:focus, textarea:focus {
        border-color: #28a745 !important;
        outline-color: #28a745 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧮 Inflation Impact Calculator (India)")

# --- User Inputs ---
age = st.number_input("Enter your current age", min_value=18, max_value=80, step=1)
location = st.selectbox("Where do you live in India?", ["Metro", "Non-Metro"])

# --- Monthly Expense Section Header with ₹ Icon ---
st.subheader("₹ Enter Your Monthly Expenses")

monthly_expenses = {}
categories = [
    "Rent",
    "Groceries & Household Supplies",
    "Weekend Entertainment",
    "Vacation",
    "Househelp",
    "Healthcare",
    "Pet Expenses",
    "Education",
    "Subscriptions",
    "Utilities"
]

# --- Monthly Expense Inputs with ₹ Symbol Formatting ---
for category in categories:
    monthly_expenses[category] = st.number_input(f"{category}", min_value=0, step=100, format="₹%d")

# --- Inflation Rate Logic ---
inflation_rates = {
    "Rent": 7 if location == "Metro" else 5,
    "Groceries & Household Supplies": 5,
    "Weekend Entertainment": 5,
    "Vacation": 8,
    "Househelp": 8,
    "Healthcare": 12,
    "Pet Expenses": 10,
    "Education": 10,
    "Subscriptions": 10,
    "Utilities": 6
}

if age > 40:
    inflation_rates["Healthcare"] = 20
elif age > 30:
    inflation_rates["Healthcare"] = 15

st.markdown("---")
st.subheader("✅ Inflation Rates Applied:")
for category in categories:
    st.write(f"**{category}**: {inflation_rates[category]}%")
