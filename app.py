import streamlit as st
# --- Helper: Format numbers in Indian number system (₹2,50,000 etc.) ---
import re

def format_indian(number):
    x = str(number)
    pattern = re.compile(r'(\d+)(\d{3})')
    while pattern.match(x):
        x = pattern.sub(r'\1,\2', x)
    return x

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
    "Rent",
    "Groceries & Household Supplies",
    "Weekend Entertainment",
    "Vacation",
    "Househelp",
    "Healthcare",
    "Pet Expenses",
    "Education",
    "Subscriptions",
    "Utilities",
    "Transportation"
]

# --- Monthly Expense Inputs with Compact Layout and Hints ---
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
    "Utilities": "📝 Mobile, broadband, gas, electricity, water, etc.",
    "Transportation": "📝 Include taxi, auto, bus, metro, petrol expenses"
}

for category in categories:
    st.markdown(f"<div style='font-weight: 600; font-size: 1.05rem;'>₹ {category}</div>", unsafe_allow_html=True)
    if hints.get(category):
        st.markdown(f"<div style='color:gray; font-size: 0.9rem;'>{hints[category]}</div>", unsafe_allow_html=True)
    monthly_expenses[category] = st.number_input(
        label=f"{category}_input", 
        min_value=0, 
        step=100, 
        label_visibility="collapsed"
    )



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
    "Utilities": 6,
    "Transportation": 7
}

if age > 40:
    inflation_rates["Healthcare"] = 20
elif age > 30:
    inflation_rates["Healthcare"] = 15

# --- Calculate 10-Year and 20-Year Future Monthly Expenses ---
projected_expenses_10yr = {}
projected_expenses_20yr = {}
total_10yr = 0
total_20yr = 0

for category in categories:
    current = monthly_expenses[category]
    rate = inflation_rates[category] / 100

    future_10 = round(current * ((1 + rate) ** 10))
    future_20 = round(current * ((1 + rate) ** 20))

    projected_expenses_10yr[category] = future_10
    projected_expenses_20yr[category] = future_20

    total_10yr += future_10
    total_20yr += future_20

# --- Button to Calculate 10-Year and 20-Year Future Monthly Expenses ---
if st.button("🚀 Calculate Future Expenses"):
    
    # --- Compute Total Projected Monthly Expense for Year 10 and 20 ---
    projected_expenses_10yr = 0
    projected_expenses_20yr = 0

    for category in categories:
        current = monthly_expenses[category]
        rate = inflation_rates[category] / 100

        projected_10 = round(current * ((1 + rate) ** 10))
        projected_20 = round(current * ((1 + rate) ** 20))

        projected_expenses_10yr += projected_10
        projected_expenses_20yr += projected_20

    # --- Display Final Result ---
    st.markdown("---")
    st.header("📈 Projected Monthly Lifestyle Cost")

    # --- Display Current Expense ---
    from datetime import datetime
    current_total = sum(monthly_expenses.values())
    current_year = datetime.now().year
   
     # --- Compute % Increase over Current ---
    percent_10 = round((projected_expenses_10yr - current_total) / current_total * 100)
    percent_20 = round((projected_expenses_20yr - current_total) / current_total * 100)
    
    # --- Calculate CAGR (Annual Lifestyle Inflation) ---
    cagr = round(((projected_expenses_20yr / current_total) ** (1 / 20) - 1) * 100, 1)

    # --- Final Combined Output Block with Clean HTML ---
    st.markdown(f"""
        <div style='font-size: 1.3rem; line-height: 1.8; margin-top: 20px;'>
            <p>✅ <strong>Current Monthly Expense in {current_year}:</strong> ₹ {format_indian(current_total)}</p>
            <p>📆 <strong>In 10 Years:</strong> ₹ {format_indian(projected_expenses_10yr)} 
            <span style='color: gray;'>({percent_10}% more than today)</span></p>
            <p>🔮 <strong>In 20 Years:</strong> ₹ {format_indian(projected_expenses_20yr)} 
            <span style='color: gray;'>({percent_20}% more than today)</span></p>
            <br>
            <p>📢 <strong>Your lifestyle expenses are increasing at {cagr}% annually.</strong><br>
            You need to increase your income by at least <strong>{cagr}% every year</strong> to keep up.<br>
            <em>How much salary increment did you receive this year?</em></p>
        </div>
    """, unsafe_allow_html=True)
    
    # --- Styled Social Share Buttons with Brand Colors ---
    share_url = "https://inflationimpact.mayankdwivedi.com/"
    whatsapp_message = f"My real lifestyle inflation rate is {cagr}%. Check yours at: {share_url}"

    linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url={share_url}"
    whatsapp_url = f"https://api.whatsapp.com/send?text={whatsapp_message}"

    st.markdown("""
        <br>
        <div style='margin-top: 20px; display: flex; gap: 20px;'>
            <a href='{0}' target='_blank' style='
                background-color: #25D366;
                color: white;
                padding: 10px 16px;
                border-radius: 6px;
                text-decoration: none;
                font-weight: 600;
                display: inline-block;
            '>📱 Share on WhatsApp</a>

            <a href='{1}' target='_blank' style='
                background-color: #0077b5;
                color: white;
                padding: 10px 16px;
                border-radius: 6px;
                text-decoration: none;
                font-weight: 600;
                display: inline-block;
            '>🔗 Share on LinkedIn</a>
        </div>
    """.format(whatsapp_url, linkedin_url), unsafe_allow_html=True)
    
     
st.markdown("---")
st.subheader("✅ Inflation Rates Applied:")
for category in categories:
    st.write(f"**{category}**: {inflation_rates[category]}%")
