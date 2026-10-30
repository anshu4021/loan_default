# 📘 Technical Documentation 07: Credit Underwriter & User Operator Manual

This user manual guides loan officers, risk analysts, and compliance auditors through operating the Explainable AI Underwriting platform.

---

## 🚦 Step-by-Step Underwriting Workflow

```
[Step 1: Input Application] ──► [Step 2: Automated Scoring] ──► [Step 3: XAI Inspection] ──► [Step 4: Notice Generation]
(Sliders / API Payload)        (PD Gauge vs 35% Cutoff)        (SHAP Waterfall & LIME)     (Approve or Deny with Recourse)
```

### 1. Navigating the Streamlit Dashboard
- **Sidebar**: Enter the applicant's demographics, credit bureau FICO score, income, requested principal, and loan purpose.
- **Tab 1 (Underwriting Decision)**: Displays the real-time default probability gauge, approval badge, and policy safety threshold comparison.
- **Tab 2 (SHAP Waterfall)**: Visualizes the exact positive and negative attributions shifting the customer from the population average to their individual score.
- **Tab 3 (LIME Rules)**: Breaks down the decision into human-readable rules (e.g., `loan_percent_income > 0.40`).
- **Tab 4 (ECOA Notice)**: For rejected applicants, review the top-4 CFPB reason codes and download the formal Adverse Action Notice.

---

## ❓ Frequently Asked Operator Questions

1. **What if the applicant is borderline (e.g., 34% default probability)?**
   - The underwriter should inspect the local SHAP waterfall in Tab 2. If the risk is driven by non-recurring factors (e.g., medical purpose), a secondary manual underwriter review can be requested.
2. **Can an underwriter override a model denial?**
   - Under banking compliance rules, overrides must be documented with an auditable justification log and submitted to the Model Risk Management committee.
3. **How does the system ensure an applicant knows how to re-qualify?**
   - The system automatically outputs **Actionable Recourse** statements in the Adverse Action Notice, telling the consumer the exact numerical thresholds needed on mutable factors (e.g., reducing loan principal by \$6,000) to cross into approval territory.
