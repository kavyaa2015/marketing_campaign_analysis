# Marketing Campaign Analysis

## Customer Analytics & Campaign Response Analysis

An end-to-end data analytics project that analyzes customer demographics, purchasing behavior, campaign responses, product spending, purchasing channels, and customer segments to identify high-value customers and improve marketing campaign targeting.

---

## Project Overview

The objective of this project is to understand customer behavior and identify which customer groups are more likely to respond to marketing campaigns.

### Workflow

**Raw Data → Data Cleaning → EDA → Business Analysis → Customer Segmentation → SQL Analysis → Dashboard → Business Insights**

The final result is an interactive Streamlit dashboard for exploring customer behavior and campaign performance.

---

## Business Objectives

- Analyze overall campaign response rate
- Identify high-performing age and income groups
- Compare campaign performance across countries
- Analyze product spending patterns
- Compare purchasing channels
- Identify high-value customers
- Create meaningful customer segments
- Provide actionable marketing recommendations

---

## Dataset

The cleaned dataset contains:

- **56,000 customers**
- **40 analytical columns**

The dataset includes:

- Customer demographics
- Income and household information
- Product spending
- Web, catalog, and store purchases
- Website visits
- Campaign acceptance history
- Final campaign response

---

## Key Results

| Metric | Result |
|---|---:|
| Customers Analyzed | 56,000 |
| Overall Response Rate | 14.76% |
| Average Income | 57,252 |
| Average Spending | 640.33 |
| High-Value Customer Response Rate | 26.04% |
| Highest Country Response Rate | Australia – 20.19% |
| Highest Income-Band Response Rate | Very High – 25.36% |
| Highest Age-Band Response Rate | 70+ – 19.51% |

---

## Project Structure

```text
marketing_campaign_analysis/
│
├── README.md
├── app.py
├── requirements.txt
│
├── data/
│   └── processed/
│       └── marketing_cleaned.csv
│
├── database/
│   └── marketing_campaign.db
│
├── sql/
│   ├── schema.sql
│   ├── load_data.py
│   └── analytical_queries.sql
│
├── src/
│   ├── data_cleaning.py
│   ├── eda.py
│   ├── visualizations.py
│   ├── business_analysis.py
│   ├── segmentation.py
│   ├── database.py
│   └── run_sql.py
│
└── outputs/
    ├── analysis/
    └── figures/
