"""
SHAP vs LIME Comparative Benchmarking Module
Measures:
1. Feature Attribution Consistency (Spearman Rank Correlation between SHAP and LIME)
2. Computational Efficiency (Inference Latency per explanation)
3. Mathematical Paradigm Differences (Game Theoretic Axioms vs Local Surrogate Perturbation)
"""

import time
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

class XAIComparator:
    def __init__(self, explainer_engine):
        self.engine = explainer_engine

    def benchmark_single_applicant(self, applicant_series: pd.Series, applicant_array: np.ndarray):
        """Runs side-by-side SHAP and LIME explanations, benchmarking runtime and concordance."""
        # 1. SHAP Execution & Latency
        t0 = time.perf_counter()
        shap_single = self.engine.shap_explainer(pd.DataFrame([applicant_series]))[0]
        shap_time = (time.perf_counter() - t0) * 1000  # ms
        
        shap_df, _, _ = self.engine.get_applicant_shap_contributions(shap_single)
        
        # 2. LIME Execution & Latency
        t0 = time.perf_counter()
        lime_exp = self.engine.explain_instance_lime(applicant_array, num_features=10)
        lime_time = (time.perf_counter() - t0) * 1000  # ms
        
        lime_df = self.engine.get_lime_as_dataframe(lime_exp)
        
        # 3. Match LIME features back to standard feature names to calculate rank correlation
        lime_features_extracted = []
        lime_weights = []
        for rule, weight in lime_exp.as_list(label=1):
            for orig_col in self.engine.feature_names:
                if orig_col in rule:
                    lime_features_extracted.append(orig_col)
                    lime_weights.append(weight)
                    break
        
        comparison_records = []
        for feat, l_weight in zip(lime_features_extracted, lime_weights):
            s_val = shap_df[shap_df['Feature'] == feat]['SHAP_Value'].values
            s_val = s_val[0] if len(s_val) > 0 else 0.0
            comparison_records.append({
                'Feature': feat,
                'SHAP_Value': round(s_val, 4),
                'LIME_Weight': round(l_weight, 4),
                'Same_Direction': (s_val > 0 and l_weight > 0) or (s_val < 0 and l_weight < 0)
            })

        comp_df = pd.DataFrame(comparison_records)
        
        # Rank correlation if enough overlapping features
        if len(comp_df) >= 3:
            corr, p_val = spearmanr(comp_df['SHAP_Value'], comp_df['LIME_Weight'])
        else:
            corr, p_val = np.nan, np.nan

        summary = {
            'shap_latency_ms': round(shap_time, 2),
            'lime_latency_ms': round(lime_time, 2),
            'rank_correlation': round(corr, 3) if not np.isnan(corr) else 'N/A',
            'directional_concordance_pct': round((comp_df['Same_Direction'].mean() * 100), 1) if len(comp_df) > 0 else 100.0,
            'comparison_table': comp_df
        }
        
        return summary
