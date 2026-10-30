"""
Interactive CLI Underwriting Prototype
Allows credit analysts to score loan applicants, inspect real-time SHAP/LIME
feature attributions, and generate ECOA Adverse Action Notices directly from terminal.
"""

import os
import sys
import json
import numpy as np
import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from src.preprocessing import load_pipeline
from src.model_trainer import load_trained_model
from src.explainers import LoanXAIExplainer
from src.compliance import AdverseActionGenerator

def load_system():
    models_dir = os.path.join(base_dir, 'models')
    pipeline = load_pipeline(os.path.join(models_dir, 'pipeline.joblib'))
    model = load_trained_model(os.path.join(models_dir, 'champion_xgboost.joblib'))
    
    # Load small reference background sample
    dataset_path = os.path.join(base_dir, 'dataset', 'loan_data_100k.csv')
    df_sample = pd.read_csv(dataset_path).head(300)
    X_sample, _, _, _, _ = pipeline.fit_transform(df_sample)
    
    explainer = LoanXAIExplainer(model, X_sample, pipeline.feature_names)
    compliance = AdverseActionGenerator(approval_threshold=0.35)
    return pipeline, model, explainer, compliance

def evaluate_applicant(applicant_data: dict, applicant_id: str, pipeline, model, explainer, compliance):
    print("\n" + "="*70)
    print(f" 🏦 APPLICANT UNDERWRITING EVALUATION: [{applicant_id}]")
    print("="*70)
    
    # Display Input summary
    print(f"Age: {applicant_data['person_age']} yrs | Income: ${applicant_data['person_income']:,} | FICO: {applicant_data['credit_score']}")
    print(f"Requested Loan: ${applicant_data['loan_amnt']:,} | Purpose: {applicant_data['loan_intent']} | Grade: {applicant_data['loan_grade']}")
    print(f"Loan-to-Income: {applicant_data['loan_percent_income']*100:.1f}% | DTI: {applicant_data['debt_to_income']*100:.1f}% | Prior Default: {applicant_data['cb_person_default_on_file']}")
    print("-" * 70)
    
    # Transform and Predict
    df_trans = pipeline.transform_single_applicant(applicant_data)
    prob_default = float(model.predict_proba(df_trans)[0, 1])
    is_denied = prob_default >= 0.35
    
    status = "\033[91mDENIED [HIGH RISK]\033[0m" if is_denied else "\033[92mAPPROVED [LOW RISK]\033[0m"
    print(f"Decision: {status}")
    print(f"Predicted Probability of Default (PD): {prob_default*100:.2f}% (Underwriting Policy Cutoff: 35.0%)")
    print("-" * 70)
    
    # SHAP Attribution
    print("📊 SHAP (Game Theory) Feature Attributions:")
    shap_res = explainer.shap_explainer(df_trans)[0]
    attr_df, risk_up, risk_down = explainer.get_applicant_shap_contributions(shap_res)
    
    print("\n  🔺 Top Drivers INCREASING Default Risk:")
    for _, r in risk_up.head(4).iterrows():
        print(f"     + {r['Feature']:<30} = {r['Feature_Value']:<8} (Impact: +{r['SHAP_Value']:.4f})")
        
    print("\n  🔻 Top Drivers REDUCING Default Risk:")
    for _, r in risk_down.head(4).iterrows():
        print(f"     - {r['Feature']:<30} = {r['Feature_Value']:<8} (Impact: {r['SHAP_Value']:.4f})")
        
    # Adverse Action Notice if Denied
    if is_denied:
        print("\n" + "-" * 70)
        print("📜 OFFICIAL ADVERSE ACTION NOTICE (ECOA REGULATION B / CFPB COMPLIANT)")
        print("-" * 70)
        notice = compliance.generate_notice(applicant_id, prob_default, attr_df)
        print(f"Statement of Credit Denial Reference: {notice['applicant_id']}")
        print("Mandatory Principal Reasons for Credit Denial:")
        for idx, reason in enumerate(notice['actionable_reasons'], 1):
            print(f"  {idx}. {reason['notice_statement']}")
            print(f"     [Metric: {reason['feature']} = {reason['current_value']} | SHAP Weight: +{reason['impact_score']:.4f}]")
        print("\nActionable Counterfactual Recourse for Consumer:")
        for rec in notice['actionable_recourse']:
            print(f"  • {rec}")
    else:
        print("\n✅ Applicant satisfies all underwriting risk guidelines. Eligible for automatic origination.")
    print("=" * 70 + "\n")

def main():
    print("=" * 70)
    print(" EXPLAINABLE AI LOAN UNDERWRITING: CLI WORKING PROTOTYPE")
    print("=" * 70)
    print("[*] Loading trained pipeline, XGBoost model, and XAI explainers...")
    pipeline, model, explainer, compliance = load_system()
    print("[+] System initialized successfully.\n")
    
    samples_path = os.path.join(os.path.dirname(__file__), 'sample_applicants.json')
    with open(samples_path, 'r') as f:
        samples = json.load(f)
        
    while True:
        print("\nSelect an option:")
        print("1. Test Prime Applicant (Sarah Jenkins - Low Risk)")
        print("2. Test Subprime Applicant (David Martinez - High Risk / Denied)")
        print("3. Test Borderline Applicant (Alex Taylor - Near Threshold)")
        print("4. Enter Custom Applicant Details")
        print("5. Exit")
        
        choice = input("\nEnter choice [1-5]: ").strip()
        if choice == '1':
            evaluate_applicant(samples[0]['data'], samples[0]['applicant_id'], pipeline, model, explainer, compliance)
        elif choice == '2':
            evaluate_applicant(samples[1]['data'], samples[1]['applicant_id'], pipeline, model, explainer, compliance)
        elif choice == '3':
            evaluate_applicant(samples[2]['data'], samples[2]['applicant_id'], pipeline, model, explainer, compliance)
        elif choice == '4':
            try:
                age = int(input("Age (e.g. 35): ") or 35)
                income = int(input("Annual Income ($) (e.g. 55000): ") or 55000)
                emp = int(input("Employment Length in Yrs (e.g. 4): ") or 4)
                loan_amnt = int(input("Loan Amount ($) (e.g. 15000): ") or 15000)
                fico = int(input("FICO Credit Score (350-850) (e.g. 640): ") or 640)
                dti = float(input("Debt to Income ratio (0.05-0.65) (e.g. 0.35): ") or 0.35)
                prior_def = input("Prior Default on Bureau? (Y/N) (e.g. N): ").strip().upper() or 'N'
                home = input("Home Ownership (RENT/MORTGAGE/OWN) (e.g. RENT): ").strip().upper() or 'RENT'
                intent = input("Loan Intent (PERSONAL/EDUCATION/DEBTCONSOLIDATION/MEDICAL) (e.g. PERSONAL): ").strip().upper() or 'PERSONAL'
                grade = input("Loan Grade (A/B/C/D/E/F) (e.g. C): ").strip().upper() or 'C'
                
                custom_app = {
                    'person_age': age, 'person_income': income, 'person_emp_length': emp,
                    'loan_intent': intent, 'loan_grade': grade, 'loan_amnt': loan_amnt,
                    'loan_int_rate': 14.0, 'loan_percent_income': round(loan_amnt / income, 4),
                    'debt_to_income': dti, 'credit_score': fico, 'cb_person_default_on_file': prior_def,
                    'cb_person_cred_hist_length': max(1, age - 21), 'person_home_ownership': home
                }
                evaluate_applicant(custom_app, "CUSTOM-USER-INPUT", pipeline, model, explainer, compliance)
            except Exception as e:
                print(f"Error parsing custom input: {e}")
        elif choice == '5':
            print("Exiting prototype. Goodbye!")
            break
        else:
            print("Invalid choice, please select 1-5.")

if __name__ == '__main__':
    main()
