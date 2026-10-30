"""
Lightweight REST API Prototype
Exposes REST endpoints for credit default scoring, SHAP explanations,
and ECOA Adverse Action Notice generation using Python standard http server.
Can run standalone without third-party web frameworks.
"""

import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import numpy as np
import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from src.preprocessing import load_pipeline
from src.model_trainer import load_trained_model
from src.explainers import LoanXAIExplainer
from src.compliance import AdverseActionGenerator

# Load system artifacts once at startup
print("[*] Initializing API Prototype Artifacts...")
models_dir = os.path.join(base_dir, 'models')
pipeline = load_pipeline(os.path.join(models_dir, 'pipeline.joblib'))
model = load_trained_model(os.path.join(models_dir, 'champion_xgboost.joblib'))
dataset_path = os.path.join(base_dir, 'dataset', 'loan_data_100k.csv')
df_sample = pd.read_csv(dataset_path).head(200)
X_sample, _, _, _, _ = pipeline.fit_transform(df_sample)
explainer = LoanXAIExplainer(model, X_sample, pipeline.feature_names)
compliance = AdverseActionGenerator(approval_threshold=0.35)
print("[+] API Prototype Ready.")

class CreditRiskAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    def do_OPTIONS(self):
        self._send_json(200, {"status": "ok"})

    def do_GET(self):
        if self.path == '/' or self.path == '/health':
            self._send_json(200, {
                "status": "healthy",
                "service": "Explainable AI Credit Risk API Prototype",
                "version": "2.0.0",
                "model": "XGBoost Classifier",
                "policy_cutoff": 0.35
            })
        elif self.path == '/sample-applicants':
            samples_path = os.path.join(os.path.dirname(__file__), 'sample_applicants.json')
            with open(samples_path, 'r') as f:
                samples = json.load(f)
            self._send_json(200, samples)
        else:
            self._send_json(404, {"error": "Endpoint not found"})

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            payload = json.loads(body.decode('utf-8'))
        except Exception as e:
            self._send_json(400, {"error": f"Invalid JSON payload: {str(e)}"})
            return

        applicant_data = payload.get('applicant', payload)
        applicant_id = payload.get('applicant_id', 'APP-REST-API')
        
        try:
            df_trans = pipeline.transform_single_applicant(applicant_data)
            prob_default = float(model.predict_proba(df_trans)[0, 1])
            is_denied = prob_default >= 0.35
            decision = "DENIED" if is_denied else "APPROVED"
        except Exception as e:
            self._send_json(422, {"error": f"Error during model scoring: {str(e)}"})
            return

        if self.path == '/predict':
            self._send_json(200, {
                "applicant_id": applicant_id,
                "decision": decision,
                "default_probability": round(prob_default, 4),
                "default_probability_pct": round(prob_default * 100, 2),
                "approval_threshold_pct": 35.0,
                "risk_tier": "High Risk" if is_denied else "Prime Quality"
            })
        elif self.path == '/explain' or self.path == '/explain/shap':
            shap_res = explainer.shap_explainer(df_trans)[0]
            attr_df, risk_up, risk_down = explainer.get_applicant_shap_contributions(shap_res)
            
            top_drivers = []
            for _, r in attr_df.head(6).iterrows():
                top_drivers.append({
                    "feature": r['Feature'],
                    "value": r['Feature_Value'],
                    "shap_impact": round(float(r['SHAP_Value']), 4),
                    "direction": "Increases Risk" if r['SHAP_Value'] > 0 else "Decreases Risk"
                })
                
            self._send_json(200, {
                "applicant_id": applicant_id,
                "decision": decision,
                "default_probability_pct": round(prob_default * 100, 2),
                "top_shap_drivers": top_drivers
            })
        elif self.path == '/adverse-action':
            shap_res = explainer.shap_explainer(df_trans)[0]
            attr_df, _, _ = explainer.get_applicant_shap_contributions(shap_res)
            notice = compliance.generate_notice(applicant_id, prob_default, attr_df)
            self._send_json(200, notice)
        else:
            self._send_json(404, {"error": "Endpoint not found"})

def run_api(port=8080):
    server = HTTPServer(('127.0.0.1', port), CreditRiskAPIHandler)
    print(f"[+] API Prototype listening on http://127.0.0.1:{port}")
    print(f"    Health check: http://127.0.0.1:{port}/health")
    print(f"    Sample cases: http://127.0.0.1:{port}/sample-applicants")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping API server...")
        server.server_close()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_api(port)
