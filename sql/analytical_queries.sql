-- ============================================================
-- MARKETING CAMPAIGN ANALYTICAL QUERIES
-- ============================================================


-- ============================================================
-- 1. TOTAL CUSTOMERS
-- ============================================================

SELECT COUNT(*) AS total_customers
FROM customers;


-- ============================================================
-- 2. OVERALL RESPONSE RATE
-- ============================================================

SELECT
    COUNT(*) AS total_customers,
    SUM(Response) AS responders,
    ROUND(
        100.0 * AVG(Response),
        2
    ) AS response_rate
FROM customers;


-- ============================================================
-- 3. CAMPAIGN ACCEPTANCE
-- ============================================================

SELECT
    SUM(AcceptedCmp1) AS Campaign1_Accepted,
    SUM(AcceptedCmp2) AS Campaign2_Accepted,
    SUM(AcceptedCmp3) AS Campaign3_Accepted,
    SUM(AcceptedCmp4) AS Campaign4_Accepted,
    SUM(AcceptedCmp5) AS Campaign5_Accepted,
    SUM(Response) AS Final_Response
FROM customers;


-- ============================================================
-- 4. RESPONSE RATE BY AGE BAND
-- ============================================================

SELECT
    Age_Band,
    COUNT(*) AS customers,
    ROUND(
        100.0 * AVG(Response),
        2
    ) AS response_rate,
    ROUND(
        AVG(Total_Spend),
        2
    ) AS avg_spend
FROM customers
GROUP BY Age_Band
ORDER BY response_rate DESC;


-- ============================================================
-- 5. RESPONSE RATE BY INCOME BAND
-- ============================================================

SELECT
    Income_Band,
    COUNT(*) AS customers,
    ROUND(
        100.0 * AVG(Response),
        2
    ) AS response_rate,
    ROUND(
        AVG(Total_Spend),
        2
    ) AS avg_spend
FROM customers
GROUP BY Income_Band
ORDER BY response_rate DESC;


-- ============================================================
-- 6. COUNTRY PERFORMANCE
-- ============================================================

SELECT
    Country,
    COUNT(*) AS customers,
    ROUND(
        AVG(Income),
        2
    ) AS avg_income,
    ROUND(
        AVG(Total_Spend),
        2
    ) AS avg_spend,
    ROUND(
        100.0 * AVG(Response),
        2
    ) AS response_rate
FROM customers
GROUP BY Country
ORDER BY response_rate DESC;


-- ============================================================
-- 7. PRODUCT SPENDING
-- ============================================================

SELECT 'Wine' AS product,
       SUM(MntWines) AS total_spend
FROM customers

UNION ALL

SELECT 'Fruits',
       SUM(MntFruits)
FROM customers

UNION ALL

SELECT 'Meat',
       SUM(MntMeatProducts)
FROM customers

UNION ALL

SELECT 'Fish',
       SUM(MntFishProducts)
FROM customers

UNION ALL

SELECT 'Sweets',
       SUM(MntSweetProducts)
FROM customers

UNION ALL

SELECT 'Gold',
       SUM(MntGoldProds)
FROM customers

ORDER BY total_spend DESC;


-- ============================================================
-- 8. PRODUCT SPENDING BY RESPONSE
-- ============================================================

SELECT
    Response,

    ROUND(AVG(MntWines), 2) AS avg_wine,
    ROUND(AVG(MntFruits), 2) AS avg_fruits,
    ROUND(AVG(MntMeatProducts), 2) AS avg_meat,
    ROUND(AVG(MntFishProducts), 2) AS avg_fish,
    ROUND(AVG(MntSweetProducts), 2) AS avg_sweets,
    ROUND(AVG(MntGoldProds), 2) AS avg_gold

FROM customers

GROUP BY Response;


-- ============================================================
-- 9. CHANNEL USAGE
-- ============================================================

SELECT
    Response,

    ROUND(
        AVG(NumWebPurchases),
        2
    ) AS avg_web_purchases,

    ROUND(
        AVG(NumCatalogPurchases),
        2
    ) AS avg_catalog_purchases,

    ROUND(
        AVG(NumStorePurchases),
        2
    ) AS avg_store_purchases,

    ROUND(
        AVG(NumDealsPurchases),
        2
    ) AS avg_deal_purchases,

    ROUND(
        AVG(NumWebVisitsMonth),
        2
    ) AS avg_web_visits

FROM customers

GROUP BY Response;


-- ============================================================
-- 10. HIGH-VALUE CUSTOMERS
-- ============================================================

WITH threshold AS (

    SELECT
        Total_Spend,
        NTILE(10) OVER (
            ORDER BY Total_Spend
        ) AS spend_decile

    FROM customers
)

SELECT
    COUNT(*) AS high_value_customers,
    ROUND(
        AVG(c.Income),
        2
    ) AS avg_income,
    ROUND(
        AVG(c.Total_Spend),
        2
    ) AS avg_spend,
    ROUND(
        100.0 * AVG(c.Response),
        2
    ) AS response_rate
FROM customers c
JOIN threshold t
    ON c.Total_Spend = t.Total_Spend
WHERE t.spend_decile = 10;


-- ============================================================
-- 11. EDUCATION + MARITAL STATUS
-- ============================================================

SELECT
    Education,
    Marital_Status,
    COUNT(*) AS customers,

    ROUND(
        AVG(Income),
        2
    ) AS avg_income,

    ROUND(
        AVG(Total_Spend),
        2
    ) AS avg_spend,

    ROUND(
        100.0 * AVG(Response),
        2
    ) AS response_rate

FROM customers

GROUP BY
    Education,
    Marital_Status

ORDER BY
    response_rate DESC;


-- ============================================================
-- 12. FAMILY CUSTOMERS
-- ============================================================

SELECT
    CASE
        WHEN Total_Children > 0
        THEN 'Family Customer'
        ELSE 'No Children'
    END AS family_segment,

    COUNT(*) AS customers,

    ROUND(
        AVG(Total_Spend),
        2
    ) AS avg_spend,

    ROUND(
        100.0 * AVG(Response),
        2
    ) AS response_rate

FROM customers

GROUP BY family_segment;


-- ============================================================
-- 13. HIGH-INCOME CUSTOMERS
-- ============================================================

SELECT
    CASE
        WHEN Income > 75000
        THEN 'High Income'
        ELSE 'Other'
    END AS income_segment,

    COUNT(*) AS customers,

    ROUND(
        AVG(Total_Spend),
        2
    ) AS avg_spend,

    ROUND(
        100.0 * AVG(Response),
        2
    ) AS response_rate

FROM customers

GROUP BY income_segment;


-- ============================================================
-- 14. YOUNG CUSTOMERS
-- ============================================================

SELECT
    CASE
        WHEN Age < 30
        THEN 'Young Customer'
        ELSE 'Other'
    END AS age_segment,

    COUNT(*) AS customers,

    ROUND(
        AVG(Total_Spend),
        2
    ) AS avg_spend,

    ROUND(
        100.0 * AVG(Response),
        2
    ) AS response_rate

FROM customers

GROUP BY age_segment;


-- ============================================================
-- 15. HIGH WEB ENGAGEMENT
-- ============================================================

SELECT
    CASE
        WHEN NumWebVisitsMonth > 5
        THEN 'High Web Engagement'
        ELSE 'Other'
    END AS web_segment,

    COUNT(*) AS customers,

    ROUND(
        AVG(Total_Spend),
        2
    ) AS avg_spend,

    ROUND(
        100.0 * AVG(Response),
        2
    ) AS response_rate

FROM customers

GROUP BY web_segment;


-- ============================================================
-- 16. CAMPAIGN RESPONDERS
-- ============================================================

SELECT
    CASE
        WHEN Response = 1
        THEN 'Campaign Responder'
        ELSE 'Non Responder'
    END AS response_segment,

    COUNT(*) AS customers,

    ROUND(
        AVG(Total_Spend),
        2
    ) AS avg_spend,

    ROUND(
        AVG(Income),
        2
    ) AS avg_income

FROM customers

GROUP BY response_segment;


-- ============================================================
-- 17. CAMPAIGN ACCEPTANCE COMPARISON
-- ============================================================

SELECT
    Campaign,
    Acceptance_Rate
FROM (

    SELECT
        'AcceptedCmp1' AS Campaign,
        AVG(AcceptedCmp1) * 100 AS Acceptance_Rate
    FROM customers

    UNION ALL

    SELECT
        'AcceptedCmp2',
        AVG(AcceptedCmp2) * 100
    FROM customers

    UNION ALL

    SELECT
        'AcceptedCmp3',
        AVG(AcceptedCmp3) * 100
    FROM customers

    UNION ALL

    SELECT
        'AcceptedCmp4',
        AVG(AcceptedCmp4) * 100
    FROM customers

    UNION ALL

    SELECT
        'AcceptedCmp5',
        AVG(AcceptedCmp5) * 100
    FROM customers

    UNION ALL

    SELECT
        'Response',
        AVG(Response) * 100
    FROM customers

)
ORDER BY Acceptance_Rate DESC;


-- ============================================================
-- 18. POTENTIALLY UNDERSERVED CUSTOMERS
-- ============================================================

SELECT
    ID,
    Age,
    Income,
    Country,
    Total_Children,
    Total_Spend,
    NumWebVisitsMonth,
    NumWebPurchases,
    Response

FROM customers

WHERE
    NumWebVisitsMonth > 5
    AND Total_Spend <= (
        SELECT AVG(Total_Spend)
        FROM customers
    )
    AND Response = 0;


-- ============================================================
-- 19. IDEAL TARGET CUSTOMER
-- ============================================================

SELECT

    COUNT(*) AS customers,

    ROUND(
        AVG(Age),
        2
    ) AS avg_age,

    ROUND(
        AVG(Income),
        2
    ) AS avg_income,

    ROUND(
        AVG(Total_Spend),
        2
    ) AS avg_spend,

    ROUND(
        AVG(Total_Purchases),
        2
    ) AS avg_purchases,

    ROUND(
        AVG(Total_Children),
        2
    ) AS avg_children

FROM customers

WHERE
    Response = 1
    AND Total_Spend >
    (
        SELECT
            Total_Spend
        FROM
            (
                SELECT
                    Total_Spend,
                    NTILE(10) OVER (
                        ORDER BY Total_Spend
                    ) AS decile
                FROM customers
            )
        WHERE decile = 9
        ORDER BY Total_Spend
        LIMIT 1
    );
    -- ============================================================
-- DASHBOARD SUPPORTING VIEWS
-- ============================================================


-- Overall KPI View
DROP VIEW IF EXISTS vw_overall_kpis;

CREATE VIEW vw_overall_kpis AS

SELECT
    COUNT(*) AS total_customers,
    ROUND(AVG(Income), 2) AS average_income,
    ROUND(AVG(Total_Spend), 2) AS average_spend,
    ROUND(AVG(Total_Purchases), 2) AS average_purchases,
    ROUND(AVG(NumWebVisitsMonth), 2) AS average_web_visits,
    ROUND(AVG(Response) * 100, 2) AS response_rate

FROM customers;


-- Campaign Performance View
DROP VIEW IF EXISTS vw_campaign_performance;

CREATE VIEW vw_campaign_performance AS

SELECT
    'Campaign 1' AS Campaign,
    SUM(AcceptedCmp1) AS Customers_Accepted,
    ROUND(AVG(AcceptedCmp1) * 100, 2) AS Acceptance_Rate
FROM customers

UNION ALL

SELECT
    'Campaign 2',
    SUM(AcceptedCmp2),
    ROUND(AVG(AcceptedCmp2) * 100, 2)
FROM customers

UNION ALL

SELECT
    'Campaign 3',
    SUM(AcceptedCmp3),
    ROUND(AVG(AcceptedCmp3) * 100, 2)
FROM customers

UNION ALL

SELECT
    'Campaign 4',
    SUM(AcceptedCmp4),
    ROUND(AVG(AcceptedCmp4) * 100, 2)
FROM customers

UNION ALL

SELECT
    'Campaign 5',
    SUM(AcceptedCmp5),
    ROUND(AVG(AcceptedCmp5) * 100, 2)
FROM customers

UNION ALL

SELECT
    'Final Response',
    SUM(Response),
    ROUND(AVG(Response) * 100, 2)
FROM customers;


-- Country Analysis View
DROP VIEW IF EXISTS vw_country_analysis;

CREATE VIEW vw_country_analysis AS

SELECT
    Country,
    COUNT(*) AS Customers,
    ROUND(AVG(Response) * 100, 2) AS Response_Rate,
    ROUND(AVG(Income), 2) AS Average_Income,
    ROUND(AVG(Total_Spend), 2) AS Average_Spend,
    ROUND(AVG(Total_Purchases), 2) AS Average_Purchases

FROM customers

GROUP BY Country;


-- ============================================================
-- AGE BAND ANALYSIS VIEW
-- ============================================================

DROP VIEW IF EXISTS vw_age_analysis;

CREATE VIEW vw_age_analysis AS

SELECT
    CASE
        WHEN Age < 30 THEN '<30'
        WHEN Age BETWEEN 30 AND 39 THEN '30-39'
        WHEN Age BETWEEN 40 AND 49 THEN '40-49'
        WHEN Age BETWEEN 50 AND 59 THEN '50-59'
        WHEN Age BETWEEN 60 AND 69 THEN '60-69'
        ELSE '70+'
    END AS Age_Band,

    COUNT(*) AS Customers,

    ROUND(AVG(Response) * 100, 2) AS Response_Rate,

    ROUND(AVG(Total_Spend), 2) AS Average_Spend,

    ROUND(AVG(Income), 2) AS Average_Income

FROM customers

GROUP BY
    CASE
        WHEN Age < 30 THEN '<30'
        WHEN Age BETWEEN 30 AND 39 THEN '30-39'
        WHEN Age BETWEEN 40 AND 49 THEN '40-49'
        WHEN Age BETWEEN 50 AND 59 THEN '50-59'
        WHEN Age BETWEEN 60 AND 69 THEN '60-69'
        ELSE '70+'
    END;

-- ============================================================
-- SEGMENT ANALYSIS VIEW
-- ============================================================

DROP VIEW IF EXISTS vw_segment_analysis;

CREATE VIEW vw_segment_analysis AS

SELECT
    'High Spender' AS Segment,

    COUNT(*) AS Customers,

    ROUND(AVG(Income), 2) AS Average_Income,

    ROUND(AVG(Total_Spend), 2) AS Average_Spend,

    ROUND(AVG(Response) * 100, 2) AS Response_Rate

FROM customers

WHERE Total_Spend > (
    SELECT Total_Spend
    FROM (
        SELECT
            Total_Spend,
            NTILE(10) OVER (
                ORDER BY Total_Spend
            ) AS decile
        FROM customers
    )
    WHERE decile = 9
    ORDER BY Total_Spend
    LIMIT 1
)


UNION ALL


SELECT
    'High Income',

    COUNT(*),

    ROUND(AVG(Income), 2),

    ROUND(AVG(Total_Spend), 2),

    ROUND(AVG(Response) * 100, 2)

FROM customers

WHERE Income > 75000


UNION ALL


SELECT
    'Young Customer',

    COUNT(*),

    ROUND(AVG(Income), 2),

    ROUND(AVG(Total_Spend), 2),

    ROUND(AVG(Response) * 100, 2)

FROM customers

WHERE Age < 30


UNION ALL


SELECT
    'High Web Engagement',

    COUNT(*),

    ROUND(AVG(Income), 2),

    ROUND(AVG(Total_Spend), 2),

    ROUND(AVG(Response) * 100, 2)

FROM customers

WHERE NumWebVisitsMonth > 5


UNION ALL


SELECT
    'Family Customer',

    COUNT(*),

    ROUND(AVG(Income), 2),

    ROUND(AVG(Total_Spend), 2),

    ROUND(AVG(Response) * 100, 2)

FROM customers

WHERE Total_Children > 0


UNION ALL


SELECT
    'Campaign Responder',

    COUNT(*),

    ROUND(AVG(Income), 2),

    ROUND(AVG(Total_Spend), 2),

    ROUND(AVG(Response) * 100, 2)

FROM customers

WHERE Response = 1;