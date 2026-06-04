# ChurnAnalysis
Customer churn analysis &amp; risk reporting — Python, SQL, Power BI, 5,000 records, identified 6 churn indicators &amp; ₹85K revenue at risk

#  Telecom Customer Churn Analysis & Risk Reporting

**Author:** Simpson Gundlapally  
**Tools:** Python (Pandas), SQL, Excel, Power BI  
**Dataset:** 5,000 telecom customer records  
**Domain:** Customer Retention | Churn Analytics | Revenue Protection

---

##  Context & Objectives

A telecom provider was experiencing escalating subscriber attrition, causing significant monthly revenue leakage. Without centralized visibility into customer behavior or historical contract performance, leadership lacked a clear picture of *why* subscribers were leaving or *which* segments posed the immediate highest risk.

The objective of this project was to clean raw transactional logs and build a diagnostic analytics pipeline to:
* **Isolate Core Churn Drivers:** Identify structural, behavioral, or contractual triggers behind customer drop-offs.
* **Quantify Revenue Exposure:** Measure the monthly recurring revenue (MRR) actively at risk to justify targeted retention spend.
---

## 📁 Project Structure

```
ChurnAnalysis/
│
├── churn_raw_data.csv              ← Raw dataset (5,000 records, with dirty data)
├── churn_cleaned_data.csv          ← Cleaned dataset (4,800 records)
├── contract_churn_summary.csv      ← Churn rate by contract type
├── tenure_churn_summary.csv        ← Churn rate by tenure segment
├── payment_churn_summary.csv       ← Churn rate by payment method
│
├── churn_queries.sql               ← Full SQL analysis (exploration → KPIs)
├── churn_analysis.py               ← Python analysis (Pandas + Matplotlib)
├── ChurnAnalysis_Complete.xlsx     ← Excel workbook (6 sheets)
│
├── ChurnAnalysis_Dashboard.png     ← Dashboard visualization
└── README.md                       ← This file
```

---

##  Core Performace Metrics

| KPI | Value |
|---|---|
| Total Customers Analyzed | 4,800 |
| Churned Customers | 1,209 |
| Overall Churn Rate | **25.2%** |
| Retention Rate | 74.8% |
| Monthly Revenue at Risk | **₹85,917** |
| Avg Tenure (Churned) | 30.0 months |
| Data Accuracy Rate | 96.0% |

---

## 🧹 Data Cleaning

| Issue | Count |
|---|---|
| Negative tenure values | 66 |
| Missing monthly charge | 68 |
| Missing total charges | 66 |
| **Total dirty records** | **200** |
| **Clean records retained** | **4,800** |

---

## 📊 Key Findings — Churn Drivers

### 1. Contract Type — Strongest Driver
| Contract | Churn Rate |
|---|---|
| Month-to-Month | **38.7%** 🔴 |
| One Year | 14.2% 🟡 |
| Two Year | 9.7% 🟢 |

### 2. Tenure — Early Months Are Critical
| Tenure Segment | Churn Rate |
|---|---|
| 0–12 Months | **41.7%** 🔴 |
| 13–24 Months | 26.5% 🟡 |
| 25–48 Months | 26.0% 🟡 |
| 49+ Months | 15.4% 🟢 |

### 3. Payment Method
| Method | Churn Rate |
|---|---|
| Electronic Check | **28.5%** 🔴 |
| Mailed Check | 24.1% |
| Bank Transfer | 23.9% |
| Credit Card | 21.9% 🟢 |

---

## 💡 Business Recommendations

1. **Priority 1 — Convert Month-to-Month customers** to annual contracts with incentives (discount or added benefits) — can reduce churn by ~24 percentage points
2. **Priority 2 — Launch 90-day onboarding program** for new customers (0–12 month window is most critical)
3. **Priority 3 — Push Electronic Check users** to auto-pay via credit card — 6.6% potential churn reduction
4. **Priority 4 — Flag high support-call customers** for proactive outreach before they churn
5. **Revenue protection** — ₹85,917/month at risk; retaining even 30% of churners saves ~₹25,775/month

---

## 🔧 How to Run

```bash
# 1. Generate dataset
python3 generate_churn_data.py  (already done)

# 2. Run full Python analysis
python3 churn_analysis.py

# 3. SQL analysis
# Load churn_raw_data.csv as table: customer_churn
# Run churn_queries.sql step by step

# 4. Open ChurnAnalysis_Complete.xlsx
# See "Power BI Guide" sheet for dashboard instructions
```

---

## 🏷️ Tags
`Churn Analysis` `Python` `Pandas` `SQL` `Power BI` `Excel` `Customer Retention` `EDA` `KPI Dashboard` `Telecom Analytics`
