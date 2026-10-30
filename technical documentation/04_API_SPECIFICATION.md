# 🔌 Technical Documentation 04: REST API Specification (OpenAPI Schema)

This document specifies the REST API endpoints, JSON request/response schemas, and HTTP status codes for the **Explainable AI Credit Risk API**.

---

## 📌 Endpoint Overview

| Method | Endpoint | Description | Auth Required |
| :---: | :--- | :--- | :---: |
| `GET` | `/health` | Service liveness and model metadata | No |
| `GET` | `/sample-applicants` | Pre-configured test applicant profiles | No |
| `POST` | `/predict` | Default probability & underwriting decision | Optional |
| `POST` | `/explain` | Full SHAP feature attribution breakdown | Optional |
| `POST` | `/adverse-action` | ECOA Regulation B Adverse Action notice | Optional |

---

## 📋 Endpoint Details

### 1. `POST /predict`
Evaluates applicant default probability against the 35% policy threshold.

#### Request Schema:
```json
{
  "applicant_id": "APP-2026-001",
  "applicant": {
    "person_age": 35,
    "person_income": 65000,
    "person_emp_length": 5,
    "loan_intent": "PERSONAL",
    "loan_grade": "B",
    "loan_amnt": 14000,
    "loan_int_rate": 11.25,
    "loan_percent_income": 0.2154,
    "debt_to_income": 0.28,
    "credit_score": 710,
    "cb_person_default_on_file": "N",
    "cb_person_cred_hist_length": 12,
    "person_home_ownership": "MORTGAGE"
  }
}
```

#### Response Schema (HTTP 200 OK):
```json
{
  "applicant_id": "APP-2026-001",
  "decision": "APPROVED",
  "default_probability": 0.0842,
  "default_probability_pct": 8.42,
  "approval_threshold_pct": 35.0,
  "risk_tier": "Prime Quality"
}
```

---

### 2. `POST /adverse-action`
Generates a compliant Statement of Credit Denial for denied applicants.

#### Response Schema (HTTP 200 OK):
```json
{
  "applicant_id": "SUBPRIME-002",
  "decision": "DENIED",
  "predicted_default_probability": 98.51,
  "regulatory_cutoff": 35.0,
  "actionable_reasons": [
    {
      "feature": "credit_score",
      "current_value": 520,
      "impact_score": 1.334,
      "notice_statement": "Credit score does not meet minimum credit tier guidelines"
    },
    {
      "feature": "loan_grade_num",
      "current_value": 4,
      "impact_score": 1.197,
      "notice_statement": "Assigned underwriting risk rating exceeds risk tolerance threshold"
    },
    {
      "feature": "loan_percent_income",
      "current_value": 0.5625,
      "impact_score": 0.780,
      "notice_statement": "High loan amount relative to verifiable annual income"
    },
    {
      "feature": "loan_int_rate",
      "current_value": 21.5,
      "impact_score": 0.742,
      "notice_statement": "High borrowing cost tier assigned based on current credit profile"
    }
  ],
  "actionable_recourse": [
    "Reduce requested loan principal to decrease loan-to-income exposure below 25%.",
    "Maintain 6+ months of on-time payments to rebuild credit score above 650."
  ]
}
```
