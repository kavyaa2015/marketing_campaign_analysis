"""
data_cleaning.py

Purpose:
    Load the raw marketing dataset,
    inspect data quality,
    clean/validate the data,
    create derived features,
    and save the processed dataset.
"""

import os
import pandas as pd
import numpy as np


# ============================================================
# 1. FILE PATHS
# ============================================================

RAW_DATA_PATH = "data/raw/marketing_campaign_data.csv"
DICTIONARY_PATH = "data/raw/marketing_data_dictionary.csv"
PROCESSED_DATA_PATH = "data/processed/marketing_cleaned.csv"


# ============================================================
# 2. LOAD DATA
# ============================================================

def load_data():
    """Load the marketing dataset."""

    df = pd.read_csv(RAW_DATA_PATH)

    print("=" * 60)
    print("DATA LOADED")
    print("=" * 60)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    return df


# ============================================================
# 3. UNDERSTAND DATA
# ============================================================

def understand_data(df):
    """Display basic information about the dataset."""

    print("\n" + "=" * 60)
    print("DATA UNDERSTANDING")
    print("=" * 60)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nDataset information:")
    df.info()

    print("\nStatistical summary:")
    print(df.describe(include="all").T)


# ============================================================
# 4. CHECK MISSING VALUES
# ============================================================

def check_missing_values(df):
    """Check missing values."""

    print("\n" + "=" * 60)
    print("MISSING VALUE CHECK")
    print("=" * 60)

    missing = pd.DataFrame({
        "Missing_Count": df.isnull().sum(),
        "Missing_Percentage": df.isnull().mean() * 100
    })

    print(missing)

    total_missing = df.isnull().sum().sum()

    print(f"\nTotal missing values: {total_missing}")


# ============================================================
# 5. CHECK DUPLICATES
# ============================================================

def check_duplicates(df):
    """Check duplicate rows and customer IDs."""

    print("\n" + "=" * 60)
    print("DUPLICATE CHECK")
    print("=" * 60)

    duplicate_rows = df.duplicated().sum()
    duplicate_ids = df["ID"].duplicated().sum()

    print(f"Duplicate rows       : {duplicate_rows}")
    print(f"Duplicate customer ID: {duplicate_ids}")


# ============================================================
# 6. CHECK NUMERICAL VALUES
# ============================================================

def check_invalid_values(df):
    """Check negative values in numerical columns."""

    print("\n" + "=" * 60)
    print("INVALID VALUE CHECK")
    print("=" * 60)

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    negative_values = (df[numeric_columns] < 0).sum()

    print("Negative values:")
    print(negative_values)


# ============================================================
# 7. CONVERT DATE
# ============================================================

def convert_date(df):
    """Convert customer enrollment date to datetime."""

    df["Dt_Customer"] = pd.to_datetime(
        df["Dt_Customer"],
        errors="coerce"
    )

    return df


# ============================================================
# 8. CREATE AGE
# ============================================================

def create_age(df):
    """Create customer age from birth year."""

    REFERENCE_YEAR = 2014

    df["Age"] = REFERENCE_YEAR - df["Year_Birth"]

    return df


# ============================================================
# 9. CREATE TOTAL CHILDREN
# ============================================================

def create_total_children(df):
    """Create total number of children/teens."""

    df["Total_Children"] = (
        df["Kidhome"] + df["Teenhome"]
    )

    return df


# ============================================================
# 10. CREATE TOTAL SPEND
# ============================================================

def create_total_spend(df):
    """Calculate total customer spending."""

    spending_columns = [
        "MntWines",
        "MntFruits",
        "MntMeatProducts",
        "MntFishProducts",
        "MntSweetProducts",
        "MntGoldProds"
    ]

    df["Total_Spend"] = df[spending_columns].sum(axis=1)

    return df


# ============================================================
# 11. CREATE TOTAL PURCHASES
# ============================================================

def create_total_purchases(df):
    """Calculate total purchases across channels."""

    purchase_columns = [
        "NumDealsPurchases",
        "NumWebPurchases",
        "NumCatalogPurchases",
        "NumStorePurchases"
    ]

    df["Total_Purchases"] = df[purchase_columns].sum(axis=1)

    return df


# ============================================================
# 12. CREATE CUSTOMER TENURE
# ============================================================

def create_customer_tenure(df):
    """Calculate customer tenure in days."""

    reference_date = df["Dt_Customer"].max()

    df["Customer_Tenure_Days"] = (
        reference_date - df["Dt_Customer"]
    ).dt.days

    return df


# ============================================================
# 13. CREATE CAMPAIGN ACCEPTANCE COUNT
# ============================================================

def create_campaign_acceptance(df):
    """Calculate number of previously accepted campaigns."""

    campaign_columns = [
        "AcceptedCmp1",
        "AcceptedCmp2",
        "AcceptedCmp3",
        "AcceptedCmp4",
        "AcceptedCmp5"
    ]

    df["Total_Campaign_Accepted"] = (
        df[campaign_columns].sum(axis=1)
    )

    return df


# ============================================================
# 14. VALIDATE AGE
# ============================================================

def validate_age(df):
    """Display age range for validation."""

    print("\n" + "=" * 60)
    print("AGE VALIDATION")
    print("=" * 60)

    print(f"Minimum age: {df['Age'].min()}")
    print(f"Maximum age: {df['Age'].max()}")

    unrealistic = df[
        (df["Age"] < 18) |
        (df["Age"] > 100)
    ]

    print(f"Potentially unrealistic ages: {len(unrealistic)}")


# ============================================================
# 15. CHECK OUTLIERS
# ============================================================

def check_outliers(df):
    """
    Identify statistical outliers using the IQR method.

    Outliers are reported, not automatically deleted.
    """

    print("\n" + "=" * 60)
    print("OUTLIER CHECK")
    print("=" * 60)

    columns_to_check = [
        "Income",
        "Recency",
        "Total_Spend",
        "Total_Purchases"
    ]

    for column in columns_to_check:

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        ]

        print(
            f"{column}: "
            f"{len(outliers)} potential outliers"
        )


# ============================================================
# 16. SAVE PROCESSED DATA
# ============================================================

def save_processed_data(df):
    """Save cleaned and feature-engineered dataset."""

    os.makedirs(
        os.path.dirname(PROCESSED_DATA_PATH),
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False
    )

    print("\n" + "=" * 60)
    print("PROCESSED DATA SAVED")
    print("=" * 60)

    print(PROCESSED_DATA_PATH)
    print(f"Final shape: {df.shape}")


# ============================================================
# 17. MAIN PIPELINE
# ============================================================

def main():

    # Load
    df = load_data()

    # Understand
    understand_data(df)

    # Data quality checks
    check_missing_values(df)
    check_duplicates(df)
    check_invalid_values(df)

    # Cleaning
    df = convert_date(df)

    # Feature engineering
    df = create_age(df)
    df = create_total_children(df)
    df = create_total_spend(df)
    df = create_total_purchases(df)
    df = create_customer_tenure(df)
    df = create_campaign_acceptance(df)

    # Validation
    validate_age(df)
    check_outliers(df)

    # Save
    save_processed_data(df)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()