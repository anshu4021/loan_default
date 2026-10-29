"""
Data Preprocessing & Feature Engineering Pipeline
Handles data ingestion, feature transformation, encoding, and train-test splits
optimized for explainability (SHAP & LIME compatibility).
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Ordinal mapping for risk tiers
GRADE_MAPPING = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}

class CreditDataPipeline:
    def __init__(self, target_col: str = 'loan_status', test_size: float = 0.2, random_state: int = 42):
        self.target_col = target_col
        self.test_size = test_size
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.feature_names = None
        self.categorical_cols = ['person_home_ownership', 'loan_intent']
        self.numerical_cols = [
            'person_age', 'person_income', 'person_emp_length',
            'loan_amnt', 'loan_int_rate', 'loan_percent_income',
            'debt_to_income', 'credit_score', 'cb_person_cred_hist_length',
            'loan_grade_num', 'cb_person_default_on_file_num'
        ]

    def fit_transform(self, df: pd.DataFrame):
        df_processed = df.copy()

        # Handle missing values if any
        for col in df_processed.select_dtypes(include=[np.number]).columns:
            df_processed[col] = df_processed[col].fillna(df_processed[col].median())
        for col in df_processed.select_dtypes(include=['object']).columns:
            df_processed[col] = df_processed[col].fillna(df_processed[col].mode()[0])

        # Feature transformations
        df_processed['loan_grade_num'] = df_processed['loan_grade'].map(GRADE_MAPPING).fillna(3).astype(int)
        df_processed['cb_person_default_on_file_num'] = (df_processed['cb_person_default_on_file'] == 'Y').astype(int)

        # Drop original raw categorical columns that were converted
        df_processed = df_processed.drop(columns=['loan_grade', 'cb_person_default_on_file'])

        # One-hot encoding for nominal categories with clean prefixes
        df_encoded = pd.get_dummies(df_processed, columns=self.categorical_cols, drop_first=False, dtype=int)

        # Separate target
        y = df_encoded[self.target_col].values
        X = df_encoded.drop(columns=[self.target_col])
        self.feature_names = list(X.columns)

        # Stratified Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )

        return X_train, X_test, y_train, y_test, self.feature_names

    def transform_single_applicant(self, applicant_dict: dict) -> pd.DataFrame:
        """Transforms a single applicant dictionary into model-ready DataFrame."""
        df_single = pd.DataFrame([applicant_dict])
        
        # Apply mappings
        df_single['loan_grade_num'] = df_single['loan_grade'].map(GRADE_MAPPING).fillna(3).astype(int)
        df_single['cb_person_default_on_file_num'] = 1 if applicant_dict.get('cb_person_default_on_file') == 'Y' else 0
        df_single = df_single.drop(columns=['loan_grade', 'cb_person_default_on_file'], errors='ignore')
        
        # One-hot encode
        df_encoded = pd.get_dummies(df_single, columns=self.categorical_cols, drop_first=False, dtype=int)
        
        # Align with known training columns
        aligned_df = pd.DataFrame(0, index=[0], columns=self.feature_names)
        for col in df_encoded.columns:
            if col in aligned_df.columns:
                aligned_df[col] = df_encoded[col]
        return aligned_df

def save_pipeline(pipeline: CreditDataPipeline, filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(pipeline, filepath)
    print(f"[+] Pipeline saved to: {filepath}")

def load_pipeline(filepath: str) -> CreditDataPipeline:
    return joblib.load(filepath)
