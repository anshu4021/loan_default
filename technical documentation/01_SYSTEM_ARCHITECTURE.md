# 🏗️ Technical Documentation 01: System Architecture & Data Flow

This document outlines the high-level system architecture, component interactions, data pipeline flow, and container topology for the **Explainable AI for Loan Default Prediction** platform.

---

## 📌 System Architecture Diagram

```
[Loan Applicant / Credit Officer]
                 │ (Web UI / REST API / CLI)
                 ▼
 ┌─────────────────────────────────────────────────────────┐
 │                   API & Ingestion Layer                 │
 │  • Streamlit Web App (Port 8501)                        │
 │  • REST API Gateway (Port 8080)                         │
 │  • Terminal CLI Underwriting Tool                       │
 └──────────────────────────┬──────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────────┐
 │            Data Ingestion & Preprocessing               │
 │  • Median / Mode Imputation                             │
 │  • Ordinal Risk Encoding (Grade A=0 to F=5)             │
 │  • One-Hot Categorical Encoding                         │
 │  • Feature Alignment & Bounds Verification              │
 └──────────────────────────┬──────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────────┐
 │            Machine Learning Inference Engine            │
 │  • Champion XGBoost Classifier (200 Trees, Depth 5)     │
 │  • Class-Weight Scaling (scale_pos_weight = 2.72)       │
 │  • Calibrated Default Probability Output P(Default)     │
 └─────────────┬─────────────────────────────┬─────────────┘
               │ (Default Prob >= 0.35)      │ (All Applicants)
               ▼                             ▼
 ┌───────────────────────────┐  ┌───────────────────────────┐
 │      SHAP TreeExplainer   │  │    LIME Local Surrogate   │
 │ • Cooperative Game Theory │  │ • 5,000 Perturbations     │
 │ • Exact Shapley Values    │  │ • Distance Kernel Weight  │
 │ • 8.60 ms Latency         │  │ • Discrete Rules          │
 └─────────────┬─────────────┘  └─────────────┬─────────────┘
               │                              │
               └──────────────┬───────────────┘
                              │ (Attribution Vectors)
                              ▼
 ┌─────────────────────────────────────────────────────────┐
 │       Regulatory Adverse Action & Recourse Engine       │
 │  • Extract Top-4 Risk-Increasing Factors                │
 │  • Map to Standardized CFPB Reason Statements           │
 │  • Compute Actionable Counterfactual Remediation Paths  │
 │  • Generate ECOA Regulation B Compliance Notice         │
 └─────────────────────────────────────────────────────────┘
```

---

## 🧩 Core Architectural Components

### 1. Data Processing Engine (`src/preprocessing.py`)
- Standardizes incoming borrower payloads into model-ready vectors.
- Manages feature ordering, handles categorical mappings, and ensures no data leakage between training and inference partitions.

### 2. Model Training & Evaluation Suite (`src/model_trainer.py`)
- Houses training pipelines for Logistic Regression, Random Forest, and XGBoost.
- Implements an asymmetric loss matrix ($5\times$ False Negative cost penalty) reflecting unrecovered credit charge-offs vs. lost interest margin.

### 3. Explainable AI Engine (`src/explainers.py`)
- **SHAP Module**: Uses pre-compiled C++ TreeSHAP bindings to execute recursive tree traversals.
- **LIME Module**: Fits local ridge regressions on distance-weighted perturbations to generate condition rules.

### 4. Regulatory Compliance Module (`src/compliance.py`)
- Enforces statutory disclosure rules under **Equal Credit Opportunity Act (ECOA Regulation B)**.
- Maps raw feature coefficients to audited CFPB reason codes and synthesizes actionable counterfactual recommendations.

---

## 🐳 Container & Deployment Topology

- **Docker Image**: Multi-stage build on `python:3.11-slim` running under unprivileged user `appuser` (UID 1000).
- **Resource Footprint**: < 450 MB RAM, < 0.2 CPU cores per inference thread.
- **Liveness Probes**: Automated healthcheck probe at `/_stcore/health`.
