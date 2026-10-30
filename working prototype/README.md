# 🚀 Working Prototype: Explainable Loan Underwriting

This directory provides self-contained working prototypes of the Explainable AI Credit Risk Engine across **Web UI**, **Terminal CLI**, and **REST API** modes.

---

## 🖥️ 1. Interactive Web Application (Streamlit)

Launch the full underwriter dashboard with applicant sliders, live gauges, SHAP waterfall plots, LIME rules, and one-click Adverse Action generation:

```bash
# From project root:
streamlit run app.py

# Or on Windows using batch launcher:
working prototype/run_prototype.bat  # Select Option 1
```

---

## ⌨️ 2. Terminal Command Line Interface (CLI)

Run interactive risk evaluations directly in your terminal, with instant color-coded approvals/denials, top positive/negative SHAP feature drivers, and official CFPB Adverse Action notices:

```bash
cd "working prototype"
python cli_prototype.py
```

### Pre-loaded Test Cases in CLI:
- **Sarah Jenkins (Prime Approved)**: Low leverage ($12k loan on $95k income), 780 FICO, 18% DTI $\rightarrow$ **Approved (Low Default Risk)**.
- **David Martinez (Subprime Denied)**: Severe debt burden ($18k loan on $32k income), 520 FICO, prior default on file $\rightarrow$ **Denied (High Default Risk)** with Adverse Action Notice & Counterfactuals.
- **Alex Taylor (Borderline)**: Moderate credit score, 35% loan-to-income $\rightarrow$ Detailed margin assessment.
- **Custom Input**: Enter any arbitrary applicant profile to score in real-time.

---

## 🔌 3. REST API Service (Standalone)

Start the lightweight REST API microservice:

```bash
cd "working prototype"
python api_prototype.py 8080
```

### Example API Calls:

#### Health Check:
```bash
curl http://127.0.0.1:8080/health
```

#### Underwriting Scoring:
```bash
curl -X POST http://127.0.0.1:8080/predict \
     -H "Content-Type: application/json" \
     -d '{
       "applicant_id": "APP-9988",
       "applicant": {
         "person_age": 30, "person_income": 45000, "person_emp_length": 3,
         "loan_intent": "PERSONAL", "loan_grade": "D", "loan_amnt": 18000,
         "loan_int_rate": 18.5, "loan_percent_income": 0.40, "debt_to_income": 0.42,
         "credit_score": 590, "cb_person_default_on_file": "N",
         "cb_person_cred_hist_length": 6, "person_home_ownership": "RENT"
       }
     }'
```

#### Explainability (SHAP Top Drivers):
```bash
curl -X POST http://127.0.0.1:8080/explain \
     -H "Content-Type: application/json" \
     -d @sample_applicants.json
```

#### Adverse Action Notice Generation:
```bash
curl -X POST http://127.0.0.1:8080/adverse-action \
     -H "Content-Type: application/json" \
     -d @sample_applicants.json
```
