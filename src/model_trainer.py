"""
Model Training & Evaluation Module
Trains Logistic Regression (Baseline), Random Forest, and XGBoost Classifier.
Evaluates with ROC-AUC, PR-AUC, F1-score, Brier score (Calibration), and Financial Cost Matrix.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score, average_precision_score, classification_report,
    confusion_matrix, brier_score_loss, f1_score
)
from xgboost import XGBClassifier

class LoanRiskModelTrainer:
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.models = {}
        self.metrics = {}

    def train_all(self, X_train, y_train, X_test, y_test):
        scale_pos_weight = (len(y_train) - sum(y_train)) / sum(y_train)

        # 1. Baseline: Logistic Regression
        lr = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=self.random_state)
        lr.fit(X_train, y_train)
        self.models['Logistic Regression'] = lr

        # 2. Random Forest
        rf = RandomForestClassifier(
            n_estimators=150, max_depth=10, class_weight='balanced',
            random_state=self.random_state, n_jobs=-1
        )
        rf.fit(X_train, y_train)
        self.models['Random Forest'] = rf

        # 3. XGBoost Classifier (Champion Model)
        xgb = XGBClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=scale_pos_weight,
            eval_metric='logloss',
            random_state=self.random_state
        )
        xgb.fit(X_train, y_train)
        self.models['XGBoost'] = xgb

        # Evaluate all models
        summary_records = []
        for name, model in self.models.items():
            preds = model.predict(X_test)
            probs = model.predict_proba(X_test)[:, 1]

            roc_auc = roc_auc_score(y_test, probs)
            pr_auc = average_precision_score(y_test, probs)
            f1 = f1_score(y_test, preds)
            brier = brier_score_loss(y_test, probs)

            # Cost-Sensitive Loss Calculation:
            # FN Cost (approving loan that defaults) = 5 * average loan loss
            # FP Cost (rejecting good borrower) = 1 * lost interest margin
            tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()
            total_cost = (fn * 5) + (fp * 1)

            self.metrics[name] = {
                'ROC-AUC': roc_auc,
                'PR-AUC': pr_auc,
                'F1-Score': f1,
                'Brier-Score': brier,
                'Financial-Cost': total_cost,
                'Confusion-Matrix': (tn, fp, fn, tp)
            }

            summary_records.append({
                'Model': name,
                'ROC-AUC': round(roc_auc, 4),
                'PR-AUC': round(pr_auc, 4),
                'F1-Score': round(f1, 4),
                'Brier Score (Calibration)': round(brier, 4),
                'Estimated Risk Cost': total_cost
            })

        summary_df = pd.DataFrame(summary_records)
        return summary_df

    def save_best_model(self, filepath: str, model_name: str = 'XGBoost'):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.models[model_name], filepath)
        print(f"[+] Champion model ({model_name}) saved to {filepath}")

def load_trained_model(filepath: str):
    return joblib.load(filepath)
