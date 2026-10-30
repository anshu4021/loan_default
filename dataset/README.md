# 📊 Credit Risk Dataset (1 Lakh / 100,000 Records)

This dataset contains **100,000 (1 Lakh)** synthetic loan applicant profiles reflecting real-world consumer credit risk underwriting standards (benchmarked against LendingClub, Fannie Mae, and FICO score distributions).

---

## 📌 Dataset Summary

| Property | Value |
| :--- | :--- |
| **Total Rows (Applicants)** | **100,000** |
| **Total Columns (Features)** | **14 (13 Predictors + 1 Target)** |
| **File Format** | CSV (`loan_data_100k.csv`) |
| **File Size** | **6.51 MB** |
| **Target Variable** | `loan_status` (Binary: `1` = Default, `0` = Fully Paid) |
| **Default Rate** | **26.89%** (26,888 defaults, 73,112 non-defaults) |
| **Missing Values** | None (Fully imputed / clean benchmark) |

---

## 📋 Data Dictionary

| # | Column Name | Data Type | Description | Range / Categories | Business Importance |
|---|:---|:---:|:---|:---:|:---|
| 1 | `person_age` | `int` | Applicant age in years | 19 – 75 | Borrower career maturity and stability |
| 2 | `person_income` | `int` | Annual verifiable gross income ($) | \$15,000 – \$450,000 | Primary capacity-to-pay metric |
| 3 | `person_home_ownership` | `str` | Residential home ownership status | `RENT`, `MORTGAGE`, `OWN`, `OTHER` | Housing expense burden indicator |
| 4 | `person_emp_length` | `int` | Current employment tenure (years) | 0 – 50 | Income continuity & stability |
| 5 | `loan_intent` | `str` | Purpose of the loan request | `DEBTCONSOLIDATION`, `EDUCATION`, `MEDICAL`, `PERSONAL`, `HOMEIMPROVEMENT`, `VENTURE` | High-risk purpose categories (e.g., debt consolidation, medical) |
| 6 | `loan_grade` | `str` | Underwriting risk rating tier | `A`, `B`, `C`, `D`, `E`, `F` | Risk classification bucket assigned by underwriting |
| 7 | `loan_amnt` | `int` | Principal loan amount requested ($) | \$1,000 – \$45,000 | Total credit exposure at default (EAD) |
| 8 | `loan_int_rate` | `float` | Annual percentage interest rate (%) | 5.25% – 29.99% | Borrowing cost compounding default risk |
| 9 | `loan_percent_income` | `float` | Loan amount divided by annual income | 0.003 – 0.550 | Overall leverage burden on borrower |
| 10 | `debt_to_income` | `float` | Monthly non-mortgage debt / monthly income | 0.050 – 0.650 | Current recurring credit commitment |
| 11 | `credit_score` | `int` | Credit bureau FICO score | 350 – 850 | Historical credit repayment reliability |
| 12 | `cb_person_default_on_file` | `str` | Historical derogatory record on bureau | `Y` (Yes), `N` (No) | Significant behavioral risk penalty |
| 13 | `cb_person_cred_hist_length` | `int` | Length of credit bureau history (years) | 1 – 54 | Depth of consumer credit file |
| 14 | **`loan_status`** (Target) | `int` | Loan outcome | `0` = Paid, `1` = Default | Dependent variable for ML models |

---

## 🔬 Class Distribution & Imbalance Handling

- **Class 0 (Non-Default / Paid)**: 73,112 (73.11%)
- **Class 1 (Default / Charged-off)**: 26,888 (26.89%)
- **Imbalance Ratio**: Approximately **2.72 : 1**

In production, models use `scale_pos_weight = 2.72` inside XGBoost to ensure minority class sensitivity and avoid trivial majority classification.

---

## 🛠️ How to Regenerate or Sample

```bash
# Generate the full 1 Lakh dataset
python dataset/generate_100k_dataset.py
```
