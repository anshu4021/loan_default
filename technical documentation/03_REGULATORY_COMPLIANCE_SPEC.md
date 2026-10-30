# ⚖️ Technical Documentation 03: Regulatory Compliance Specification

This document details the regulatory compliance architecture, statutory mapping, and automated legal notice generation conforming to federal banking guidelines.

---

## 1. Statutory Mandates in Automated Credit Underwriting

```
                         Federal Regulatory Framework
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
   ECOA Reg B                      FCRA                        CFPB 2022-03
(12 CFR § 1002.9)           (15 U.S.C. § 1681)             Regulatory Circular
• Adverse Action Notices    • Credit agency accuracy       • Prohibits black-box
• Top-4 specific reasons    • Disclosure of score factors    excuses for denial
• No disparate impact       • Consumer dispute rights      • Demands auditable XAI
```

### Key Federal Requirements:
1. **ECOA Regulation B (12 CFR § 1002.9)**:
   - When a creditor takes an adverse action (denial or unfavorable terms), they must deliver a written Statement of Adverse Action within 30 days.
   - The statement must disclose the **principal reasons** (typically 4) for the adverse decision.
2. **CFPB Circular 2022-03 ("Adverse Action Notification Requirements in Connection with Credit Decisions Based on Complex Algorithms")**:
   - Explicitly establishes that creditors cannot avoid explaining decisions by claiming that the algorithmic technology is too complicated.
   - If a lender uses complex machine learning models, they must maintain an explainability mechanism capable of generating specific, legally compliant denial reasons.

---

## 2. Standardized CFPB Reason Code Mapping Dictionary

Our `AdverseActionGenerator` extracts the top positive contributors from the applicant's local SHAP waterfall attribution and matches them against standardized Consumer Financial Protection Bureau (CFPB) reason statements:

| Internal Feature | CFPB Legal Reason Code Statement | Actionable Counterfactual Recourse |
| :--- | :--- | :--- |
| `loan_percent_income` | High loan amount relative to verifiable annual income | Reduce requested principal to lower exposure below 25%. |
| `debt_to_income` (DTI) | Excessive total monthly debt obligations relative to income | Pay down revolving debt to bring DTI below 30%. |
| `credit_score` | Credit score does not meet minimum credit tier guidelines | Maintain 6+ months of on-time payments to rebuild score. |
| `cb_person_default_on_file` | Adverse public records or prior delinquency on bureau file | Resolve delinquent collections remarks with reporting bureaus. |
| `loan_int_rate` | High borrowing cost tier assigned based on credit profile | Improve credit profile to qualify for lower interest tier. |
| `loan_grade_num` | Assigned underwriting risk rating exceeds risk tolerance | Reapply with a creditworthy co-signer or lower loan facility. |
| `person_emp_length` | Length of current employment tenure does not meet criteria | Maintain continuous employment with current employer. |
| `person_income` | Insufficient gross annual income for requested facility | Apply for lower principal or include supplemental verified income. |

---

## 3. Disparate Impact & Fair Lending Auditing

Under the Fair Housing Act and ECOA, lenders must ensure that credit algorithms do not produce an unlawful **Disparate Impact** against protected demographic groups (race, sex, marital status, age).

### The Four-Fifths (80%) Rule Formula:
$$\text{Adverse Impact Ratio (AIR)} = \frac{\text{Selection Rate}_{\text{protected}}}{\text{Selection Rate}_{\text{unprotected}}} \ge 0.80$$

Our system audits demographic proxies using SHAP dependence plots to ensure no indirect proxy discrimination exists across age or socioeconomic segments.
