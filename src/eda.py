"""
eda.py

Purpose:
    Perform Exploratory Data Analysis on the
    cleaned marketing dataset.

Analysis includes:
    1. Univariate analysis
    2. Bivariate analysis
    3. Multivariate analysis
    4. Correlation analysis
    5. Business-focused analysis
    6. Segment exploration
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. FILE PATH
# ============================================================

DATA_PATH = "data/processed/marketing_cleaned.csv"
FIGURE_PATH = "outputs/figures"


# ============================================================
# 2. LOAD DATA
# ============================================================

def load_cleaned_data():

    df = pd.read_csv(DATA_PATH)

    print("=" * 60)
    print("CLEANED DATA LOADED FOR EDA")
    print("=" * 60)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    return df


# ============================================================
# 3. BASIC EDA SUMMARY
# ============================================================

def basic_summary(df):

    print("\n" + "=" * 60)
    print("BASIC EDA SUMMARY")
    print("=" * 60)

    print("\nDataset shape:")
    print(df.shape)

    print("\nNumerical summary:")
    print(df.describe().T)


# ============================================================
# 4. SAVE FIGURE
# ============================================================

def save_figure(filename):

    os.makedirs(FIGURE_PATH, exist_ok=True)

    filepath = os.path.join(
        FIGURE_PATH,
        filename
    )

    plt.savefig(
        filepath,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()


# ============================================================
# 5. UNIVARIATE - AGE
# ============================================================

def analyze_age(df):

    print("\nAge statistics:")
    print(df["Age"].describe())

    plt.figure(figsize=(8, 5))

    sns.histplot(
        data=df,
        x="Age",
        bins=30,
        kde=True
    )

    plt.title("Distribution of Customer Age")
    plt.xlabel("Age")
    plt.ylabel("Number of Customers")

    save_figure("age_distribution.png")


# ============================================================
# 6. UNIVARIATE - INCOME
# ============================================================

def analyze_income(df):

    print("\nIncome statistics:")
    print(df["Income"].describe())

    plt.figure(figsize=(8, 5))

    sns.histplot(
        data=df,
        x="Income",
        bins=40,
        kde=True
    )

    plt.title("Distribution of Customer Income")
    plt.xlabel("Income")
    plt.ylabel("Number of Customers")

    save_figure("income_distribution.png")


# ============================================================
# 7. UNIVARIATE - RECENCY
# ============================================================

def analyze_recency(df):

    print("\nRecency statistics:")
    print(df["Recency"].describe())

    plt.figure(figsize=(8, 5))

    sns.histplot(
        data=df,
        x="Recency",
        bins=30,
        kde=True
    )

    plt.title("Distribution of Customer Recency")
    plt.xlabel("Recency (Days)")
    plt.ylabel("Number of Customers")

    save_figure("recency_distribution.png")


# ============================================================
# 8. UNIVARIATE - TOTAL SPENDING
# ============================================================

def analyze_total_spend(df):

    print("\nTotal spending statistics:")
    print(df["Total_Spend"].describe())

    plt.figure(figsize=(8, 5))

    sns.histplot(
        data=df,
        x="Total_Spend",
        bins=40,
        kde=True
    )

    plt.title("Distribution of Total Customer Spending")
    plt.xlabel("Total Spend")
    plt.ylabel("Number of Customers")

    save_figure("total_spend_distribution.png")


# ============================================================
# 9. PRODUCT SPENDING
# ============================================================

def analyze_product_spending(df):

    spending_columns = [
        "MntWines",
        "MntFruits",
        "MntMeatProducts",
        "MntFishProducts",
        "MntSweetProducts",
        "MntGoldProds"
    ]

    product_totals = (
        df[spending_columns]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nTotal spending by product:")
    print(product_totals)

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=product_totals.values,
        y=product_totals.index
    )

    plt.title("Total Spending by Product Category")
    plt.xlabel("Total Spending")
    plt.ylabel("Product Category")

    save_figure("product_spending.png")


# ============================================================
# 10. CUSTOMER DISTRIBUTION BY COUNTRY
# ============================================================

def analyze_country(df):

    country_counts = df["Country"].value_counts()

    print("\nCustomers by country:")
    print(country_counts)

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=country_counts.values,
        y=country_counts.index
    )

    plt.title("Customers by Country")
    plt.xlabel("Number of Customers")
    plt.ylabel("Country")

    save_figure("customers_by_country.png")


# ============================================================
# 11. CAMPAIGN RESPONSE
# ============================================================

def analyze_response(df):

    response_rate = df["Response"].mean() * 100

    print(
        f"\nOverall campaign response rate: "
        f"{response_rate:.2f}%"
    )

    print("\nResponse counts:")
    print(df["Response"].value_counts())

    plt.figure(figsize=(7, 5))

    sns.countplot(
        data=df,
        x="Response"
    )

    plt.title("Campaign Response")
    plt.xlabel("Response")
    plt.ylabel("Number of Customers")

    save_figure("campaign_response.png")


# ============================================================
# 12. INCOME VS RESPONSE
# ============================================================

def income_vs_response(df):

    result = df.groupby("Response")["Income"].agg(
        ["count", "mean", "median"]
    )

    print("\nIncome by campaign response:")
    print(result)

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="Response",
        y="Income"
    )

    plt.title("Income vs Campaign Response")
    plt.xlabel("Response")
    plt.ylabel("Income")

    save_figure("income_vs_response.png")


# ============================================================
# 13. AGE VS RESPONSE
# ============================================================

def age_vs_response(df):

    bins = [0, 29, 39, 49, 59, 69, 100]

    labels = [
        "<30",
        "30-39",
        "40-49",
        "50-59",
        "60-69",
        "70+"
    ]

    df["Age_Band"] = pd.cut(
        df["Age"],
        bins=bins,
        labels=labels
    )

    age_response = (
        df.groupby(
            "Age_Band",
            observed=False
        )["Response"]
        .mean()
        .mul(100)
    )

    print("\nResponse rate by age group:")
    print(age_response)

    plt.figure(figsize=(9, 5))

    sns.barplot(
        x=age_response.index,
        y=age_response.values
    )

    plt.title("Campaign Response Rate by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Response Rate (%)")

    save_figure("age_vs_response.png")


# ============================================================
# 14. SPENDING VS RESPONSE
# ============================================================

def spending_vs_response(df):

    result = df.groupby("Response")["Total_Spend"].agg(
        ["count", "mean", "median"]
    )

    print("\nTotal spending by response:")
    print(result)

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="Response",
        y="Total_Spend"
    )

    plt.title("Total Spending vs Campaign Response")
    plt.xlabel("Response")
    plt.ylabel("Total Spend")

    save_figure("spending_vs_response.png")


# ============================================================
# 15. PRODUCT SPENDING VS RESPONSE
# ============================================================

def product_spending_vs_response(df):

    spending_columns = [
        "MntWines",
        "MntFruits",
        "MntMeatProducts",
        "MntFishProducts",
        "MntSweetProducts",
        "MntGoldProds"
    ]

    result = (
        df.groupby("Response")[spending_columns]
        .mean()
        .T
    )

    print("\nAverage product spending by response:")
    print(result)

    result.plot(
        kind="bar",
        figsize=(12, 6)
    )

    plt.title(
        "Average Product Spending by Campaign Response"
    )

    plt.xlabel("Product Category")
    plt.ylabel("Average Spending")

    plt.xticks(rotation=45)

    plt.tight_layout()

    save_figure("product_spending_vs_response.png")


# ============================================================
# 16. CHANNEL USAGE VS RESPONSE
# ============================================================

def channel_vs_response(df):

    channel_columns = [
        "NumDealsPurchases",
        "NumWebPurchases",
        "NumCatalogPurchases",
        "NumStorePurchases"
    ]

    result = (
        df.groupby("Response")[channel_columns]
        .mean()
        .T
    )

    print("\nAverage channel purchases by response:")
    print(result)

    result.plot(
        kind="bar",
        figsize=(12, 6)
    )

    plt.title(
        "Average Channel Purchases by Campaign Response"
    )

    plt.xlabel("Channel")
    plt.ylabel("Average Purchases")

    plt.xticks(rotation=45)

    plt.tight_layout()

    save_figure("channel_vs_response.png")


# ============================================================
# 17. WEBSITE VISITS VS RESPONSE
# ============================================================

def website_visits_vs_response(df):

    result = df.groupby("Response")[
        "NumWebVisitsMonth"
    ].agg(
        ["mean", "median"]
    )

    print("\nWebsite visits by response:")
    print(result)

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="Response",
        y="NumWebVisitsMonth"
    )

    plt.title(
        "Website Visits vs Campaign Response"
    )

    plt.xlabel("Response")
    plt.ylabel("Website Visits per Month")

    save_figure("website_visits_vs_response.png")


# ============================================================
# 18. CORRELATION ANALYSIS
# ============================================================

def correlation_analysis(df):

    columns = [
        "Age",
        "Income",
        "Recency",
        "Total_Spend",
        "Total_Purchases",
        "NumWebVisitsMonth",
        "Response"
    ]

    correlation = df[columns].corr()

    print("\nCorrelation with Response:")
    print(
        correlation["Response"]
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 7))

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0
    )

    plt.title("Correlation Matrix")

    save_figure("correlation_matrix.png")


# ============================================================
# 19. MULTIVARIATE ANALYSIS
# ============================================================

def multivariate_analysis(df):

    sample = df.sample(
        min(10000, len(df)),
        random_state=42
    )

    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=sample,
        x="Income",
        y="Total_Spend",
        hue="Response",
        alpha=0.6
    )

    plt.title(
        "Income vs Total Spending by Campaign Response"
    )

    plt.xlabel("Income")
    plt.ylabel("Total Spend")

    save_figure("income_spending_response.png")


# ============================================================
# 20. MAIN
# ============================================================

def main():

    df = load_cleaned_data()

    basic_summary(df)

    # ------------------------------
    # UNIVARIATE ANALYSIS
    # ------------------------------

    analyze_age(df)
    analyze_income(df)
    analyze_recency(df)
    analyze_total_spend(df)
    analyze_product_spending(df)
    analyze_country(df)
    analyze_response(df)

    # ------------------------------
    # BIVARIATE ANALYSIS
    # ------------------------------

    income_vs_response(df)
    age_vs_response(df)
    spending_vs_response(df)
    product_spending_vs_response(df)
    channel_vs_response(df)
    website_visits_vs_response(df)

    # ------------------------------
    # MULTIVARIATE ANALYSIS
    # ------------------------------

    correlation_analysis(df)
    multivariate_analysis(df)

    print("\n" + "=" * 60)
    print("EDA COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()