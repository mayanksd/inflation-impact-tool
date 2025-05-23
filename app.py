import streamlit as st

# --- Custom CSS to Fix Number Input Red Border and Add Green Focus ---
st.markdown("""
    <style>
    /* Button hover to green */
    div.stButton > button:hover {
        background-color: #2ecc71 !important;
        color: white !important;
    }

    /* Dropdown focus green border */
    div[data-baseweb="select"] > div:focus-within {
        border-color: #2ecc71 !important;
        box-shadow: 0 0 0 0.2rem rgba(46, 204, 113, 0.25);
    }

    /* Remove red border from dropdown */
    div[data-baseweb="select"] > div {
        border-color: #ccc !important;
    }

    /* Fix for Streamlit number input red border */
    div[data-testid="stNumberInput"] > div {
        border: 2px solid #ccc !important;
        border-radius: 8px;
    }

    /* Apply green focus style when number input is active */
    div[data-testid="stNumberInput"] > div:focus-within {
        border: 2px solid #2ecc71 !important;
        box-shadow: 0 0 0 0.2rem rgba(46, 204, 113, 0.25);
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
    "Monthly Rent",
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

# --- Monthly Expense Inputs with ₹ Symbol and Visible Hints ---
hints = {
    "Rent": None,
    "Groceries & Household Supplies": "📝 Includes vegetables, milk, bread, and also toilet roll, spices, cleaning items etc.",
    "Weekend Entertainment": "📝 Movies, eating out, clubbing, etc.",
    "Vacation": "📝 Annual cost of 2-3 domestic + 1-2 international vacations divided by 12.",
    "Househelp": "📝 Maid, cook, nanny, gardener, car washer, caretaker, etc.",
    "Healthcare": "📝 Insurance premiums, doctor visits, medicines, supplements, etc.",
    "Pet Expenses": "📝 Food, vet visits, grooming, toys, litter etc.",
    "Education": "📝 Kids’ education + your own upskilling/learning expenses.",
    "Subscriptions": "📝 Netflix, Prime, Swiggy One, Zomato Gold, OpenAI, Canva, etc.",
    "Utilities": "📝 Mobile, broadband, gas, electricity, water, etc."
}

for category in categories:
    monthly_expenses[category] = st.number_input(f"₹ {category}", min_value=0, step=100)
    if hints.get(category):
        st.caption(hints[category])


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
