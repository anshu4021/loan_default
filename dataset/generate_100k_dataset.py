"""
100,000 (1 Lakh) Realistic Credit Risk Dataset Generator
Generates an enterprise-scale credit risk dataset of 100,000 loan applicants
with realistic financial distributions, non-linear default mechanics,
and multi-tier credit bureau risk indicators.
"""

import os
import json
import numpy as np
import pandas as pd

def generate_credit_data_100k(num_samples: int = 100000, random_state: int = 42) -> pd.DataFrame:
    print(f"[*] Generating {num_samples:,} (1 Lakh) loan applicant records with seed={random_state}...")
    np.random.seed(random_state)
    
    # 1. Demographics & Employment
    age = np.clip(np.random.normal(36, 11, num_samples).astype(int), 19, 75)
    emp_length = np.clip(np.random.exponential(scale=6, size=num_samples).astype(int), 0, age - 18)
    
    # Annual income (log-normal distribution)
    income = np.exp(np.random.normal(10.95, 0.55, num_samples))
    income = np.clip(np.round(income, -2), 15000, 450000)
    
    home_ownership = np.random.choice(
        ['RENT', 'MORTGAGE', 'OWN', 'OTHER'],
        size=num_samples,
        p=[0.48, 0.42, 0.08, 0.02]
    )
    
    # 2. Credit Bureau History
    cred_hist_length = np.clip(np.random.normal(age - 21, 4, num_samples).astype(int), 1, age - 18)
    default_on_file = np.random.choice(['N', 'Y'], size=num_samples, p=[0.82, 0.18])
    
    # FICO Credit Score (300 - 850)
    base_fico = np.random.normal(675, 55, num_samples)
    fico_penalty = np.where(default_on_file == 'Y', 70, 0)
    credit_score = np.clip(np.round(base_fico - fico_penalty), 350, 850).astype(int)
    
    # Debt-to-Income (DTI) ratio
    dti = np.clip(np.random.beta(2, 5, num_samples) * 0.75, 0.05, 0.65)
    
    # 3. Loan Details
    loan_intent = np.random.choice(
        ['DEBTCONSOLIDATION', 'EDUCATION', 'MEDICAL', 'PERSONAL', 'HOMEIMPROVEMENT', 'VENTURE'],
        size=num_samples,
        p=[0.35, 0.18, 0.15, 0.14, 0.10, 0.08]
    )
    
    # Loan amount requested
    max_affordable_loan = income * 0.55
    raw_loan_amnt = np.random.gamma(shape=3.5, scale=4200, size=num_samples)
    loan_amnt = np.clip(np.round(np.minimum(raw_loan_amnt, max_affordable_loan), -2), 1000, 45000)
    
    # Loan percent of annual income
    loan_percent_income = np.round(loan_amnt / income, 4)
    
    # Loan Grade & Interest Rate based on Credit Score and DTI
    grade_risk_score = (850 - credit_score) / 50 + (dti * 10) + np.where(default_on_file == 'Y', 10, 0)
    
    # Vectorized grade & interest assignment
    grades = np.empty(num_samples, dtype=object)
    int_rates = np.empty(num_samples, dtype=float)
    
    m_a = grade_risk_score < 5
    m_b = (grade_risk_score >= 5) & (grade_risk_score < 7.5)
    m_c = (grade_risk_score >= 7.5) & (grade_risk_score < 10)
    m_d = (grade_risk_score >= 10) & (grade_risk_score < 12.5)
    m_e = (grade_risk_score >= 12.5) & (grade_risk_score < 15)
    m_f = grade_risk_score >= 15
    
    grades[m_a] = 'A'
    int_rates[m_a] = np.random.normal(7.2, 0.8, m_a.sum())
    
    grades[m_b] = 'B'
    int_rates[m_b] = np.random.normal(10.5, 1.1, m_b.sum())
    
    grades[m_c] = 'C'
    int_rates[m_c] = np.random.normal(13.8, 1.4, m_c.sum())
    
    grades[m_d] = 'D'
    int_rates[m_d] = np.random.normal(17.2, 1.6, m_d.sum())
    
    grades[m_e] = 'E'
    int_rates[m_e] = np.random.normal(20.5, 1.8, m_e.sum())
    
    grades[m_f] = 'F'
    int_rates[m_f] = np.random.normal(23.8, 2.0, m_f.sum())
    
    loan_int_rate = np.clip(np.round(int_rates, 2), 5.25, 29.99)
    
    # 4. Latent Default Probability Simulation
    # Real-world underwriting risk formula with realistic non-linear logit relationships
    z = (
        -3.85
        + 5.2 * (loan_percent_income)
        + 3.8 * (dti)
        + 0.12 * (loan_int_rate - 12.0)
        - 0.015 * (credit_score - 650)
        + 1.45 * (default_on_file == 'Y')
        - 0.03 * (emp_length)
        - 0.02 * (cred_hist_length)
        + 0.35 * (home_ownership == 'RENT')
        - 0.40 * (home_ownership == 'OWN')
        + 0.40 * (loan_intent == 'DEBTCONSOLIDATION')
        + 0.50 * (loan_intent == 'MEDICAL')
        + np.random.normal(0, 0.4, num_samples) # Unobserved behavioral noise
    )
    
    prob_default = 1 / (1 + np.exp(-z))
    loan_status = (np.random.binomial(1, prob_default)).astype(int)
    
    df = pd.DataFrame({
        'person_age': age,
        'person_income': income.astype(int),
        'person_home_ownership': home_ownership,
        'person_emp_length': emp_length,
        'loan_intent': loan_intent,
        'loan_grade': grades,
        'loan_amnt': loan_amnt.astype(int),
        'loan_int_rate': loan_int_rate,
        'loan_percent_income': loan_percent_income,
        'debt_to_income': np.round(dti, 3),
        'credit_score': credit_score,
        'cb_person_default_on_file': default_on_file,
        'cb_person_cred_hist_length': cred_hist_length,
        'loan_status': loan_status  # Target: 1 = Default, 0 = Non-default
    })
    
    return df

if __name__ == '__main__':
    dataset_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(dataset_dir, 'loan_data_100k.csv')
    df = generate_credit_data_100k(num_samples=100000, random_state=42)
    df.to_csv(output_path, index=False)
    
    default_rate = df['loan_status'].mean() * 100
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    
    print(f"[+] Successfully generated 1 Lakh dataset: {output_path}")
    print(f"    Total records: {len(df):,}")
    print(f"    File size: {file_size_mb:.2f} MB")
    print(f"    Default rate: {default_rate:.2f}%")
    
    # Save dataset summary metadata
    summary = {
        "dataset_name": "Credit Risk & Loan Default Benchmark Dataset (1 Lakh)",
        "total_records": len(df),
        "total_features": len(df.columns) - 1,
        "target_variable": "loan_status",
        "default_count": int(df['loan_status'].sum()),
        "non_default_count": int((df['loan_status'] == 0).sum()),
        "default_rate_pct": round(default_rate, 2),
        "file_size_mb": round(file_size_mb, 2),
        "feature_summary": {
            col: {
                "dtype": str(df[col].dtype),
                "unique_values": int(df[col].nunique()),
                "missing_values": int(df[col].isnull().sum())
            } for col in df.columns
        }
    }
    
    summary_path = os.path.join(dataset_dir, 'dataset_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"[+] Saved dataset summary: {summary_path}")
