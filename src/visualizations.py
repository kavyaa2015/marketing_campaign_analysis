import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "marketing_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "figures" / "eda_visualizations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("GENERATING EDA VISUALIZATIONS")
print("=" * 60)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")


# ============================================================
# CREATE AGE GROUP
# ============================================================

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


# ============================================================
# 1. AGE DISTRIBUTION
# ============================================================

print("\nCreating age distribution...")

plt.figure(figsize=(8, 5))

plt.hist(df["Age"], bins=20)

plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "age_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 2. INCOME DISTRIBUTION
# ============================================================

print("Creating income distribution...")

plt.figure(figsize=(8, 5))

plt.hist(df["Income"], bins=30)

plt.title("Customer Income Distribution")
plt.xlabel("Income")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "income_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 3. SPENDING BY PRODUCT
# ============================================================

print("Creating spending by product chart...")

product_columns = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds"
]

product_spending = (
    df[product_columns]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))

plt.bar(
    product_spending.index,
    product_spending.values
)

plt.title("Total Spending by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Spending")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "spending_by_product.png",
    dpi=300
)

plt.close()


# ============================================================
# 4. RESPONSE RATE BY AGE GROUP
# ============================================================

print("Creating response by age group chart...")

age_response = (
    df.groupby(
        "Age_Band",
        observed=False
    )["Response"]
    .mean()
    * 100
)

plt.figure(figsize=(8, 5))

plt.bar(
    age_response.index.astype(str),
    age_response.values
)

plt.title("Campaign Response Rate by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Response Rate (%)")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "response_by_age_group.png",
    dpi=300
)

plt.close()


# ============================================================
# 5. RESPONSE VS INCOME
# ============================================================

print("Creating response vs income chart...")

plt.figure(figsize=(8, 5))

df.boxplot(
    column="Income",
    by="Response"
)

plt.title("Income Distribution by Campaign Response")
plt.suptitle("")

plt.xlabel("Campaign Response (0 = No, 1 = Yes)")
plt.ylabel("Income")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "response_vs_income.png",
    dpi=300
)

plt.close()


# ============================================================
# 6. RESPONSE VS TOTAL SPENDING
# ============================================================

print("Creating response vs total spending chart...")

plt.figure(figsize=(8, 5))

df.boxplot(
    column="Total_Spend",
    by="Response"
)

plt.title("Total Spending by Campaign Response")
plt.suptitle("")

plt.xlabel("Campaign Response (0 = No, 1 = Yes)")
plt.ylabel("Total Spending")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "response_vs_total_spend.png",
    dpi=300
)

plt.close()


# ============================================================
# 7. CHANNEL PURCHASES BY RESPONSE
# ============================================================

print("Creating channel purchases chart...")

channel_columns = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases"
]

channel_response = (
    df.groupby("Response")[channel_columns]
    .mean()
    .T
)

ax = channel_response.plot(
    kind="bar",
    figsize=(9, 5)
)

ax.set_title("Average Channel Purchases by Campaign Response")
ax.set_xlabel("Purchase Channel")
ax.set_ylabel("Average Purchases")

ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45
)

ax.legend(
    ["No Response", "Response"]
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "channel_purchases_by_response.png",
    dpi=300
)

plt.close()


# ============================================================
# COMPLETED
# ============================================================

print("\n" + "=" * 60)
print("EDA VISUALIZATION COMPLETED")
print("=" * 60)

print("\nFiles created:")

files = [
    "age_distribution.png",
    "income_distribution.png",
    "spending_by_product.png",
    "response_by_age_group.png",
    "response_vs_income.png",
    "response_vs_total_spend.png",
    "channel_purchases_by_response.png"
]

for file in files:
    print(f"  ✓ {file}")

print("\nLocation:")
print(OUTPUT_DIR)

