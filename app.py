import streamlit as st

# --- Custom CSS for Green Focus and Hover Styles ---
st.markdown("""
    <style>
    /* Button hover to green */
    div.stButton > button:hover {
        background-color: #2ecc71 !important;
        color: white !important;
    }

    /* Dropdown hover and focus border color */
    div[data-baseweb="select"] > div:focus-within {
        border-color: #2ecc71 !important;
        box-shadow: 0 0 0 0.2rem rgba(46, 204, 113, 0.25);
    }

    /* Remove red outline on dropdown */
    div[data-baseweb="select"] > div {
        border-color: #ccc;
    }

    /* Textbox (number_input) green focus border */
    input:focus {
        border: 2px solid #2ecc71 !important;
        box-shadow: 0 0 0 0.2rem rgba(46, 204, 113, 0.25) !important;
    }
    </style>
""", unsafe_allow_html=True)

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

# --- Monthly Expense Inputs with ₹ in Label ---
for category in categories:
    monthly_expenses[category] = st.number_input(f"₹ {category}", min_value=0, step=100)

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
