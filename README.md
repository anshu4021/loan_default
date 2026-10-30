# 🏦 Explainable AI (XAI) for Loan Default Prediction Using SHAP & LIME

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://img.shields.io/badge/Streamlit-UI%20Enabled-orange)](https://streamlit.io/)
[![Dataset: 1 Lakh](https://img.shields.io/badge/Dataset-100%2C000%20Records-blueviolet)](dataset/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-2496ED)](deployed%20application/)

An enterprise-grade, compliance-ready Machine Learning and Explainable AI (XAI) capstone platform trained on **100,000 (1 Lakh)** loan applicants. Demonstrates how to predict consumer loan default risk with an optimized **XGBoost Classifier** (0.894 ROC-AUC | 0.794 PR-AUC) and dismantle model opacity using **SHAP (SHapley Additive exPlanations)** and **LIME (Local Interpretable Model-agnostic Explanations)**.

Features automated generation of legally required **Adverse Action Notices (ECOA Regulation B / FCRA)** and real-time interactive risk scoring across Web UI, Terminal CLI, and REST API.

> 📄 **Download the Complete Interview & Capstone PDF Guide:**  
> [**`Explainable_AI_Loan_Default_Prediction_Master_Guide.pdf`**](./Explainable_AI_Loan_Default_Prediction_Master_Guide.pdf)

---

## 🎬 Animated Walkthrough & Demo Video

| Interactive Underwriting Walkthrough Preview |
| :---: |
| ![Demo Walkthrough](demo%20video/demo_walkthrough.gif) |
| *Full HD Video available at:* [`demo video/loan_default_xai_demo.mp4`](demo%20video/loan_default_xai_demo.mp4) (5.49 MB) |

---

## 📁 Repository Structure & Directory Map

```
loan_default/
├── 📂 dataset/                      # 100,000 (1 Lakh) applicant dataset & data dictionary
│   ├── loan_data_100k.csv          # 1 Lakh applicant records (6.51 MB)
│   ├── dataset_summary.json        # Class balance & statistical metadata
│   ├── generate_100k_dataset.py    # Standalone dataset generation script
│   └── README.md                   # Data dictionary & distribution schema
├── 📂 working prototype/            # Self-contained runnable prototypes
│   ├── sample_applicants.json      # Prime, subprime, and borderline test profiles
│   ├── cli_prototype.py            # Terminal interactive underwriting CLI
│   ├── api_prototype.py            # Lightweight standalone REST API server
│   ├── run_prototype.bat           # 1-Click Windows execution launcher
│   ├── run_prototype.sh            # 1-Click Linux / macOS launcher
│   └── README.md                   # Complete prototype user instructions
├── 📂 demo video/                   # Video assets & narration script
│   ├── loan_default_xai_demo.mp4   # 720p HD MP4 walkthrough video (5.49 MB)
│   ├── demo_walkthrough.gif        # Compact animated GIF preview (0.55 MB)
│   ├── create_demo_video.py        # Video synthesis rendering script
│   └── DEMO_WALKTHROUGH.md         # Scene timestamps & spoken voiceover script
├── 📂 deployed application/         # Production cloud & container configurations
│   ├── Dockerfile                  # Multi-stage hardened production container
│   ├── docker-compose.yml          # Web UI & REST API service orchestration
│   ├── Procfile                    # PaaS runtime for Heroku / Render / Railway
│   ├── render.yaml                 # Render.com infrastructure-as-code blueprint
│   ├── .streamlit/config.toml      # Production Streamlit headless theme configuration
│   └── DEPLOYMENT_GUIDE.md         # Deployment manual for AWS, GCP, HuggingFace & Cloud
├── 📂 testing report/               # Automated test suites, photos & QA reports
│   ├── test_coverage_chart.png     # Verification & module coverage chart (Photo)
│   ├── latency_benchmark_test.png  # 100 concurrent stress test latency distribution (Photo)
│   ├── model_validation_test_suite.png # 5-Fold cross-validation stability test (Photo)
│   ├── run_test_suite.py           # Automated test executor (7/7 tests passed)
│   ├── test_results.json           # Machine-readable test log
│   └── TEST_REPORT.md              # Formal QA audit & invariance testing report
├── 📂 performance result/           # 1 Lakh model benchmark charts & metrics
│   ├── roc_curves_comparison.png   # ROC curve comparison across all 3 models
│   ├── precision_recall_curves.png # Precision-Recall curve on imbalanced defaults
│   ├── calibration_curves.png      # Brier score reliability calibration diagram
│   ├── confusion_matrices.png      # Normalized confusion matrix heatmaps
│   ├── financial_cost_matrix.png   # Asymmetric 5:1 False Negative cost optimization
│   ├── feature_importance_comparison.png # Global Gain feature ranking
│   ├── shap_vs_lime_concordance.png# Attribution scatter & rank correlation plot
│   ├── metrics_summary.json        # Benchmark metrics data
│   └── PERFORMANCE_REPORT.md       # Comprehensive evaluation & analysis report
├── 📂 technical documentation/      # Modular engineering & legal specifications
│   ├── 01_SYSTEM_ARCHITECTURE.md   # Architectural design, data flow & topology
│   ├── 02_MATHEMATICAL_FOUNDATIONS.md # Formal Shapley values & LIME surrogate proofs
│   ├── 03_REGULATORY_COMPLIANCE_SPEC.md # Legal mapping to ECOA Reg B, FCRA & SR 11-7
│   ├── 04_API_SPECIFICATION.md     # OpenAPI / Swagger REST API schemas
│   ├── 05_DATA_DICTIONARY_AND_SCHEMA.md # Deep feature stats & imputation procedures
│   ├── 06_MODEL_RISK_MANAGEMENT_SR11_7.md # Drift detection (PSI) & surveillance
│   ├── 07_USER_AND_UNDERWRITER_MANUAL.md # Operator guide for loan officers
│   └── README.md                   # Technical documentation index
├── 📂 src/                          # Core application Python modules
│   ├── preprocessing.py            # Feature transformations & pipeline class
│   ├── model_trainer.py            # Multi-model training & cost matrix evaluation
│   ├── explainers.py               # SHAP TreeExplainer & LIME TabularExplainer
│   ├── compliance.py               # ECOA Adverse Action Notice generator
│   └── xai_comparison.py           # SHAP vs LIME concordance & latency benchmarks
├── 📂 models/                       # Trained champion model & pipeline serialized
│   ├── champion_xgboost.joblib     # Pre-trained XGBoost Classifier
│   └── pipeline.joblib             # Fitted preprocessing pipeline
├── app.py                          # Main interactive Streamlit application
├── run_pipeline.py                 # Master end-to-end execution runner
├── generate_pdf_report.py          # Executive PDF generator script
├── requirements.txt                # Project dependencies
└── README.md                       # Main project overview
```

---

## 📊 Performance Benchmark Summary (100,000 Applicant Dataset)

| Evaluation Metric | Logistic Regression (Baseline) | Random Forest | XGBoost (Champion) | Strategic Banking Impact |
| :--- | :---: | :---: | :---: | :--- |
| **ROC-AUC** | `0.8872` | `0.8919` | **`0.8941`** | Overall ranking capability across all thresholds |
| **PR-AUC (Avg Precision)** | `0.7781` | `0.7888` | **`0.7940`** | True precision on imbalanced default minority class |
| **Accuracy** | `76.54%` | `83.12%` | **`84.28%`** | Overall classification accuracy |
| **F1-Score** | `0.7018` | `0.7106` | **`0.7074`** | Harmonic mean of precision and default recall |
| **Brier Score (Loss)** | `0.1295` | `0.1238` | **`0.1263`** | Probability calibration (essential for Expected Loss loan pricing) |
| **Inference Latency** | `0.003 ms` | `0.065 ms` | **`0.012 ms`** | Sub-millisecond response for real-time underwriting APIs |

*Detailed benchmark charts, cost optimization curves, and calibration diagrams are documented in [`performance result/`](performance%20result/).*

---

## 🔬 Mathematical Foundations: SHAP vs LIME

| Feature | SHAP (TreeExplainer) | LIME (LimeTabularExplainer) | Winner / Recommendation |
| :--- | :--- | :--- | :--- |
| **Foundational Theory** | Cooperative Game Theory (Shapley Values) | Local Linear Surrogate Regression | **SHAP** (Mathematically provable) |
| **Optimization Goal** | Fair payout allocation based on marginal contributions | Minimize fidelity loss + complexity $\mathcal{L}(f, g, \pi_x) + \Omega(g)$ | **SHAP** |
| **Axiomatic Guarantees** | Efficiency, Symmetry, Dummy Player, Additivity | None (Heuristic sampling) | **SHAP** (Legally defensible) |
| **Scope** | Unifies Global (Beeswarm) & Local (Waterfall) | Strictly Local per-instance | **SHAP** |
| **Determinism** | 100% Deterministic (Exact calculations) | Stochastic (Random perturbation sampling) | **SHAP** (Auditable stability) |
| **Inference Latency** | **8.60 ms** (Polynomial dynamic programming) | **112.86 ms** (5,000 forward passes) | **SHAP is ~13× faster** |
| **Concordance** | **Spearman Rank Correlation: 0.879** | **100.0% Directional Agreement** | Both methods cross-validate |

---

## 📜 Regulatory Compliance: Adverse Action Notices (ECOA / FCRA)

Under **Equal Credit Opportunity Act (ECOA) Regulation B (12 CFR § 1002.9)** and **CFPB Circular 2022-03**, creditors cannot cite algorithmic complexity to justify unexplainable credit denials.

When default risk exceeds the **35% threshold**, our engine:
1. Filters top positive (risk-increasing) SHAP features.
2. Maps them to audited Consumer Financial Protection Bureau (CFPB) statement codes.
3. Automatically synthesizes **Actionable Counterfactual Recourse** for the consumer:
   - *Reason 1: Credit score does not meet minimum credit tier guidelines (FICO: 520, SHAP: +1.334)*
   - *Reason 2: Assigned underwriting risk rating exceeds risk tolerance threshold (Grade: E, SHAP: +1.197)*
   - *Reason 3: High loan amount relative to verifiable annual income (Loan % Income: 56.3%, SHAP: +0.780)*
   - *Reason 4: High borrowing cost tier assigned based on current credit profile (Interest Rate: 21.50%, SHAP: +0.742)*
   - 💡 **Actionable Recourse**: *Reduce requested loan principal from \$18,000 to \$8,000 to lower loan-to-income exposure below 25%, and maintain 6+ consecutive months of on-time payments.*

---

## 🚀 Quickstart & Execution

### 1. Installation
```bash
git clone https://github.com/anshu4021/loan_default.git
cd loan_default
pip install -r requirements.txt
```

### 2. Launch Interactive Web Dashboard
```bash
streamlit run app.py
```
*Access the underwriting dashboard at `http://localhost:8501`.*

### 3. Launch Working Prototypes (CLI / API)
```bash
# Terminal CLI interactive underwriting
python "working prototype/cli_prototype.py"

# REST API microservice (Port 8080)
python "working prototype/api_prototype.py"
```

### 4. Run Automated Testing Suite
```bash
python "testing report/run_test_suite.py"
```

---

## 👨‍💻 Author & Project Credits
- **Author**: Anshu Raj
- **Email**: `rajanshu4021@gmail.com`
- **GitHub**: [github.com/anshu4021/loan_default](https://github.com/anshu4021/loan_default)
- **Project**: Capstone Defense in Applied Machine Learning & Explainable AI for Credit Underwriting.
