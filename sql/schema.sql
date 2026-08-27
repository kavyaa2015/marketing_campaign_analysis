-- ============================================================
-- MARKETING CAMPAIGN ANALYSIS DATABASE
-- ============================================================

DROP TABLE IF EXISTS customers;

CREATE TABLE customers (

    ID INTEGER PRIMARY KEY,

    Year_Birth INTEGER,
    Education TEXT,
    Marital_Status TEXT,
    Income REAL,

    Kidhome INTEGER,
    Teenhome INTEGER,
    Country TEXT,

    Dt_Customer TEXT,
    Recency INTEGER,

    MntWines REAL,
    MntFruits REAL,
    MntMeatProducts REAL,
    MntFishProducts REAL,
    MntSweetProducts REAL,
    MntGoldProds REAL,

    NumDealsPurchases INTEGER,
    NumWebPurchases INTEGER,
    NumCatalogPurchases INTEGER,
    NumStorePurchases INTEGER,
    NumWebVisitsMonth INTEGER,

    AcceptedCmp1 INTEGER,
    AcceptedCmp2 INTEGER,
    AcceptedCmp3 INTEGER,
    AcceptedCmp4 INTEGER,
    AcceptedCmp5 INTEGER,

    Response INTEGER,
    Complain INTEGER,

    Age INTEGER,
    Total_Children INTEGER,
    Total_Spend REAL,
    Total_Purchases INTEGER,
    Customer_Tenure_Days INTEGER,
    Total_Campaign_Accepted INTEGER,

    Age_Band TEXT,
    Income_Band TEXT
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_customers_country
ON customers(Country);

CREATE INDEX idx_customers_response
ON customers(Response);

CREATE INDEX idx_customers_income
ON customers(Income);

CREATE INDEX idx_customers_age
ON customers(Age);

CREATE INDEX idx_customers_spend
ON customers(Total_Spend);