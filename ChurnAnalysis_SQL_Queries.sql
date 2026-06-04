-- ============================================================
-- CUSTOMER CHURN ANALYSIS — SQL QUERIES
-- Author: Simpson Gundlapally
-- Dataset: churn_raw_data.csv (5,000 records)
-- Tool: SQL (MySQL / PostgreSQL / SQLite)
-- ============================================================

-- ============================================================
-- STEP 1: DATA EXPLORATION
-- ============================================================

-- 1.1 Preview raw data
SELECT * FROM customer_churn LIMIT 10;

-- 1.2 Total record count
SELECT COUNT(*) AS total_records FROM customer_churn;

-- 1.3 Overall churn rate
SELECT
    COUNT(*) AS total_customers,
    SUM(Churn) AS churned,
    COUNT(*) - SUM(Churn) AS retained,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customer_churn;

-- ============================================================
-- STEP 2: DATA CLEANING
-- ============================================================

-- 2.1 Find records with negative tenure
SELECT Customer_ID, Tenure_Months, Monthly_Charge
FROM customer_churn
WHERE Tenure_Months < 0;

-- 2.2 Find records with missing charges
SELECT Customer_ID, Tenure_Months, Monthly_Charge, Total_Charges
FROM customer_churn
WHERE Monthly_Charge IS NULL OR Total_Charges IS NULL;

-- 2.3 Dirty record count summary
SELECT
    SUM(CASE WHEN Tenure_Months < 0 THEN 1 ELSE 0 END)         AS negative_tenure,
    SUM(CASE WHEN Monthly_Charge IS NULL THEN 1 ELSE 0 END)     AS missing_charges,
    SUM(CASE WHEN Total_Charges IS NULL THEN 1 ELSE 0 END)      AS missing_total,
    COUNT(*) AS total_rows
FROM customer_churn;

-- 2.4 Create cleaned view
CREATE VIEW churn_clean AS
SELECT *
FROM customer_churn
WHERE
    Tenure_Months >= 0
    AND Monthly_Charge IS NOT NULL
    AND Total_Charges IS NOT NULL;

SELECT COUNT(*) AS clean_records FROM churn_clean;

-- ============================================================
-- STEP 3: CHURN DRIVER ANALYSIS
-- ============================================================

-- 3.1 Churn by Contract Type (KEY INSIGHT)
SELECT
    Contract_Type,
    COUNT(*) AS total_customers,
    SUM(Churn) AS churned,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 1) AS churn_rate_pct
FROM churn_clean
GROUP BY Contract_Type
ORDER BY churn_rate_pct DESC;

-- 3.2 Churn by Tenure Segment (Critical onboarding window)
SELECT
    CASE
        WHEN Tenure_Months BETWEEN 0  AND 12 THEN '0-12 Months'
        WHEN Tenure_Months BETWEEN 13 AND 24 THEN '13-24 Months'
        WHEN Tenure_Months BETWEEN 25 AND 48 THEN '25-48 Months'
        ELSE '49+ Months'
    END AS Tenure_Segment,
    COUNT(*) AS total,
    SUM(Churn) AS churned,
    ROUND(SUM(Churn)*100.0/COUNT(*), 1) AS churn_rate_pct
FROM churn_clean
GROUP BY Tenure_Segment
ORDER BY churn_rate_pct DESC;

-- 3.3 Churn by Payment Method
SELECT
    Payment_Method,
    COUNT(*) AS total,
    SUM(Churn) AS churned,
    ROUND(SUM(Churn)*100.0/COUNT(*), 1) AS churn_rate_pct
FROM churn_clean
GROUP BY Payment_Method
ORDER BY churn_rate_pct DESC;

-- 3.4 Churn by Internet Service
SELECT
    Internet_Service,
    COUNT(*) AS total,
    SUM(Churn) AS churned,
    ROUND(SUM(Churn)*100.0/COUNT(*), 1) AS churn_rate_pct
FROM churn_clean
GROUP BY Internet_Service
ORDER BY churn_rate_pct DESC;

-- 3.5 Average monthly charge — Churned vs Retained
SELECT
    CASE WHEN Churn = 1 THEN 'Churned' ELSE 'Retained' END AS status,
    COUNT(*) AS customers,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge,
    ROUND(AVG(Tenure_Months), 1)  AS avg_tenure_months,
    ROUND(AVG(Support_Calls), 2)  AS avg_support_calls
FROM churn_clean
GROUP BY Churn;

-- ============================================================
-- STEP 4: REVENUE IMPACT
-- ============================================================

-- 4.1 Monthly revenue at risk from churned customers
SELECT
    ROUND(SUM(Monthly_Charge), 2) AS monthly_revenue_at_risk,
    COUNT(*) AS churned_customers,
    ROUND(AVG(Monthly_Charge), 2) AS avg_charge_churned
FROM churn_clean
WHERE Churn = 1;

-- 4.2 Revenue impact by contract type
SELECT
    Contract_Type,
    SUM(CASE WHEN Churn=1 THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn=1 THEN Monthly_Charge ELSE 0 END), 2) AS monthly_rev_lost,
    ROUND(SUM(CASE WHEN Churn=1 THEN Total_Charges ELSE 0 END), 2)  AS lifetime_rev_lost
FROM churn_clean
GROUP BY Contract_Type
ORDER BY monthly_rev_lost DESC;

-- ============================================================
-- STEP 5: KPI SUMMARY (for Power BI Cards)
-- ============================================================
SELECT
    COUNT(*) AS total_customers,
    SUM(Churn) AS churned_customers,
    COUNT(*) - SUM(Churn) AS retained_customers,
    ROUND(SUM(Churn)*100.0/COUNT(*), 1) AS churn_rate_pct,
    ROUND((COUNT(*)-SUM(Churn))*100.0/COUNT(*), 1) AS retention_rate_pct,
    ROUND(AVG(Tenure_Months), 1) AS avg_tenure_months,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_charge,
    ROUND(SUM(CASE WHEN Churn=1 THEN Monthly_Charge ELSE 0 END), 2) AS monthly_rev_at_risk
FROM churn_clean;
