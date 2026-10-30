# 📖 Technical Documentation 05: Data Dictionary, Feature Schemas & Preprocessing

This document details the feature schemas, summary statistics, valid ranges, and transformation pipelines for the 100,000 credit risk dataset.

---

## 📋 Comprehensive Feature Dictionary

| Feature Name | Type | Unit / Encoding | Mean $\pm$ Std | Valid Range | Business Role |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `person_age` | Numeric | Years | $36.0 \pm 11.0$ | $19 - 75$ | Borrower maturity & employment stability |
| `person_income` | Numeric | USD (\$) | $\$62,400 \pm \$38,100$ | $\$15,000 - \$450,000$ | Verification of annual debt service capacity |
| `person_emp_length` | Numeric | Years | $5.9 \pm 5.8$ | $0 - 50$ | Tenure stability with current employer |
| `loan_amnt` | Numeric | USD (\$) | $\$14,600 \pm \$8,900$ | $\$1,000 - \$45,000$ | Exposure at Default (EAD) |
| `loan_int_rate` | Numeric | Percentage (%) | $13.82\% \pm 4.31\%$ | $5.25\% - 29.99\%$ | Borrowing cost compounding default risk |
| `loan_percent_income` | Numeric | Ratio | $0.234 \pm 0.141$ | $0.003 - 0.550$ | Debt-to-income leverage burden |
| `debt_to_income` (DTI) | Numeric | Ratio | $0.214 \pm 0.125$ | $0.050 - 0.650$ | Existing revolving and installment debt load |
| `credit_score` | Numeric | FICO (300-850) | $662 \pm 62$ | $350 - 850$ | Bureau repayment reliability score |
| `cb_person_cred_hist_length`| Numeric | Years | $15.0 \pm 8.2$ | $1 - 54$ | Credit bureau depth and track record |
| `loan_grade` | Categorical | `A, B, C, D, E, F` | Mode: `B` | 6 Ordinal Tiers | Underwriting pricing and risk grade |
| `person_home_ownership` | Nominal | `RENT, MORTGAGE, OWN, OTHER`| Mode: `RENT` | 4 Categories | Housing fixed expenditure indicator |
| `loan_intent` | Nominal | 6 Categories | Mode: `DEBTCONSOLIDATION` | 6 Categories | Credit application stated purpose |
| `cb_person_default_on_file` | Binary | `Y` (18%), `N` (82%) | Mode: `N` | 2 Categories | Public derogatory or historical charge-off |
| `loan_status` (Target) | Binary | `0` (Paid), `1` (Default) | Default Rate: $26.89\%$ | $\{0, 1\}$ | Supervised classification target |

---

## ⚙️ Transformation & Pipeline Steps (`CreditDataPipeline`)

1. **Missing Value Imputation**: Continuous variables imputed with median; categorical with mode.
2. **Ordinal Mapping**: `loan_grade` mapped monotonically: `{'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}`.
3. **Binary Encoding**: `cb_person_default_on_file` mapped to $\{0, 1\}$.
4. **Nominal One-Hot Encoding**: `person_home_ownership` (4 dummies) and `loan_intent` (6 dummies).
5. **Stratified Split**: Preserves $26.89\%$ default ratio across train (80,000) and test (20,000) partitions.
