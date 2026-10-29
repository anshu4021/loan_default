"""
Realistic Credit Risk Dataset Generator
Generates a comprehensive loan applicant dataset reflecting realistic distributions,
covariances, and default probabilities based on real-world credit risk underwriting standards
(similar to LendingClub, German Credit, and Fannie Mae benchmarks).
"""

import os
import numpy as np
import pandas as pd

def generate_credit_data(num_samples: int = 12000, random_state: int = 42) -> pd.DataFrame:
    np.random.seed(random_state)
    
    # 1. Demographics & Employment
    age = np.clip(np.random.normal(35, 11, num_samples).astype(int), 19, 72)
    emp_length = np.clip(np.random.exponential(scale=6, size=num_samples).astype(int), 0, age - 18)
    
    # Annual income (log-normal distribution)
    income = np.exp(np.random.normal(10.9, 0.55, num_samples))
    income = np.clip(np.round(income, -2), 15000, 350000)
    
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
    
    # Debt-to-Income (DTI) ratio (excluding proposed loan)
    dti = np.clip(np.random.beta(2, 5, num_samples) * 0.75, 0.05, 0.65)
    
    # 3. Loan Details
    loan_intent = np.random.choice(
        ['DEBTCONSOLIDATION', 'EDUCATION', 'MEDICAL', 'PERSONAL', 'HOMEIMPROVEMENT', 'VENTURE'],
        size=num_samples,
        p=[0.35, 0.18, 0.15, 0.14, 0.10, 0.08]
    )
    
    # Loan amount requested
    max_affordable_loan = income * 0.55
    raw_loan_amnt = np.random.gamma(shape=3.5, scale=4000, size=num_samples)
    loan_amnt = np.clip(np.round(np.minimum(raw_loan_amnt, max_affordable_loan), -2), 1000, 40000)
    
    # Loan percent of annual income
    loan_percent_income = np.round(loan_amnt / income, 4)
    
    # Loan Grade & Interest Rate based on Credit Score and DTI
    grade_risk_score = (850 - credit_score) / 50 + (dti * 10) + np.where(default_on_file == 'Y', 10, 0)
    grades = []
    int_rates = []
    for score in grade_risk_score:
        if score < 5:
            g = 'A'
            ir = np.random.normal(7.2, 0.8)
        elif score < 7.5:
            g = 'B'
            ir = np.random.normal(10.5, 1.1)
        elif score < 10:
            g = 'C'
            ir = np.random.normal(13.8, 1.4)
        elif score < 12.5:
            g = 'D'
            ir = np.random.normal(17.2, 1.6)
        elif score < 15:
            g = 'E'
            ir = np.random.normal(20.5, 1.8)
        else:
            g = 'F'
            ir = np.random.normal(23.8, 2.0)
        grades.append(g)
        int_rates.append(np.clip(np.round(ir, 2), 5.25, 29.99))
    
    loan_grade = np.array(grades)
    loan_int_rate = np.array(int_rates)
    
    # 4. Latent Default Probability Simulation
    # Real-world underwriting risk formula with realistic non-linear logit relationships
    z = (
        -3.80
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
        'loan_grade': loan_grade,
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
    data_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(data_dir, 'loan_data.csv')
    df = generate_credit_data(num_samples=12000, random_state=42)
    df.to_csv(output_path, index=False)
    print(f"[+] Successfully generated realistic dataset at: {output_path}")
    print(f"    Total records: {len(df)}")
    print(f"    Default rate: {df['loan_status'].mean()*100:.2f}%")
    print(df.head())
