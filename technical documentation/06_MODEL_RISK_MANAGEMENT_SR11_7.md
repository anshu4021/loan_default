# 🛡️ Technical Documentation 06: Model Risk Management (Federal Reserve SR 11-7 / OCC 2011-12)

This document formalizes the Model Risk Management (MRM) procedures, model governance framework, and ongoing surveillance protocols mandated by the Federal Reserve and OCC.

---

## 🏛️ The Three Pillars of SR 11-7 Compliance

```
                       Federal Reserve SR 11-7 Guidance
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
Pillar 1: Development          Pillar 2: Validation           Pillar 3: Surveillance
• Sound conceptual design      • Independent benchmarking     • Ongoing drift tracking
• Data lineage & leakage audit • Sensitivity & stress testing • Explainability stability
• Linear baseline comparison   • Boundary condition tests     • Model retirement triggers
```

---

## 🔍 Model Surveillance & Drift Detection Protocols

To prevent silent model degradation in production, our surveillance engine tracks three tiers of drift:

### 1. Data Drift (Covariate Shift) — Population Stability Index (PSI)
$$PSI = \sum_{b=1}^B \left( \% \text{Actual}_b - \% \text{Expected}_b \right) \times \ln\left( \frac{\% \text{Actual}_b}{\% \text{Expected}_b} \right)$$
- **PSI < 0.10**: No significant shift; normal operation.
- **0.10 $\le$ PSI < 0.25**: Moderate drift; flag for review.
- **PSI $\ge$ 0.25**: Significant population shift; mandatory retraining trigger.

### 2. Concept Drift (Performance Decay)
- Monitored on mature 90-day delinquent loan cohorts using quarterly **Brier Score calibration curves** and **PR-AUC**.
- An increase in Brier score $> 0.03$ triggers underwriting parameter recalibration.

### 3. Explainability Drift (XAI Invariance)
- Tracks the mean absolute SHAP attribution values across monthly cohorts.
- Detects if macroeconomic events (e.g., federal interest rate hikes) cause certain features to disproportionately dominate underwriting decisions before actual credit charge-offs occur.
