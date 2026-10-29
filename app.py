"""
Streamlit Web Application: Explainable Loan Default Prediction
Interactive Risk Scoring, Real-Time SHAP Waterfall, LIME Explanation,
and ECOA-Compliant Adverse Action Notice Generation.
"""

import os
import sys
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.preprocessing import load_pipeline
from src.model_trainer import load_trained_model
from src.explainers import LoanXAIExplainer
from src.compliance import AdverseActionGenerator

# Streamlit Page Setup
st.set_page_config(
    page_title="FinExplain: Loan Default XAI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_artifacts():
    models_dir = os.path.join(BASE_DIR, 'models')
    pipeline_path = os.path.join(models_dir, 'pipeline.joblib')
    model_path = os.path.join(models_dir, 'champion_xgboost.joblib')
    
    if not os.path.exists(pipeline_path) or not os.path.exists(model_path):
        return None, None, None
        
    pipeline = load_pipeline(pipeline_path)
    model = load_trained_model(model_path)
    
    # Initialize explainer with small sample from training distribution
    csv_path = os.path.join(BASE_DIR, 'data', 'loan_data.csv')
    raw_df = pd.read_csv(csv_path)
    X_train, _, _, _, _ = pipeline.fit_transform(raw_df)
    explainer = LoanXAIExplainer(model, X_train.iloc[:500], pipeline.feature_names)
    
    return pipeline, model, explainer

def main():
    st.title("🏦 Explainable AI for Loan Default Prediction")
    st.caption("Underwriting Risk Assessment powered by XGBoost, SHAP (TreeExplainer), and LIME")

    pipeline, model, explainer = load_artifacts()

    if pipeline is None:
        st.warning("⚠️ Model artifacts not found! Please run `python run_pipeline.py` first to generate models and data.")
        st.info("You can also run the training pipeline directly from your terminal.")
        return

    # Sidebar: Applicant Profile Inputs
    st.sidebar.header("📋 Loan Applicant Profile")
    
    col_sb1, col_sb2 = st.sidebar.columns(2)
    with col_sb1:
        age = st.number_input("Age", min_value=18, max_value=85, value=34, step=1)
        income = st.number_input("Annual Income ($)", min_value=10000, max_value=500000, value=58000, step=2000)
        emp_length = st.number_input("Employment (Yrs)", min_value=0, max_value=45, value=4, step=1)
    with col_sb2:
        credit_score = st.slider("FICO Score", min_value=350, max_value=850, value=640, step=5)
        dti = st.slider("Debt-to-Income (DTI)", min_value=0.05, max_value=0.70, value=0.38, step=0.01)
        cred_hist = st.number_input("Credit Hist (Yrs)", min_value=1, max_value=40, value=8, step=1)

    loan_amnt = st.sidebar.number_input("Requested Loan ($)", min_value=1000, max_value=50000, value=22000, step=1000)
    loan_intent = st.sidebar.selectbox("Loan Intent", ['DEBTCONSOLIDATION', 'EDUCATION', 'MEDICAL', 'PERSONAL', 'HOMEIMPROVEMENT', 'VENTURE'])
    home_ownership = st.sidebar.selectbox("Home Ownership", ['RENT', 'MORTGAGE', 'OWN', 'OTHER'])
    default_on_file = st.sidebar.selectbox("Prior Default on File?", ['N', 'Y'], index=0)
    loan_grade = st.sidebar.selectbox("Credit Rating Grade", ['A', 'B', 'C', 'D', 'E', 'F'], index=2)

    # Calculate derived features
    loan_percent_income = round(loan_amnt / income, 4)
    # Estimated interest rate benchmark
    int_rate_map = {'A': 7.5, 'B': 10.8, 'C': 14.2, 'D': 17.5, 'E': 21.0, 'F': 24.5}
    loan_int_rate = int_rate_map.get(loan_grade, 14.0)

    applicant_data = {
        'person_age': age,
        'person_income': income,
        'person_emp_length': emp_length,
        'loan_intent': loan_intent,
        'loan_grade': loan_grade,
        'loan_amnt': loan_amnt,
        'loan_int_rate': loan_int_rate,
        'loan_percent_income': loan_percent_income,
        'debt_to_income': dti,
        'credit_score': credit_score,
        'cb_person_default_on_file': default_on_file,
        'cb_person_cred_hist_length': cred_hist,
        'person_home_ownership': home_ownership
    }

    # Transform applicant input
    X_applicant_df = pipeline.transform_single_applicant(applicant_data)
    applicant_array = np.array(X_applicant_df.iloc[0])

    # Run Prediction
    pred_prob = model.predict_proba(X_applicant_df)[0, 1]
    cutoff_threshold = 0.35
    is_denied = pred_prob >= cutoff_threshold

    # Main Dashboard Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Underwriting Decision",
        "🌳 SHAP Explanation (Game Theory)",
        "🍋 LIME Explanation (Local Surrogate)",
        "📜 ECOA Adverse Action Notice"
    ])

    with tab1:
        st.subheader("Automated Underwriting Assessment")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        status_color = "🔴 DENIED" if is_denied else "🟢 APPROVED"
        col_m1.metric("Underwriting Decision", status_color)
        col_m2.metric("Default Probability", f"{pred_prob*100:.1f}%")
        col_m3.metric("Policy Cutoff Limit", f"{cutoff_threshold*100:.1f}%")
        col_m4.metric("Loan-to-Income Exposure", f"{loan_percent_income*100:.1f}%")

        if is_denied:
            st.error(f"🚨 **High Default Risk**: Applicant default probability ({pred_prob*100:.1f}%) exceeds the 35% risk threshold. Loan cannot be auto-approved.")
        else:
            st.success(f"✅ **Low Default Risk**: Applicant default probability ({pred_prob*100:.1f}%) is within the safety threshold. Eligible for automated origination.")

        st.markdown("---")
        st.markdown("#### Input Applicant Summary")
        st.dataframe(pd.DataFrame([applicant_data]), use_container_width=True)

    with tab2:
        st.subheader("SHAP TreeExplainer Attribution")
        st.write("SHAP allocates credit for the prediction from the population baseline expected value $E[f(X)]$ to the individual score $f(x)$ using Shapley values.")
        
        with st.spinner("Computing Shapley values..."):
            shap_obj = explainer.shap_explainer(X_applicant_df)[0]
            fig, ax = plt.subplots(figsize=(9, 5))
            import shap
            shap.plots.waterfall(shap_obj, max_display=10, show=False)
            plt.title(f"SHAP Waterfall: Shift from Baseline to Applicant Prediction ({pred_prob*100:.1f}%)", fontsize=11)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        # Tabular Breakdown
        attr_df, risk_up, risk_down = explainer.get_applicant_shap_contributions(shap_obj)
        col_up, col_down = st.columns(2)
        with col_up:
            st.markdown("##### 🔺 Top Factors Increasing Default Risk:")
            st.dataframe(risk_up[['Feature', 'Feature_Value', 'SHAP_Value']], use_container_width=True)
        with col_down:
            st.markdown("##### 🔻 Top Factors Decreasing Default Risk:")
            st.dataframe(risk_down[['Feature', 'Feature_Value', 'SHAP_Value']], use_container_width=True)

    with tab3:
        st.subheader("LIME Local Linear Surrogate")
        st.write("LIME generates 5,000 perturbations around this applicant's profile to approximate the local decision boundary with a sparse interpretable model.")
        
        with st.spinner("Perturbing local neighborhood and fitting surrogate..."):
            lime_exp = explainer.explain_instance_lime(applicant_array, num_features=8)
            fig_lime = lime_exp.as_pyplot_figure(label=1)
            plt.title("LIME Feature Contributions (Default Risk Class)", fontsize=11)
            plt.tight_layout()
            st.pyplot(fig_lime)
            plt.close(fig_lime)

            df_lime = explainer.get_lime_as_dataframe(lime_exp)
            st.markdown("##### Local Rule Explanations:")
            st.dataframe(df_lime, use_container_width=True)

    with tab4:
        st.subheader("Official Adverse Action Notice (ECOA Regulation B / FCRA)")
        st.write("Under Federal Regulation B, credit applicants denied or granted unfavorable terms are entitled to an Adverse Action Notice containing specific, actionable reasons.")

        aan_gen = AdverseActionGenerator(approval_threshold=cutoff_threshold)
        notice = aan_gen.generate_notice(
            applicant_id="APP-STREAMLIT-DEMO",
            default_prob=pred_prob,
            shap_contributions=attr_df
        )

        if not is_denied:
            st.info("ℹ️ Applicant is APPROVED. No Adverse Action Notice required.")
        else:
            st.warning("📄 **Statement of Credit Denial, Termination, or Change**")
            st.markdown(f"**Application Reference:** `{notice['applicant_id']}`")
            st.markdown(f"**Decision:** **{notice['decision']}** (Risk Score: {notice['predicted_default_probability']}%, Cutoff: {notice['regulatory_cutoff']}%)")
            
            st.markdown("#### Key Principal Reasons for Adverse Action:")
            for idx, reason in enumerate(notice['actionable_reasons'], 1):
                st.markdown(f"{idx}. **{reason['notice_statement']}** (Feature: `{reason['feature']}` = `{reason['current_value']}`, SHAP Attribution: `+{reason['impact_score']}`)")

            st.markdown("#### Actionable Recourse (Counterfactual Guidance):")
            for rec in notice['actionable_recourse']:
                st.markdown(f"- 💡 {rec}")

if __name__ == '__main__':
    main()
