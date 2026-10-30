# 📚 Enterprise Technical Documentation Index

Welcome to the comprehensive technical documentation repository for the **Explainable AI for Loan Default Prediction Using SHAP & LIME** capstone project.

---

## 📑 Documentation Structure & Index

| Module | Title | Primary Audience | Key Topics Covered |
| :---: | :--- | :---: | :--- |
| **01** | [**System Architecture & Data Flow**](01_SYSTEM_ARCHITECTURE.md) | Architects & Engineers | Architecture diagrams, component interactions, container topology, and pipeline flow. |
| **02** | [**Mathematical Foundations**](02_MATHEMATICAL_FOUNDATIONS.md) | Data Scientists & Quants | Shapley value derivations, proofs of the 4 axioms, TreeSHAP $\mathcal{O}(TLD^2)$ dynamic programming, and LIME loss optimization. |
| **03** | [**Regulatory Compliance Spec**](03_REGULATORY_COMPLIANCE_SPEC.md) | Compliance & Legal | ECOA Regulation B (12 CFR § 1002.9), FCRA, CFPB Circular 2022-03, CFPB reason code dictionary, and disparate impact auditing. |
| **04** | [**REST API Specification**](04_API_SPECIFICATION.md) | Backend Developers | OpenAPI schema, JSON request/response formats, error codes, and curl examples for `/predict`, `/explain`, and `/adverse-action`. |
| **05** | [**Data Dictionary & Feature Schema**](05_DATA_DICTIONARY_AND_SCHEMA.md) | Data Analysts | Complete dictionary of 14 raw and 21 engineered features, statistics, distributions, and preprocessing transforms. |
| **06** | [**Model Risk Management (SR 11-7)**](06_MODEL_RISK_MANAGEMENT_SR11_7.md) | Risk Officers | Federal Reserve SR 11-7 compliance, 3-pillar governance, Population Stability Index (PSI), and drift surveillance protocols. |
| **07** | [**Underwriter & User Manual**](07_USER_AND_UNDERWRITER_MANUAL.md) | Loan Officers | Operator handbook for Streamlit UI, interpreting SHAP waterfalls, handling borderline cases, and exporting Adverse Action notices. |
