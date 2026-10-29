"""
End-to-End Master Execution Pipeline
Coordinates data generation, model training, evaluation, SHAP & LIME explanations,
comparative benchmarking, and regulatory adverse action generation.
"""

import os
import sys
import json
import numpy as np
import pandas as pd

# Add local directory to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from data.generate_dataset import generate_credit_data
from src.preprocessing import CreditDataPipeline, save_pipeline
from src.model_trainer import LoanRiskModelTrainer
from src.explainers import LoanXAIExplainer
from src.xai_comparison import XAIComparator
from src.compliance import AdverseActionGenerator

def main():
    print("="*75)
    print(" EXPLAINABLE AI (XAI) FOR LOAN DEFAULT PREDICTION (SHAP & LIME)")
    print(" Capstone Production Pipeline")
    print("="*75)

    data_dir = os.path.join(BASE_DIR, 'data')
    models_dir = os.path.join(BASE_DIR, 'models')
    reports_dir = os.path.join(BASE_DIR, 'reports')
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    csv_path = os.path.join(data_dir, 'loan_data.csv')

    # STEP 1: Dataset Generation / Loading
    if not os.path.exists(csv_path):
        print("\n[Step 1] Generating realistic credit risk dataset...")
        raw_df = generate_credit_data(num_samples=12000, random_state=42)
        raw_df.to_csv(csv_path, index=False)
    else:
        print(f"\n[Step 1] Loading existing dataset from {csv_path}...")
        raw_df = pd.read_csv(csv_path)

    print(f" Dataset Shape: {raw_df.shape}")
    print(f" Default Rate: {raw_df['loan_status'].mean()*100:.2f}%")

    # STEP 2: Preprocessing
    print("\n[Step 2] Feature Engineering & Pipeline Fit...")
    pipeline = CreditDataPipeline(target_col='loan_status', test_size=0.2, random_state=42)
    X_train, X_test, y_train, y_test, feature_names = pipeline.fit_transform(raw_df)
    save_pipeline(pipeline, os.path.join(models_dir, 'pipeline.joblib'))
    print(f" Training Samples: {len(X_train)} | Test Samples: {len(X_test)} | Features: {len(feature_names)}")

    # STEP 3: Model Training & Multi-Metric Evaluation
    print("\n[Step 3] Training ML Classifiers (Baseline LR, Random Forest, XGBoost)...")
    trainer = LoanRiskModelTrainer(random_state=42)
    metrics_df = trainer.train_all(X_train, y_train, X_test, y_test)
    print("\n" + metrics_df.to_string(index=False))
    
    # Save Champion Model
    champion_path = os.path.join(models_dir, 'champion_xgboost.joblib')
    trainer.save_best_model(champion_path, 'XGBoost')
    champion_model = trainer.models['XGBoost']

    # STEP 4: Explainable AI Engine (SHAP & LIME)
    print("\n[Step 4] Initializing XAI Engine...")
    explainer_engine = LoanXAIExplainer(champion_model, X_train, feature_names)

    # Global SHAP Explanation (using 500 test samples for fast & accurate estimation)
    print("\n[*] Generating Global SHAP Beeswarm Summary Plot...")
    X_sample_shap = X_test.iloc[:500]
    shap_values = explainer_engine.compute_shap_values(X_sample_shap)
    explainer_engine.save_shap_summary_plot(shap_values, os.path.join(reports_dir, 'shap_summary.png'))

    # Local Case Study: High-Risk Applicant
    print("\n[*] Generating Local Explanations for High-Risk Applicant Case Study...")
    test_probs = champion_model.predict_proba(X_test)[:, 1]
    high_risk_idx = np.where(test_probs > 0.70)[0][0]
    applicant_series = X_test.iloc[high_risk_idx]
    applicant_array = np.array(applicant_series)
    applicant_shap = explainer_engine.shap_explainer(pd.DataFrame([applicant_series]))[0]

    # Save local SHAP waterfall
    explainer_engine.save_shap_waterfall_plot(
        applicant_shap, os.path.join(reports_dir, 'shap_waterfall_example.png')
    )

    # Save local LIME explanation
    lime_exp = explainer_engine.explain_instance_lime(applicant_array, num_features=8)
    explainer_engine.save_lime_plot(
        lime_exp, os.path.join(reports_dir, 'lime_explanation_example.png')
    )

    # STEP 5: SHAP vs LIME Comparative Benchmarking
    print("\n[Step 5] Benchmarking SHAP vs LIME...")
    comparator = XAIComparator(explainer_engine)
    benchmark_res = comparator.benchmark_single_applicant(applicant_series, applicant_array)
    print(f" SHAP Latency: {benchmark_res['shap_latency_ms']} ms")
    print(f" LIME Latency: {benchmark_res['lime_latency_ms']} ms")
    print(f" Feature Rank Correlation: {benchmark_res['rank_correlation']}")
    print(f" Directional Concordance: {benchmark_res['directional_concordance_pct']}%")
    print("\nAttribution Concordance Table:")
    print(benchmark_res['comparison_table'].to_string(index=False))

    # STEP 6: Regulatory Adverse Action Notice Generator
    print("\n[Step 6] Generating Adverse Action Notice (ECOA / FCRA Compliant)...")
    aan_generator = AdverseActionGenerator(approval_threshold=0.35)
    shap_attr_df, _, _ = explainer_engine.get_applicant_shap_contributions(applicant_shap)
    notice = aan_generator.generate_notice(
        applicant_id=f"APP-TEST-{high_risk_idx}",
        default_prob=float(test_probs[high_risk_idx]),
        shap_contributions=shap_attr_df
    )
    print(json.dumps(notice, indent=2))

    # Save Pipeline Summary Report
    summary_report = {
        'model_metrics': metrics_df.to_dict(orient='records'),
        'benchmark_summary': {
            'shap_latency_ms': benchmark_res['shap_latency_ms'],
            'lime_latency_ms': benchmark_res['lime_latency_ms'],
            'rank_correlation': benchmark_res['rank_correlation'],
            'directional_concordance_pct': benchmark_res['directional_concordance_pct']
        },
        'sample_adverse_action_notice': notice
    }
    with open(os.path.join(reports_dir, 'pipeline_summary.json'), 'w') as f:
        json.dump(summary_report, f, indent=2)

    print("\n" + "="*75)
    print(" Pipeline execution complete! All artifacts and plots generated successfully.")
    print("="*75)

if __name__ == '__main__':
    main()
