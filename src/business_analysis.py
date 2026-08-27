import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "marketing_cleaned.csv"

OUTPUT_DIR = BASE_DIR / "outputs" / "analysis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("MARKETING CAMPAIGN BUSINESS ANALYSIS")
print("=" * 70)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")


# ============================================================
# CREATE DERIVED ANALYSIS COLUMNS IF NOT PRESENT
# ============================================================

if "Age_Band" not in df.columns:

    df["Age_Band"] = pd.cut(
        df["Age"],
        bins=[0, 29, 39, 49, 59, 69, np.inf],
        labels=[
            "<30",
            "30-39",
            "40-49",
            "50-59",
            "60-69",
            "70+"
        ]
    )


if "Income_Band" not in df.columns:

    df["Income_Band"] = pd.cut(
        df["Income"],
        bins=[0, 30000, 60000, 90000, np.inf],
        labels=[
            "Low",
            "Medium",
            "High",
            "Very High"
        ],
        include_lowest=True
    )


if "Total_Children" not in df.columns:

    df["Total_Children"] = (
        df["Kidhome"] +
        df["Teenhome"]
    )


if "Total_Spend" not in df.columns:

    product_columns = [
        "MntWines",
        "MntFruits",
        "MntMeatProducts",
        "MntFishProducts",
        "MntSweetProducts",
        "MntGoldProds"
    ]

    df["Total_Spend"] = df[product_columns].sum(axis=1)


if "Total_Purchases" not in df.columns:

    purchase_columns = [
        "NumDealsPurchases",
        "NumWebPurchases",
        "NumCatalogPurchases",
        "NumStorePurchases"
    ]

    df["Total_Purchases"] = df[purchase_columns].sum(axis=1)


# ============================================================
# 1. OVERALL KPIs
# ============================================================

total_customers = len(df)

response_rate = df["Response"].mean() * 100

average_income = df["Income"].mean()

average_spend = df["Total_Spend"].mean()

average_purchases = df["Total_Purchases"].mean()

average_visits = df["NumWebVisitsMonth"].mean()

high_spender_threshold = df["Total_Spend"].quantile(0.90)

high_spender_count = (
    df["Total_Spend"] > high_spender_threshold
).sum()


print("\n" + "=" * 70)
print("1. OVERALL KPIs")
print("=" * 70)

print(f"Total Customers          : {total_customers:,}")
print(f"Overall Response Rate    : {response_rate:.2f}%")
print(f"Average Income           : {average_income:,.2f}")
print(f"Average Total Spend      : {average_spend:,.2f}")
print(f"Average Total Purchases  : {average_purchases:.2f}")
print(f"Average Website Visits   : {average_visits:.2f}")
print(f"High Spender Threshold   : {high_spender_threshold:,.2f}")
print(f"High Spender Customers   : {high_spender_count:,}")


# ============================================================
# 2. CAMPAIGN PERFORMANCE
# ============================================================

campaign_columns = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Response"
]

campaign_records = []

for campaign in campaign_columns:

    accepted = int(df[campaign].sum())

    rate = df[campaign].mean() * 100

    campaign_records.append({
        "Campaign": campaign,
        "Customers_Accepted": accepted,
        "Acceptance_Rate": round(rate, 2)
    })


campaign_df = pd.DataFrame(campaign_records)

campaign_df.to_csv(
    OUTPUT_DIR / "campaign_performance.csv",
    index=False
)


print("\n" + "=" * 70)
print("2. CAMPAIGN PERFORMANCE")
print("=" * 70)

print(campaign_df.to_string(index=False))


# ============================================================
# 3. RESPONSE BY AGE BAND
# ============================================================

age_analysis = (
    df.groupby("Age_Band", observed=False)
    .agg(
        Customers=("ID", "count"),
        Response_Rate=("Response", "mean"),
        Average_Spend=("Total_Spend", "mean"),
        Average_Income=("Income", "mean")
    )
    .reset_index()
)

age_analysis["Response_Rate"] *= 100

age_analysis["Response_Rate"] = age_analysis[
    "Response_Rate"
].round(2)

age_analysis = age_analysis.round(2)

print("\n" + "=" * 70)
print("3. RESPONSE BY AGE BAND")
print("=" * 70)

print(age_analysis.to_string(index=False))


# ============================================================
# 4. RESPONSE BY INCOME BAND
# ============================================================

income_analysis = (
    df.groupby("Income_Band", observed=False)
    .agg(
        Customers=("ID", "count"),
        Response_Rate=("Response", "mean"),
        Average_Spend=("Total_Spend", "mean"),
        Average_Income=("Income", "mean")
    )
    .reset_index()
)

income_analysis["Response_Rate"] *= 100

income_analysis["Response_Rate"] = income_analysis[
    "Response_Rate"
].round(2)

income_analysis = income_analysis.round(2)

print("\n" + "=" * 70)
print("4. RESPONSE BY INCOME BAND")
print("=" * 70)

print(income_analysis.to_string(index=False))


# ============================================================
# 5. RESPONSE BY COUNTRY
# ============================================================

country_analysis = (
    df.groupby("Country")
    .agg(
        Customers=("ID", "count"),
        Response_Rate=("Response", "mean"),
        Average_Income=("Income", "mean"),
        Average_Spend=("Total_Spend", "mean"),
        Average_Purchases=("Total_Purchases", "mean")
    )
    .reset_index()
)

country_analysis["Response_Rate"] *= 100

country_analysis = country_analysis.round(2)

country_analysis = country_analysis.sort_values(
    "Response_Rate",
    ascending=False
)

country_analysis.to_csv(
    OUTPUT_DIR / "country_analysis.csv",
    index=False
)

print("\n" + "=" * 70)
print("5. RESPONSE BY COUNTRY")
print("=" * 70)

print(country_analysis.to_string(index=False))


# ============================================================
# 6. PRODUCT SPENDING ANALYSIS
# ============================================================

product_columns = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds"
]

product_records = []

for product in product_columns:

    product_records.append({
        "Product": product,
        "Total_Spending": df[product].sum(),
        "Average_Spending": df[product].mean(),
        "Median_Spending": df[product].median()
    })


product_analysis = pd.DataFrame(product_records)

product_analysis = product_analysis.sort_values(
    "Total_Spending",
    ascending=False
)

product_analysis = product_analysis.round(2)

product_analysis.to_csv(
    OUTPUT_DIR / "product_analysis.csv",
    index=False
)


print("\n" + "=" * 70)
print("6. PRODUCT SPENDING")
print("=" * 70)

print(product_analysis.to_string(index=False))


# ============================================================
# 7. PRODUCT SPENDING BY RESPONSE
# ============================================================

product_response = (
    df.groupby("Response")[product_columns]
    .mean()
    .round(2)
)

print("\n" + "=" * 70)
print("7. AVERAGE PRODUCT SPENDING BY RESPONSE")
print("=" * 70)

print(product_response)


# ============================================================
# 8. PRODUCT SPENDING BY COUNTRY
# ============================================================

country_product = (
    df.groupby("Country")[product_columns]
    .mean()
    .round(2)
)

print("\n" + "=" * 70)
print("8. AVERAGE PRODUCT SPENDING BY COUNTRY")
print("=" * 70)

print(country_product)


# ============================================================
# 9. CHANNEL ANALYSIS
# ============================================================

channel_columns = [
    "NumDealsPurchases",
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases"
]

channel_analysis = (
    df.groupby("Response")[channel_columns + ["NumWebVisitsMonth"]]
    .mean()
    .round(2)
)

print("\n" + "=" * 70)
print("9. CHANNEL USAGE BY RESPONSE")
print("=" * 70)

print(channel_analysis)


# ============================================================
# 10. HIGH-VALUE CUSTOMER ANALYSIS
# ============================================================

df["High_Value"] = (
    df["Total_Spend"] >= high_spender_threshold
)

high_value = df[df["High_Value"] == True]

normal_value = df[df["High_Value"] == False]

high_value_summary = pd.DataFrame({
    "Metric": [
        "Customers",
        "Average Income",
        "Average Spend",
        "Average Purchases",
        "Average Web Purchases",
        "Average Catalog Purchases",
        "Average Store Purchases",
        "Average Deals Purchases",
        "Average Website Visits",
        "Response Rate"
    ],

    "High_Value": [
        len(high_value),
        high_value["Income"].mean(),
        high_value["Total_Spend"].mean(),
        high_value["Total_Purchases"].mean(),
        high_value["NumWebPurchases"].mean(),
        high_value["NumCatalogPurchases"].mean(),
        high_value["NumStorePurchases"].mean(),
        high_value["NumDealsPurchases"].mean(),
        high_value["NumWebVisitsMonth"].mean(),
        high_value["Response"].mean() * 100
    ],

    "Other_Customers": [
        len(normal_value),
        normal_value["Income"].mean(),
        normal_value["Total_Spend"].mean(),
        normal_value["Total_Purchases"].mean(),
        normal_value["NumWebPurchases"].mean(),
        normal_value["NumCatalogPurchases"].mean(),
        normal_value["NumStorePurchases"].mean(),
        normal_value["NumDealsPurchases"].mean(),
        normal_value["NumWebVisitsMonth"].mean(),
        normal_value["Response"].mean() * 100
    ]
})

high_value_summary.iloc[1:, 1:] = (
    high_value_summary.iloc[1:, 1:].astype(float).round(2)
)

print("\n" + "=" * 70)
print("10. HIGH-VALUE CUSTOMER ANALYSIS")
print("=" * 70)

print(high_value_summary.to_string(index=False))


# ============================================================
# 11. RULE-BASED SEGMENTS
# ============================================================

df["High_Income"] = df["Income"] > 75000

df["Young_Customer"] = df["Age"] < 30

df["Campaign_Responder"] = df["Response"] == 1

df["High_Web_Engagement"] = df["NumWebVisitsMonth"] > 5

df["Family_Customer"] = df["Total_Children"] > 0

df["High_Spender"] = (
    df["Total_Spend"] > high_spender_threshold
)


segment_definitions = {
    "High Income": "High_Income",
    "Young Customer": "Young_Customer",
    "Campaign Responder": "Campaign_Responder",
    "High Web Engagement": "High_Web_Engagement",
    "Family Customer": "Family_Customer",
    "High Spender": "High_Spender"
}


segment_records = []

for segment_name, condition in segment_definitions.items():

    segment_data = df[df[condition]]

    segment_records.append({
        "Segment": segment_name,
        "Customers": len(segment_data),
        "Percentage": len(segment_data) / len(df) * 100,
        "Average_Spend": segment_data["Total_Spend"].mean(),
        "Average_Income": segment_data["Income"].mean(),
        "Average_Purchases": segment_data["Total_Purchases"].mean(),
        "Average_Web_Visits": segment_data["NumWebVisitsMonth"].mean(),
        "Response_Rate": segment_data["Response"].mean() * 100
    })


segment_summary = pd.DataFrame(segment_records)

segment_summary = segment_summary.round(2)

segment_summary = segment_summary.sort_values(
    "Response_Rate",
    ascending=False
)

segment_summary.to_csv(
    OUTPUT_DIR / "segment_summary.csv",
    index=False
)


print("\n" + "=" * 70)
print("11. RULE-BASED SEGMENT ANALYSIS")
print("=" * 70)

print(segment_summary.to_string(index=False))


# ============================================================
# 12. DEMOGRAPHIC ANALYSIS
# ============================================================

demographic_analysis = (
    df.groupby(
        ["Education", "Marital_Status"],
        dropna=False
    )
    .agg(
        Customers=("ID", "count"),
        Average_Income=("Income", "mean"),
        Average_Spend=("Total_Spend", "mean"),
        Response_Rate=("Response", "mean")
    )
    .reset_index()
)

demographic_analysis["Response_Rate"] *= 100

demographic_analysis = demographic_analysis.round(2)

demographic_analysis.to_csv(
    OUTPUT_DIR / "demographic_analysis.csv",
    index=False
)


print("\n" + "=" * 70)
print("12. EDUCATION + MARITAL STATUS ANALYSIS")
print("=" * 70)

print(demographic_analysis.head(20).to_string(index=False))


# ============================================================
# 13. UNDERSERVED CUSTOMERS
# ============================================================

# Business definition:
# High website engagement + low spending + no campaign response

low_spend_threshold = df["Total_Spend"].median()

underserved = df[
    (df["NumWebVisitsMonth"] > 5) &
    (df["Total_Spend"] <= low_spend_threshold) &
    (df["Response"] == 0)
].copy()

print("\n" + "=" * 70)
print("13. UNDERSERVED CUSTOMER ANALYSIS")
print("=" * 70)

print(f"Underserved Customers : {len(underserved):,}")
print(
    f"Percentage of Customers: "
    f"{len(underserved) / len(df) * 100:.2f}%"
)

if len(underserved) > 0:

    underserved_summary = pd.DataFrame({
        "Metric": [
            "Customers",
            "Average Age",
            "Average Income",
            "Average Spend",
            "Average Web Visits",
            "Average Web Purchases"
        ],

        "Value": [
            len(underserved),
            underserved["Age"].mean(),
            underserved["Income"].mean(),
            underserved["Total_Spend"].mean(),
            underserved["NumWebVisitsMonth"].mean(),
            underserved["NumWebPurchases"].mean()
        ]
    })

    underserved_summary["Value"] = underserved_summary[
        "Value"
    ].round(2)

    print("\nUnderserved profile:")
    print(underserved_summary.to_string(index=False))

    underserved[
        [
            "ID",
            "Age",
            "Income",
            "Country",
            "Total_Children",
            "Total_Spend",
            "NumWebVisitsMonth",
            "NumWebPurchases",
            "Response"
        ]
    ].to_csv(
        OUTPUT_DIR / "underserved_customers.csv",
        index=False
    )


# ============================================================
# 14. IDEAL TARGET CUSTOMER PROFILE
# ============================================================

# Data-driven target:
# High spenders who responded to the campaign

ideal_customers = df[
    (df["High_Spender"]) &
    (df["Response"] == 1)
].copy()


print("\n" + "=" * 70)
print("14. IDEAL TARGET CUSTOMER PROFILE")
print("=" * 70)

print(f"Ideal target customers: {len(ideal_customers):,}")

if len(ideal_customers) > 0:

    ideal_profile = pd.DataFrame({
        "Metric": [
            "Customers",
            "Average Age",
            "Average Income",
            "Average Spend",
            "Average Purchases",
            "Average Children",
            "Average Web Purchases",
            "Average Catalog Purchases",
            "Average Store Purchases",
            "Average Deals Purchases",
            "Average Website Visits"
        ],

        "Value": [
            len(ideal_customers),
            ideal_customers["Age"].mean(),
            ideal_customers["Income"].mean(),
            ideal_customers["Total_Spend"].mean(),
            ideal_customers["Total_Purchases"].mean(),
            ideal_customers["Total_Children"].mean(),
            ideal_customers["NumWebPurchases"].mean(),
            ideal_customers["NumCatalogPurchases"].mean(),
            ideal_customers["NumStorePurchases"].mean(),
            ideal_customers["NumDealsPurchases"].mean(),
            ideal_customers["NumWebVisitsMonth"].mean()
        ]
    })

    ideal_profile["Value"] = ideal_profile[
        "Value"
    ].round(2)

    print("\nIdeal customer profile:")
    print(ideal_profile.to_string(index=False))

    ideal_profile.to_csv(
        OUTPUT_DIR / "ideal_target_profile.csv",
        index=False
    )

    print("\nTop countries among ideal customers:")

    print(
        ideal_customers["Country"]
        .value_counts()
        .head(5)
    )

    print("\nAge bands among ideal customers:")

    print(
        ideal_customers["Age_Band"]
        .value_counts()
    )


# ============================================================
# 15. CORRELATION WITH RESPONSE
# ============================================================

correlation_columns = [
    "Income",
    "Age",
    "Recency",
    "Total_Spend",
    "Total_Purchases",
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
    "NumDealsPurchases",
    "NumWebVisitsMonth"
]

correlations = (
    df[correlation_columns + ["Response"]]
    .corr()["Response"]
    .drop("Response")
    .sort_values(
        ascending=False
    )
)

print("\n" + "=" * 70)
print("15. CORRELATION WITH CAMPAIGN RESPONSE")
print("=" * 70)

print(correlations.round(4))


# ============================================================
# COMPLETED
# ============================================================

print("\n" + "=" * 70)
print("BUSINESS ANALYSIS COMPLETED")
print("=" * 70)

print("\nOutput directory:")
print(OUTPUT_DIR)

print("\nGenerated files:")

for file in OUTPUT_DIR.iterdir():

    if file.is_file():
        print(f"  ✓ {file.name}")