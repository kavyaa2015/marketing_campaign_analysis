import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Marketing Campaign Analysis",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "marketing_cleaned.csv"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    # Create Age_Band if it is not already present
    if "Age_Band" not in df.columns:
        df["Age_Band"] = pd.cut(
            df["Age"],
            bins=[0, 29, 39, 49, 59, 69, float("inf")],
            labels=[
                "<30",
                "30-39",
                "40-49",
                "50-59",
                "60-69",
                "70+"
            ]
        )

    # Create Income_Band if it is not already present
    if "Income_Band" not in df.columns:

        df["Income_Band"] = pd.cut(
            df["Income"],
            bins=[
                -float("inf"),
                30000,
                50000,
                75000,
                float("inf")
            ],
            labels=[
                "Low",
                "Medium",
                "High",
                "Very High"
            ]
        )

    return df


df = load_data()


# ============================================================
# TITLE
# ============================================================

st.title("📊 Marketing Campaign Analysis")
st.markdown(
    "### Customer Analytics Dashboard"
)

st.write(
    "This dashboard analyzes customer demographics, spending, "
    "purchasing channels, campaign performance, and customer "
    "segments to identify high-value and responsive customers."
)


# ============================================================
# OVERALL KPIs
# ============================================================

st.header("📌 Overall Business KPIs")


total_customers = len(df)

response_rate = df["Response"].mean() * 100

avg_income = df["Income"].mean()

avg_spend = df["Total_Spend"].mean()

avg_purchases = df["Total_Purchases"].mean()


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Response Rate",
    f"{response_rate:.2f}%"
)

col3.metric(
    "Average Income",
    f"{avg_income:,.0f}"
)

col4.metric(
    "Average Spend",
    f"{avg_spend:,.2f}"
)

col5.metric(
    "Avg Purchases",
    f"{avg_purchases:.2f}"
)


# ============================================================
# CAMPAIGN PERFORMANCE
# ============================================================

st.header("📢 Campaign Performance")


campaigns = {
    "Campaign 1": "AcceptedCmp1",
    "Campaign 2": "AcceptedCmp2",
    "Campaign 3": "AcceptedCmp3",
    "Campaign 4": "AcceptedCmp4",
    "Campaign 5": "AcceptedCmp5",
    "Final Response": "Response"
}


campaign_names = []
campaign_rates = []

for name, column in campaigns.items():

    campaign_names.append(name)

    campaign_rates.append(
        df[column].mean() * 100
    )


fig, ax = plt.subplots(figsize=(7, 4))

ax.bar(
    campaign_names,
    campaign_rates
)

ax.set_title(
    "Campaign Acceptance / Response Rate"
)

ax.set_ylabel("Rate (%)")

ax.tick_params(axis="x", rotation=30)

plt.tight_layout()

st.pyplot(fig, width="stretch")

plt.close(fig)


best_campaign_index = campaign_rates.index(
    max(campaign_rates)
)

best_campaign = campaign_names[best_campaign_index]

st.info(
    f"📌 **Key takeaway:** {best_campaign} has the highest "
    f"acceptance/response rate at "
    f"**{campaign_rates[best_campaign_index]:.2f}%**."
)


# ============================================================
# PRODUCT SPENDING
# ============================================================

st.header("🛍️ Product Spending Analysis")


product_columns = {
    "Wine": "MntWines",
    "Fruits": "MntFruits",
    "Meat": "MntMeatProducts",
    "Fish": "MntFishProducts",
    "Sweets": "MntSweetProducts",
    "Gold": "MntGoldProds"
}


product_totals = {
    product: df[column].sum()
    for product, column in product_columns.items()
}


product_data = pd.Series(product_totals).sort_values(
    ascending=False
)


fig, ax = plt.subplots(figsize=(7, 4))

ax.bar(
    product_data.index,
    product_data.values
)

ax.set_title(
    "Total Spending by Product Category"
)

ax.set_ylabel("Total Spending")

ax.tick_params(axis="x", rotation=30)

plt.tight_layout()

st.pyplot(fig, width="stretch")

plt.close(fig)


best_product = product_data.idxmax()

st.info(
    f"🏆 **Highest spending category:** {best_product} "
    f"with total spending of "
    f"**{product_data.max():,.0f}**."
)


# ============================================================
# PRODUCT SPENDING BY RESPONSE
# ============================================================

st.subheader("Product Spending by Campaign Response")


response_product = (
    df.groupby("Response")[
        list(product_columns.values())
    ]
    .mean()
)


response_product.index = [
    "No Response",
    "Response"
]


response_product.columns = list(
    product_columns.keys()
)


fig, ax = plt.subplots(figsize=(8, 4))

response_product.T.plot(
    kind="bar",
    ax=ax
)

ax.set_title(
    "Average Product Spending by Campaign Response"
)

ax.set_xlabel("Product")

ax.set_ylabel("Average Spending")

ax.tick_params(axis="x", rotation=30)

ax.legend(
    title="Customer Group"
)

plt.tight_layout()

st.pyplot(fig, width="stretch")

plt.close(fig)


# ============================================================
# CHANNEL ANALYSIS
# ============================================================

st.header("📱🛒 Channel Analysis")


channel_columns = {
    "Web": "NumWebPurchases",
    "Catalog": "NumCatalogPurchases",
    "Store": "NumStorePurchases",
    "Deals": "NumDealsPurchases"
}


channel_totals = {
    channel: df[column].sum()
    for channel, column in channel_columns.items()
}


channel_data = pd.Series(channel_totals).sort_values(
    ascending=False
)


fig, ax = plt.subplots(figsize=(7, 4))

ax.bar(
    channel_data.index,
    channel_data.values
)

ax.set_title(
    "Total Purchases by Channel"
)

ax.set_ylabel("Number of Purchases")

plt.tight_layout()

st.pyplot(fig, width="stretch")

plt.close(fig)


# ============================================================
# CHANNEL USAGE BY RESPONSE
# ============================================================

st.subheader("Channel Usage by Campaign Response")


channel_response = (
    df.groupby("Response")[
        list(channel_columns.values())
    ]
    .mean()
)


channel_response.index = [
    "No Response",
    "Response"
]


channel_response.columns = list(
    channel_columns.keys()
)


fig, ax = plt.subplots(figsize=(8, 4))

channel_response.T.plot(
    kind="bar",
    ax=ax
)

ax.set_title(
    "Average Channel Purchases by Campaign Response"
)

ax.set_xlabel("Channel")

ax.set_ylabel("Average Purchases")

ax.tick_params(axis="x", rotation=30)

ax.legend(
    title="Customer Group"
)

plt.tight_layout()

st.pyplot(fig, width="stretch")

plt.close(fig)


# ============================================================
# WEBSITE VISITS
# ============================================================

st.subheader("Website Visits by Campaign Response")


website_visits = (
    df.groupby("Response")[
        "NumWebVisitsMonth"
    ]
    .mean()
)


website_visits.index = [
    "No Response",
    "Response"
]


fig, ax = plt.subplots(figsize=(6, 4))

ax.bar(
    website_visits.index,
    website_visits.values
)

ax.set_title(
    "Average Website Visits per Month"
)

ax.set_ylabel("Average Visits")

plt.tight_layout()

st.pyplot(fig, width="stretch")

plt.close(fig)


# ============================================================
# CUSTOMER SEGMENTATION
# ============================================================

st.header("👥 Customer Segmentation")


# High Spender
high_spender_threshold = df["Total_Spend"].quantile(0.90)

# Create rule-based segment
def assign_segment(row):

    if row["Total_Spend"] > high_spender_threshold:
        return "High Spender"

    elif row["Income"] > 75000:
        return "High Income"

    elif row["Age"] < 30:
        return "Young Customer"

    elif row["Response"] == 1:
        return "Campaign Responder"

    elif row["NumWebVisitsMonth"] > 5:
        return "High Web Engagement"

    elif row["Total_Children"] > 0:
        return "Family Customer"

    else:
        return "Other"


df["Segment"] = df.apply(
    assign_segment,
    axis=1
)


segment_summary = (
    df.groupby("Segment")
    .agg(
        Customers=("ID", "count"),
        Average_Income=("Income", "mean"),
        Average_Spend=("Total_Spend", "mean"),
        Response_Rate=("Response", "mean")
    )
    .reset_index()
)


segment_summary["Response_Rate"] *= 100


# Segment size
fig, ax = plt.subplots(figsize=(8, 4))

segment_size = (
    segment_summary
    .sort_values("Customers", ascending=False)
)


ax.bar(
    segment_size["Segment"],
    segment_size["Customers"]
)

ax.set_title(
    "Customer Count by Segment"
)

ax.set_ylabel("Customers")

ax.tick_params(axis="x", rotation=30)

plt.tight_layout()

st.pyplot(fig, width="stretch")

plt.close(fig)


# Segment response
st.subheader("Response Rate by Customer Segment")


segment_response = (
    segment_summary
    .sort_values(
        "Response_Rate",
        ascending=False
    )
)


fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    segment_response["Segment"],
    segment_response["Response_Rate"]
)

ax.set_title(
    "Response Rate by Customer Segment"
)

ax.set_ylabel("Response Rate (%)")

ax.tick_params(axis="x", rotation=30)

plt.tight_layout()

st.pyplot(fig, width="stretch")

plt.close(fig)


# ============================================================
# HIGH-VALUE CUSTOMERS
# ============================================================

st.header("💎 High-Value Customer Analysis")


high_value = df[
    df["Total_Spend"] >= high_spender_threshold
]


other_customers = df[
    df["Total_Spend"] < high_spender_threshold
]


hv_count = len(high_value)

hv_spend = high_value["Total_Spend"].mean()

hv_income = high_value["Income"].mean()

hv_response = high_value["Response"].mean() * 100


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "High-Value Customers",
    f"{hv_count:,}"
)

col2.metric(
    "Avg High-Value Spend",
    f"{hv_spend:,.2f}"
)

col3.metric(
    "Avg High-Value Income",
    f"{hv_income:,.2f}"
)

col4.metric(
    "High-Value Response Rate",
    f"{hv_response:.2f}%"
)


# ============================================================
# CUSTOMER PROFILE
# ============================================================

st.header("🌍 Customer Profile")


# ------------------------------------------------------------
# COUNTRY
# ------------------------------------------------------------

st.subheader("Customer Performance by Country")


country_summary = (
    df.groupby("Country")
    .agg(
        Customers=("ID", "count"),
        Response_Rate=("Response", "mean"),
        Average_Spend=("Total_Spend", "mean")
    )
    .reset_index()
)


country_summary["Response_Rate"] *= 100


country_summary = country_summary.sort_values(
    "Response_Rate",
    ascending=False
)


fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    country_summary["Country"],
    country_summary["Response_Rate"]
)

ax.set_title(
    "Response Rate by Country"
)

ax.set_ylabel("Response Rate (%)")

ax.tick_params(axis="x", rotation=30)

plt.tight_layout()

st.pyplot(fig, width="stretch")

plt.close(fig)


best_country = country_summary.iloc[0]


st.info(
    f"🌍 **Highest response rate:** "
    f"{best_country['Country']} "
    f"({best_country['Response_Rate']:.2f}%)."
)


# ============================================================
# AGE GROUP
# ============================================================

st.subheader("Response Rate by Age Group")


age_summary = (
    df.groupby(
        "Age_Band",
        observed=False
    )
    .agg(
        Customers=("ID", "count"),
        Response_Rate=("Response", "mean"),
        Average_Spend=("Total_Spend", "mean")
    )
    .reset_index()
)


age_summary["Response_Rate"] *= 100


fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    age_summary["Age_Band"].astype(str),
    age_summary["Response_Rate"]
)

ax.set_title(
    "Response Rate by Age Group"
)

ax.set_xlabel("Age Group")

ax.set_ylabel("Response Rate (%)")

plt.tight_layout()

st.pyplot(fig, width="stretch")

plt.close(fig)


# ============================================================
# INCOME BAND
# ============================================================

st.subheader("Response Rate by Income Band")


income_summary = (
    df.groupby(
        "Income_Band",
        observed=False
    )
    .agg(
        Customers=("ID", "count"),
        Response_Rate=("Response", "mean"),
        Average_Spend=("Total_Spend", "mean")
    )
    .reset_index()
)


income_summary["Response_Rate"] *= 100


fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    income_summary["Income_Band"].astype(str),
    income_summary["Response_Rate"]
)

ax.set_title(
    "Response Rate by Income Band"
)

ax.set_xlabel("Income Band")

ax.set_ylabel("Response Rate (%)")

plt.tight_layout()

st.pyplot(fig, width="stretch")

plt.close(fig)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.header("💡 Business Insights")


highest_age = age_summary.loc[
    age_summary["Response_Rate"].idxmax()
]


highest_income = income_summary.loc[
    income_summary["Response_Rate"].idxmax()
]


st.markdown(
    f"""
### 1️⃣ Older customers show stronger campaign response

The **{highest_age['Age_Band']}** age group has the highest
response rate at **{highest_age['Response_Rate']:.2f}%**.

### 2️⃣ Higher-income customers are more responsive

The **{highest_income['Income_Band']}** income group has the
highest response rate at **{highest_income['Response_Rate']:.2f}%**.

### 3️⃣ High-value customers are important targets

The top 10% of customers by spending have an average spend of
**{hv_spend:,.2f}** and a response rate of **{hv_response:.2f}%**.

### 4️⃣ Australia is the strongest-performing market

**{best_country['Country']}** has the highest country-level
response rate at **{best_country['Response_Rate']:.2f}%**.

### 5️⃣ Responders show stronger purchase activity

Campaign responders can be compared with non-responders across
web, catalog, and store purchasing channels to identify the
most effective channels for future campaigns.
"""
)


# ============================================================
# RECOMMENDATIONS
# ============================================================

st.header("🎯 Business Recommendations")


st.markdown(
    """
**1. Target high-income customers**

Prioritize higher-income segments because their campaign response
rates are stronger.

**2. Focus on high-value customers**

Customers in the top spending segment generate substantially more
revenue and show stronger campaign responsiveness.

**3. Prioritize mature customer segments**

Customers aged 50+ show stronger response rates and can be an
important target group.

**4. Use digital channels strategically**

Responders show stronger web and catalog purchasing activity,
making these channels useful for targeted campaigns.

**5. Investigate country-level differences**

Markets with higher response rates should receive focused campaigns,
while lower-performing markets should be tested with localized offers.

**6. Promote high-performing product categories**

Meat and wine represent the largest spending categories and can be
considered for promotional bundles and targeted offers.
"""
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Marketing Campaign Analysis | "
    "Python • Pandas • EDA • SQL • Customer Segmentation • Streamlit"
)