"""
Regulatory Compliance & Adverse Action Notice Module
Translates SHAP / XAI attribution weights into legally compliant Adverse Action Notices
under the Equal Credit Opportunity Act (ECOA, 12 CFR Part 1002 - Regulation B)
and the Fair Credit Reporting Act (FCRA).
"""

import pandas as pd
import numpy as np

# Standardized CFPB-aligned Reason Codes
REASON_DICTIONARY = {
    'loan_percent_income': 'High loan amount relative to verifiable annual income',
    'debt_to_income': 'Excessive total monthly debt obligations relative to income (DTI)',
    'credit_score': 'Credit score does not meet minimum credit tier guidelines',
    'cb_person_default_on_file_num': 'Adverse public records or prior delinquency on credit bureau file',
    'loan_int_rate': 'High borrowing cost tier assigned based on current credit profile',
    'loan_grade_num': 'Assigned underwriting risk rating exceeds risk tolerance threshold',
    'loan_amnt': 'Requested principal loan amount exceeds automated risk limits',
    'person_income': 'Insufficient gross annual income for requested credit facility',
    'person_emp_length': 'Length of current employment tenure does not meet criteria',
    'cb_person_cred_hist_length': 'Insufficient length of established credit history',
    'person_home_ownership_RENT': 'Housing status (renter with ongoing fixed housing expenditure)',
    'person_home_ownership_MORTGAGE': 'Substantial mortgage payment obligations',
    'loan_intent_DEBTCONSOLIDATION': 'Consolidation of existing unsecured credit lines',
    'loan_intent_MEDICAL': 'High-risk loan purpose category'
}

class AdverseActionGenerator:
    def __init__(self, approval_threshold: float = 0.35):
        self.approval_threshold = approval_threshold

    def generate_notice(self, applicant_id: str, default_prob: float, shap_contributions: pd.DataFrame) -> dict:
        """
        Generates an Adverse Action Notice if applicant default risk exceeds threshold.
        ECOA Regulation B requires stating up to 4 principal reasons for credit denial.
        """
        is_denied = default_prob >= self.approval_threshold
        status = "DENIED" if is_denied else "APPROVED"
        
        notice = {
            'applicant_id': applicant_id,
            'decision': status,
            'predicted_default_probability': round(default_prob * 100, 2),
            'regulatory_cutoff': round(self.approval_threshold * 100, 2),
            'actionable_reasons': [],
            'actionable_recourse': []
        }

        if not is_denied:
            notice['actionable_reasons'] = ["Applicant satisfies all underwriting risk criteria."]
            return notice

        # Identify top positive contributors to default risk
        risk_drivers = shap_contributions[shap_contributions['SHAP_Value'] > 0].copy()
        risk_drivers = risk_drivers.sort_values(by='SHAP_Value', ascending=False)
        
        top_reasons = []
        for _, row in risk_drivers.head(4).iterrows():
            feat = row['Feature']
            reason_text = REASON_DICTIONARY.get(feat, f"Unfavorable contribution from feature: {feat}")
            top_reasons.append({
                'feature': feat,
                'current_value': row['Feature_Value'],
                'impact_score': round(row['SHAP_Value'], 4),
                'notice_statement': reason_text
            })
        
        notice['actionable_reasons'] = top_reasons

        # Counterfactual Recourse Suggestions (Actionable recommendations)
        recourse = []
        features_present = risk_drivers['Feature'].values
        if 'loan_percent_income' in features_present or 'loan_amnt' in features_present:
            recourse.append("Reduce requested loan principal to decrease loan-to-income exposure below 25%.")
        if 'debt_to_income' in features_present:
            recourse.append("Pay down existing credit card / personal loan balances to bring DTI below 30%.")
        if 'credit_score' in features_present:
            recourse.append("Improve credit score by maintaining 6+ months of on-time payments and resolving delinquent remarks.")
        if len(recourse) == 0:
            recourse.append("Consider applying with a creditworthy co-signer or applying for a lower loan facility.")

        notice['actionable_recourse'] = recourse
        return notice
