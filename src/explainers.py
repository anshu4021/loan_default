"""
Explainable AI (XAI) Engine: SHAP & LIME
Implements SHAP TreeExplainer for global/local game-theoretic attribution
and LIME LimeTabularExplainer for local linear surrogate explanations.
"""

import os
import shap
import lime
import lime.lime_tabular
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class LoanXAIExplainer:
    def __init__(self, model, X_train: pd.DataFrame, feature_names: list = None):
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names if feature_names is not None else list(X_train.columns)
        
        # 1. Initialize SHAP TreeExplainer
        # TreeExplainer calculates exact polynomial-time Shapley values for tree ensembles
        print("[*] Initializing SHAP TreeExplainer...")
        self.shap_explainer = shap.TreeExplainer(self.model)
        
        # 2. Initialize LIME Tabular Explainer
        # Uses training data distributions to sample perturbations and fit local ridge regressors
        print("[*] Initializing LIME Tabular Explainer...")
        self.lime_explainer = lime.lime_tabular.LimeTabularExplainer(
            training_data=np.array(self.X_train),
            feature_names=self.feature_names,
            class_names=['Approved / Paid', 'Default Risk'],
            mode='classification',
            discretize_continuous=True,
            random_state=42
        )

    # ==========================
    # SHAP EXPLANATIONS
    # ==========================
    def compute_shap_values(self, X_sample: pd.DataFrame):
        """Computes SHAP Explanation object and raw shap values."""
        shap_values = self.shap_explainer(X_sample)
        return shap_values

    def save_shap_summary_plot(self, shap_values, output_path: str):
        """Generates and saves the beeswarm summary plot showing directionality."""
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, show=False)
        plt.title("SHAP Global Feature Impact on Loan Default Risk", fontsize=14, pad=15)
        plt.tight_layout()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[+] Saved SHAP summary plot: {output_path}")

    def save_shap_waterfall_plot(self, shap_values_single, output_path: str, max_display: int = 10):
        """Generates and saves a local waterfall plot for a specific applicant."""
        plt.figure(figsize=(9, 6))
        shap.plots.waterfall(shap_values_single, max_display=max_display, show=False)
        plt.title("SHAP Local Attribution for Applicant", fontsize=13, pad=15)
        plt.tight_layout()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[+] Saved SHAP waterfall plot: {output_path}")

    def get_applicant_shap_contributions(self, shap_values_single, top_n: int = 5):
        """Extracts top positive (risk-increasing) and negative (risk-decreasing) features."""
        values = shap_values_single.values
        feature_names = np.array(self.feature_names)
        
        # DataFrame of contributions
        df = pd.DataFrame({
            'Feature': feature_names,
            'SHAP_Value': values,
            'Feature_Value': shap_values_single.data
        })
        
        # Sort by absolute impact
        df['Abs_Impact'] = df['SHAP_Value'].abs()
        df = df.sort_values(by='Abs_Impact', ascending=False)
        
        risk_increasing = df[df['SHAP_Value'] > 0].head(top_n)
        risk_decreasing = df[df['SHAP_Value'] < 0].head(top_n)
        
        return df, risk_increasing, risk_decreasing

    # ==========================
    # LIME EXPLANATIONS
    # ==========================
    def explain_instance_lime(self, instance_array: np.ndarray, num_features: int = 8):
        """Generates LIME explanation for a single applicant instance."""
        exp = self.lime_explainer.explain_instance(
            data_row=instance_array,
            predict_fn=self.model.predict_proba,
            num_features=num_features,
            labels=[1]  # Explain default class
        )
        return exp

    def save_lime_plot(self, lime_exp, output_path: str):
        """Saves LIME explanation as a horizontal bar chart."""
        fig = lime_exp.as_pyplot_figure(label=1)
        plt.title("LIME Local Feature Contributions (Default Risk Class)", fontsize=12)
        plt.tight_layout()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"[+] Saved LIME plot: {output_path}")

    def get_lime_as_dataframe(self, lime_exp) -> pd.DataFrame:
        """Parses LIME list of (rule, weight) into a clean DataFrame."""
        exp_list = lime_exp.as_list(label=1)
        df_lime = pd.DataFrame(exp_list, columns=['Condition_Rule', 'LIME_Weight'])
        df_lime['Impact'] = df_lime['LIME_Weight'].apply(
            lambda w: 'Increases Default Risk' if w > 0 else 'Reduces Default Risk'
        )
        return df_lime
