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

# --- Collapsible About Section with Emojis and Indian Flag ---
with st.expander("ℹ️ About this Tool"):
    st.markdown("""
    This calculator helps you estimate how your monthly **lifestyle expenses** will increase over the next **10 and 20 years**, based on real inflation data across 11 spending categories — built for the **Indian context** 🇮🇳.

    **What it does:**

    - 🧾 Lets you input your current monthly expenses across categories like rent, groceries, healthcare, etc.  
    - 📈 Uses real inflation trends and data-backed assumptions to project your future monthly costs  
    - 💸 Shows how much your income needs to grow annually just to maintain your lifestyle  

    Designed for working professionals and urban families in India 🇮🇳 who want to understand and plan for the **real impact of lifestyle inflation** — beyond what headline CPI numbers show.
    """)

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

# --- Monthly Expense Inputs with Compact Layout, Hints, and Indian Format Preview ---
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

# Ensure `monthly_expenses` is initialized
monthly_expenses = {}

for category in categories:
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"<div style='font-weight: 600; font-size: 1.05rem;'>₹ {category}</div>", unsafe_allow_html=True)
        if hints.get(category):
            st.markdown(f"<div style='color:gray; font-size: 0.9rem;'>{hints[category]}</div>", unsafe_allow_html=True)

        # Store the input
        value = st.number_input(
            label=f"{category}_input", 
            min_value=0, 
            step=100, 
            label_visibility="collapsed"
        )
        monthly_expenses[category] = value

    with col2:
        # Show formatted value only if > 0
        if value > 0:
            formatted_value = format_indian(value)
            st.markdown(
                f"<div style='margin-top: 38px; font-weight: 500; color: #444;'>₹ {formatted_value}</div>", 
                unsafe_allow_html=True
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


# --- Button to Calculate and Store Future Monthly Expenses in Session State ---
if st.button("🚀 Calculate Future Expenses"):
    if all(v == 0 for v in monthly_expenses.values()):
        st.warning("⚠️ Please enter at least one monthly expense before calculating.")
    else:
        # --- Store projections in session state for persistent display ---
        st.session_state["projected_10"] = sum(
            round(monthly_expenses[c] * ((1 + inflation_rates[c]/100) ** 10))
            for c in categories
        )
        st.session_state["projected_20"] = sum(
            round(monthly_expenses[c] * ((1 + inflation_rates[c]/100) ** 20))
            for c in categories
        )
        st.session_state["current_total"] = sum(monthly_expenses.values())
        st.session_state["cagr"] = round(
            ((st.session_state["projected_20"] / st.session_state["current_total"]) ** (1 / 20) - 1) * 100, 1
        )
        st.session_state["percent_10"] = round(
            (st.session_state["projected_10"] - st.session_state["current_total"]) / st.session_state["current_total"] * 100
        )
        st.session_state["percent_20"] = round(
            (st.session_state["projected_20"] - st.session_state["current_total"]) / st.session_state["current_total"] * 100
        )
        st.session_state["future_expenses_displayed"] = True


# --- Display Future Expense Output if Previously Calculated ---
if st.session_state.get("future_expenses_displayed", False):
    from datetime import datetime
    import urllib.parse

    current_year = datetime.now().year
    st.markdown("---")
    st.header("📈 Projected Monthly Lifestyle Cost")

    st.markdown(f"""
        <div style='font-size: 1.3rem; line-height: 1.8; margin-top: 20px;'>
            <p>✅ <strong>Current Monthly Expense in {current_year}:</strong> ₹ {format_indian(st.session_state["current_total"])}</p>
            <p>📆 <strong>In 10 Years:</strong> ₹ {format_indian(st.session_state["projected_10"])} 
            <span style='color: gray;'>({st.session_state["percent_10"]}% more than today)</span></p>
            <p>🔮 <strong>In 20 Years:</strong> ₹ {format_indian(st.session_state["projected_20"])} 
            <span style='color: gray;'>({st.session_state["percent_20"]}% more than today)</span></p>
            <br>
            <p>📢 <strong>Your lifestyle expenses are increasing at {st.session_state["cagr"]}% annually.</strong><br>
            You need to increase your income by at least <strong>{st.session_state["cagr"]}% every year</strong> to keep up.<br>
            <em>How much salary increment did you receive this year?</em></p>
        </div>
    """, unsafe_allow_html=True)

    # --- Social Share Buttons ---
    share_message = f"My real lifestyle inflation rate is {st.session_state['cagr']}%. Check yours: https://inflationimpact.mayankdwivedi.com/"
    wa_url = "https://wa.me/?text=" + urllib.parse.quote(share_message)
    li_url = "https://www.linkedin.com/sharing/share-offsite/?url=" + urllib.parse.quote("https://inflationimpact.mayankdwivedi.com")

    st.markdown(f"""
    <br><br>
    <a href="{wa_url}" target="_blank">
        <button style="background-color:#25D366;color:white;padding:8px 16px;border:none;border-radius:5px;margin-right:10px;cursor:pointer;">
            📤 Share on WhatsApp
        </button>
    </a>
    <a href="{li_url}" target="_blank">
        <button style="background-color:#0077b5;color:white;padding:8px 16px;border:none;border-radius:5px;cursor:pointer;">
            💼 Share on LinkedIn
        </button>
    </a>
    """, unsafe_allow_html=True)

    # --- "I don't believe this!" button ---
    if "show_examples" not in st.session_state:
        st.session_state["show_examples"] = False

    if st.button("😮 I don't believe this! (Click anyway)"):
        st.session_state["show_examples"] = True

  # --- Real-Life Inflation Examples Display (clean HTML, no code block rendering) ---
if st.session_state.get("show_examples", False):
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📉 Real-Life Impact of Inflation (2005–2025)", unsafe_allow_html=True)

    # This block is NOT indented to avoid rendering issues
    st.markdown("""
<div style='font-size: 1.05rem; line-height: 1.8; color: #eee;'>
<b>🛫 Flight: Mumbai to Delhi</b><br>
2005: ₹1,599 → 2025: ₹5,352<br>
CAGR: ~6.2%<br>
📎 <a href="https://timesofindia.indiatimes.com/business/india-business/now-fly-delhi-mumbai-for-rs-1599/articleshow/1197518.cms" target="_blank">TOI</a> | 
<a href="https://www.airindia.com/en-us/book-flights/mumbai-to-delhi-flights" target="_blank">Air India</a>
<hr>
<b>🥛 Milk (1 litre)</b><br>
2005: ₹13 → 2025: ₹30<br>
CAGR: ~4.3%<br>
📎 <a href="https://timesofindia.indiatimes.com/city/bengaluru/nandini-milk-price-hike-from-jan-14/articleshow/401859.cms" target="_blank">TOI</a> | 
<a href="https://www.hindustantimes.com/india-news/mother-dairy-hikes-milk-prices-by-up-to-rs-2-per-litre-effective-april-30" target="_blank">HT</a>
<hr>
<b>🏠 Rent: 2BHK in Bangalore</b><br>
2005: ₹5,000 → 2025: ₹35,000<br>
CAGR: ~10.2%<br>
📎 <a href="https://housing.com/rent/2bhk-flats-for-rent-in-bengaluru-karnataka" target="_blank">Housing.com</a>
<hr>
<b>🏥 Health Insurance (Annual)</b><br>
2005: ₹1,000 → 2025: ₹7,000<br>
CAGR: ~10.2%<br>
📎 <a href="https://en.wikipedia.org/wiki/Health_insurance_in_India" target="_blank">Wikipedia</a>
<hr>
<b>🎓 Private School Tuition</b><br>
2005: ₹20,000 → 2025: ₹1,00,000<br>
CAGR: ~8.4%<br>
📎 <a href="https://www.edufund.in/blog/factors-responsible-for-education-inflation" target="_blank">EduFund</a>
</div>
""", unsafe_allow_html=True)

# --- Collapsible Section: Inflation Rates Applied & References ---
with st.expander("📁 Inflation Rates Applied & References"):
    st.markdown("Below are the inflation rate assumptions used in this tool, along with links to credible sources:")

    st.markdown("**🏠 Rent (5–7%)**")
    st.markdown("- [Global Property Guide](https://www.globalpropertyguide.com/asia/india/price-history)")
    st.markdown("- [India Today: Rent Crisis](https://www.indiatoday.in/sunday-special/story/high-rent-crisis-india-real-estate-new-cities-bengaluru-delhi-ncr-mumbai-flats-2529306-2024-04-21?utm_source=chatgpt.com)")

    st.markdown("**🛒 Groceries & Household Supplies (5%)**")
    st.markdown("- [PIB – Food Inflation](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2122148)")

    st.markdown("**🎬 Weekend Entertainment (5%)**")
    st.markdown("- [CPI Data](https://www.data.gov.in/keywords/CPI)")

    st.markdown("**✈️ Vacation (8%)**")
    st.markdown("- [Reuters – India’s Travel Boom](https://www.reuters.com/breakingviews/indias-travel-boom-enters-departure-lounge-2025-02-12)")

    st.markdown("**👩‍🍳 Househelp (8%)**")
    st.markdown("- [ILO Report](https://www.ilo.org/sites/default/files/wcmsp5/groups/public/%40asia/%40ro-bangkok/%40sro-new_delhi/documents/publication/wcms_638305.pdf)")
    st.markdown("- [JobNukkad Salary Guide](https://jobnukkad.com/full-time-maid-salary-in-mumbai)")
    st.markdown("- [Glassdoor: Maid Salaries](https://www.glassdoor.co.in/Salaries/maid-salary-SRCH_KO0%2C4.htm)")

    st.markdown("**🩺 Healthcare (12–20%)**")
    st.markdown("- [Financial Express](https://www.financialexpress.com/business/healthcare/indias-healthcare-costs-to-rise-13-in-2025-beat-global-average-report/3800929)")
    st.markdown("- [Acko Health Inflation](https://www.acko.com/health-insurance/medical-inflation-in-india/)")

    st.markdown("**🐶 Pet Expenses (10%)**")
    st.markdown("- [Mordor Intelligence – Pet Market](https://www.mordorintelligence.com/industry-reports/india-pet-food-market)")
    st.markdown("- [NPR on Rising Pet Costs](https://www.npr.org/2024/07/29/nx-s1-5018032/inflation-pets-expensive-money-cost-veterinary)")
    st.markdown("- [Business Standard](https://www.business-standard.com/industry/news/online-pet-care-sales-double-fy25-small-cities-drive-demand-125041500826_1.html)")

    st.markdown("**🎓 Education (10%)**")
    st.markdown("- [Fincart – Education Inflation](https://www.fincart.com/blog/how-will-education-inflation-impact-in-the-coming-years/)")
    st.markdown("- [EduFund Blog](https://www.edufund.in/blog/factors-responsible-for-education-inflation/)")

    st.markdown("**📺 Subscriptions (10%)**")
    st.markdown("- [S&P Global – Streamer Pricing](https://www.spglobal.com/market-intelligence/en/news-insights/research/streamers-balance-growth-and-pricing-strategies-in-india)")
    st.markdown("- [TOI: YouTube Premium Prices](https://timesofindia.indiatimes.com/technology/tech-news/youtube-increases-premium-plan-prices-but-why-users-in-india-should-not-worry/articleshow/113640960.cms)")

    st.markdown("**💡 Utilities (6%)**")
    st.markdown("- [CERC – Regulatory Reference](https://en.wikipedia.org/wiki/Central_Electricity_Regulatory_Commission?utm_source=chatgpt.com)")
    st.markdown("- [PRS Blog – LPG Prices](https://prsindia.org/theprsblog/recent-rise-in-lpg-prices?page=4&per-page=1)")
    st.markdown("- [HT: Airtel & Jio Bill Impact](https://www.hindustimes.com/technology/decoding-costlier-airtel-and-jio-bills-and-what-it-means-for-india-s-5g-curve-101720036268234.html)")

    st.markdown("**🚕 Transportation (7%)**")
    st.markdown("- [BankBazaar: Petrol Price Trend](https://www.bankbazaar.com/fuel/petrol-price-trend-in-india.html)")
    st.markdown("- [Mordor: Taxi Market Report](https://www.mordorintelligence.com/industry-reports/india-taxi-market)")
    st.markdown("- [WorldData – India Inflation](https://www.worlddata.info/asia/india/inflation-rates.php)")
