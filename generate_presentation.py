"""
Automated Professional PowerPoint Generator (16:9 Widescreen)
Generates an executive, publication-grade technical defense presentation
for 'Explainable AI for Loan Default Prediction Using SHAP and LIME'.
Includes 14 fully-styled slides, metric callout cards, comparison tables,
and embedded high-resolution performance and XAI visual plots.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# ========================================================
# PALETTE DEFINITION (Modern FinTech Executive Theme)
# ========================================================
BG_DARK = RGBColor(11, 17, 32)        # Deep Obsidian Navy #0B1120
CARD_BG = RGBColor(30, 41, 59)       # Slate 800 #1E293B
CARD_BORDER = RGBColor(51, 65, 85)   # Slate 700 #334155
TEAL_ACCENT = RGBColor(13, 148, 136) # Emerald Teal #0D9488
CYAN_ACCENT = RGBColor(56, 189, 248) # Sky Cyan #38BDF8
GOLD_ACCENT = RGBColor(245, 158, 11) # Amber Gold #F59E0B
RED_ACCENT = RGBColor(239, 68, 68)   # Crimson Red #EF4444
GREEN_ACCENT = RGBColor(34, 197, 94) # Emerald Green #22C55E
TEXT_LIGHT = RGBColor(248, 250, 252) # White Slate #F8FAFC
TEXT_MUTED = RGBColor(148, 163, 184) # Muted Slate #94A3B8

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_DARK

def add_header(slide, category: str, title: str, subtitle: str = None):
    # Category Pill
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(2.8), Inches(0.35))
    pill.fill.solid()
    pill.fill.fore_color.rgb = CARD_BG
    pill.line.color.rgb = TEAL_ACCENT
    pill.line.width = Pt(1)
    tf_pill = pill.text_frame
    tf_pill.word_wrap = True
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = category.upper()
    p_pill.font.size = Pt(10)
    p_pill.font.bold = True
    p_pill.font.color.rgb = CYAN_ACCENT
    p_pill.alignment = PP_ALIGN.CENTER

    # Main Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.8))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_LIGHT

    if subtitle:
        p_sub = tf_title.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card

def add_metric_box(slide, left, top, width, height, metric: str, label: str, accent_color=CYAN_ACCENT):
    add_card(slide, left, top, width, height, CARD_BG, accent_color)
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    p1 = tf.paragraphs[0]
    p1.text = metric
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = accent_color
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = label
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER

def create_presentation():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, "Explainable_AI_Loan_Default_Prediction_Presentation.pptx")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ========================================================
    # SLIDE 1: TITLE SLIDE
    # ========================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Accent Top Stripe
    stripe = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = TEAL_ACCENT
    stripe.line.fill.background()

    # Main Center Container
    add_card(slide1, Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.2), CARD_BG, TEAL_ACCENT)

    tb = slide1.shapes.add_textbox(Inches(1.5), Inches(1.6), Inches(10.333), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "CAPSTONE TECHNICAL DEFENSE & PRESENTATION"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_ACCENT

    p1 = tf.add_paragraph()
    p1.text = "Explainable AI for Loan Default Prediction"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT

    p2 = tf.add_paragraph()
    p2.text = "Using SHAP (TreeExplainer) & LIME (Local Linear Surrogates)"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = TEAL_ACCENT

    p3 = tf.add_paragraph()
    p3.text = "Bridging High-Accuracy Gradient Boosted Trees with Regulatory Adverse Action Compliance (ECOA Reg B & FCRA)"
    p3.font.size = Pt(12)
    p3.font.color.rgb = TEXT_MUTED

    # Metadata Badges
    badges = [
        ("Dataset", "100,000 Applicants", Inches(1.5), Inches(4.8), Inches(2.2)),
        ("Champion Model", "XGBoost (0.894 AUC)", Inches(3.9), Inches(4.8), Inches(2.5)),
        ("Inference Latency", "8.60 ms (TreeSHAP)", Inches(6.6), Inches(4.8), Inches(2.3)),
        ("Author", "Anshu Raj", Inches(9.1), Inches(4.8), Inches(2.2)),
    ]
    for b_label, b_val, left, top, width in badges:
        add_metric_box(slide1, left, top, width, Inches(1.0), b_val, b_label, TEAL_ACCENT)

    # ========================================================
    # SLIDE 2: THE BANKING DILEMMA & PROBLEM STATEMENT
    # ========================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Problem Statement", "The Accuracy vs. Transparency Dilemma in Credit Risk", "Why financial institutions struggle to deploy black-box machine learning models in regulated lending")

    # Column 1: Traditional Scorecards
    add_card(slide2, Inches(0.8), Inches(1.9), Inches(5.6), Inches(5.0))
    tb = slide2.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.0), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Traditional Linear Scorecards (Basel II/III)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    bullets1 = [
        "Relies on Logistic Regression with manual Weight-of-Evidence (WOE) binning.",
        "Fully transparent and auditable for banking regulators.",
        "FAILED to capture high-order non-linear risk interactions (e.g. toxic debt burden combined with low FICO).",
        "Results in mispriced credit risk and millions in default charge-offs.",
        "Rejects creditworthy thin-file borrowers due to rigid linear assumptions."
    ]
    for b in bullets1:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_LIGHT

    # Column 2: Modern Black-Box Machine Learning
    add_card(slide2, Inches(6.8), Inches(1.9), Inches(5.6), Inches(5.0))
    tb = slide2.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.0), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "High-Capacity Machine Learning (XGBoost)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT

    bullets2 = [
        "Captures deep non-linear patterns, reducing default losses by over 50%.",
        "Operates as an opaque 'black-box' across hundreds of decision trees.",
        "BLOCKED by strict consumer protection regulations (ECOA / FCRA).",
        "Illegal to deny loan applicants without providing specific principal reasons.",
        "Our Solution: Pair champion XGBoost with axiomatic SHAP & LIME to achieve both peak accuracy and 100% regulatory transparency."
    ]
    for b in bullets2:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_LIGHT

    # ========================================================
    # SLIDE 3: REGULATORY & LEGAL MANDATES
    # ========================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "Compliance Drivers", "Why Explainability is Legally Mandatory in Banking", "Federal laws strictly forbid black-box decisions in automated credit underwriting")

    reg_cards = [
        ("ECOA Regulation B (12 CFR § 1002.9)",
         "Mandates that creditors provide an Adverse Action Notice (AAN) disclosing the top principal reasons (typically 4) whenever credit is denied or provided on less favorable terms. Blanket denial statements are strictly illegal.",
         Inches(0.8), Inches(1.9), Inches(5.6), Inches(2.3), TEAL_ACCENT),

        ("CFPB Circular 2022-03",
         "Explicitly establishes that creditors cannot avoid explaining decisions by claiming algorithmic technology is too complex. If an algorithm makes a credit denial, lenders MUST provide specific, verifiable reasons.",
         Inches(6.8), Inches(1.9), Inches(5.6), Inches(2.3), CYAN_ACCENT),

        ("Fair Credit Reporting Act (FCRA)",
         "Protects consumers from inaccurate or arbitrary bureau scoring and mandates disclosure of key negative score factors affecting approval, empowering consumer dispute rights.",
         Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.3), GOLD_ACCENT),

        ("Federal Reserve SR 11-7 / OCC 2011-12",
         "Supervisory guidance on Model Risk Management (MRM). Mandates conceptual soundness, rigorous benchmarking against linear models, and continuous tracking of model/explainability drift.",
         Inches(6.8), Inches(4.5), Inches(5.6), Inches(2.3), GREEN_ACCENT),
    ]

    for title, desc, left, top, width, height, accent in reg_cards:
        add_card(slide3, left, top, width, height, CARD_BG, accent)
        tb = slide3.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = accent
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_LIGHT

    # ========================================================
    # SLIDE 4: END-TO-END ARCHITECTURE
    # ========================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Architecture", "End-to-End System Architecture & Data Flow", "A modular, containerized pipeline from raw applicant ingestion to compliance notices")

    arch_steps = [
        ("1. Ingestion Layer", "Processes raw borrower features: demographics, employment, income, FICO score, DTI, loan intent, and bureau derogatory marks.", Inches(0.8), TEAL_ACCENT),
        ("2. Preprocessing & Encoding", "Median/mode imputation, monotonic ordinal grading (A=0 to F=5), nominal one-hot encoding, and 80/20 stratified train/test split.", Inches(3.2), CYAN_ACCENT),
        ("3. XGBoost Inference", "200-tree gradient boosted ensemble computing calibrated Default Probability P(Default) with scale_pos_weight class balancing.", Inches(5.6), GOLD_ACCENT),
        ("4. Dual XAI Engine", "SHAP TreeExplainer computes exact Shapley attributions in 8.6ms; LIME generates 5,000 local neighborhood perturbations.", Inches(8.0), RED_ACCENT),
        ("5. Adverse Action Engine", "Maps top-4 risk drivers to CFPB reason statements and computes actionable counterfactual guidance for denied consumers.", Inches(10.4), GREEN_ACCENT),
    ]

    for step_title, step_desc, left, accent in arch_steps:
        add_card(slide4, left, Inches(2.0), Inches(2.1), Inches(4.8), CARD_BG, accent)
        tb = slide4.shapes.add_textbox(left + Inches(0.15), Inches(2.2), Inches(1.8), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = step_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = accent

        p2 = tf.add_paragraph()
        p2.text = step_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_LIGHT

    # ========================================================
    # SLIDE 5: 100,000 DATASET BENCHMARK
    # ========================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Data Engineering", "100,000 (1 Lakh) Applicant Credit Risk Dataset", "Synthesized to reflect LendingClub, Fannie Mae, and FICO bureau risk distributions")

    # Metrics on left
    add_metric_box(slide5, Inches(0.8), Inches(1.9), Inches(3.6), Inches(1.1), "100,000", "Total Loan Applicants (1 Lakh)", CYAN_ACCENT)
    add_metric_box(slide5, Inches(0.8), Inches(3.2), Inches(3.6), Inches(1.1), "26.89%", "Realistic Default Rate (26,888 Defaults)", RED_ACCENT)
    add_metric_box(slide5, Inches(0.8), Inches(4.5), Inches(3.6), Inches(1.1), "14 Features", "13 Predictors + 1 Target Variable", TEAL_ACCENT)
    add_metric_box(slide5, Inches(0.8), Inches(5.8), Inches(3.6), Inches(1.1), "6.51 MB", "Clean Benchmark CSV Dataset Size", GOLD_ACCENT)

    # Right Card: Key Underwriting Indicators Table
    add_card(slide5, Inches(4.8), Inches(1.9), Inches(7.7), Inches(5.0))
    tb = slide5.shapes.add_textbox(Inches(5.0), Inches(2.1), Inches(7.3), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Key Underwriting Feature Indicators & Covariances"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    table_lines = [
        "• loan_percent_income: Loan principal divided by annual income (debt leverage burden).",
        "• debt_to_income (DTI): Non-mortgage recurring monthly debt / monthly income (0.05 to 0.65).",
        "• credit_score: FICO bureau score (350 to 850); scores < 580 incur steep default probabilities.",
        "• cb_person_default_on_file: Historical 90+ day delinquency or charge-off on bureau record.",
        "• loan_int_rate & loan_grade: Risk-based pricing tier assigned by underwriting (Grades A to F).",
        "• person_emp_length & person_age: Career stability and employment tenure indicators.",
        "• loan_intent: Stated loan purpose (Debt Consolidation, Medical, Education, Venture, Personal)."
    ]
    for tl in table_lines:
        p = tf.add_paragraph()
        p.text = tl
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_LIGHT

    # ========================================================
    # SLIDE 6: MODEL BENCHMARK & METRICS
    # ========================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Model Performance", "Multi-Model Benchmarks on 20,000 Out-of-Sample Applicants", "Comprehensive evaluation across discrimination, minority-class precision, and calibration")

    # Left: Comparison Table
    add_card(slide6, Inches(0.8), Inches(1.9), Inches(6.8), Inches(5.0))
    tb = slide6.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(6.4), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Performance Metric Comparison (20,000 Test Set)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    rows = [
        ("Evaluation Metric", "Logistic Reg.", "Random Forest", "XGBoost (Champion)"),
        ("ROC-AUC", "0.8872", "0.8919", "0.8941 (Highest)"),
        ("PR-AUC (Avg Precision)", "0.7781", "0.7888", "0.7940 (Highest)"),
        ("Accuracy", "76.54%", "83.12%", "84.28% (Highest)"),
        ("F1-Score", "0.7018", "0.7106", "0.7074"),
        ("Brier Score (Loss)", "0.1295", "0.1238", "0.1263 (Calibrated)"),
        ("Inference Latency", "0.003 ms", "0.065 ms", "0.012 ms (Sub-ms)"),
        ("Optimal Cutoff Threshold", "0.50", "0.38", "0.35 (Cost-Optimized)")
    ]
    for row in rows:
        p = tf.add_paragraph()
        p.text = f"{row[0]:<25} | {row[1]:<12} | {row[2]:<14} | {row[3]}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_LIGHT if "XGBoost" not in row[3] else CYAN_ACCENT

    # Right: Embed ROC or PR Curve image if exists
    roc_img_path = os.path.join(base_dir, 'performance result', 'roc_curves_comparison.png')
    if os.path.exists(roc_img_path):
        add_card(slide6, Inches(7.9), Inches(1.9), Inches(4.6), Inches(5.0))
        slide6.shapes.add_picture(roc_img_path, Inches(8.1), Inches(2.1), Inches(4.2), Inches(4.4))

    # ========================================================
    # SLIDE 7: SHAP (COOPERATIVE GAME THEORY)
    # ========================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "Explainable AI: SHAP", "Mathematical Rigor: Shapley Value Formulations", "Cooperative Game Theory guarantees fair, additive attribution across all features")

    # Formula Box
    add_card(slide7, Inches(0.8), Inches(1.9), Inches(11.7), Inches(1.4), CARD_BG, TEAL_ACCENT)
    tb = slide7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "The Shapley Value Formula (Lloyd Shapley, 1953 Nobel Prize)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p2 = tf.add_paragraph()
    p2.text = "φ_i(v) = Σ [ (|S|! (|N| - |S| - 1)!) / |N|! ] × [ v(S ∪ {i}) - v(S) ]    (Summed over all subsets S ⊆ N \\ {i})"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_LIGHT

    # 4 Axiom Cards
    axioms = [
        ("1. Efficiency (Local Accuracy)", "Σ φ_i = f(x) - E[f(X)]. Attributions exactly sum to the difference between individual prediction and base rate. No credit lost.", Inches(0.8), Inches(3.6)),
        ("2. Symmetry (Equal Treatment)", "If two features contribute identical value to all coalitions, their attributions are identical. Eliminates arbitrary bias.", Inches(6.8), Inches(3.6)),
        ("3. Dummy Player (Null)", "If a feature has zero marginal predictive value across all coalitions, its attribution is strictly zero (φ_i = 0).", Inches(0.8), Inches(5.3)),
        ("4. Additivity (Linear Ensembles)", "For ensemble models (XGBoost), overall attribution is the exact linear sum of attributions of individual trees.", Inches(6.8), Inches(5.3)),
    ]
    for a_title, a_desc, left, top in axioms:
        add_card(slide7, left, top, Inches(5.7), Inches(1.5), CARD_BG, CARD_BORDER)
        tb = slide7.shapes.add_textbox(left + Inches(0.15), top + Inches(0.15), Inches(5.4), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = a_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEAL_ACCENT
        p2 = tf.add_paragraph()
        p2.text = a_desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_LIGHT

    # ========================================================
    # SLIDE 8: SHAP VISUALIZATIONS (GLOBAL & LOCAL)
    # ========================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "Visual Explainability", "Global Beeswarm Summary vs. Local Waterfall Breakdown", "Providing macro portfolio visibility alongside individual loan denial explanations")

    sum_path = os.path.join(base_dir, 'reports', 'shap_summary.png')
    wf_path = os.path.join(base_dir, 'reports', 'shap_waterfall_example.png')

    if os.path.exists(sum_path) and os.path.exists(wf_path):
        # Left: Global Summary
        add_card(slide8, Inches(0.8), Inches(1.9), Inches(5.6), Inches(5.0))
        slide8.shapes.add_picture(sum_path, Inches(1.0), Inches(2.1), Inches(5.2), Inches(3.8))
        tb = slide8.shapes.add_textbox(Inches(1.0), Inches(6.0), Inches(5.2), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "Global Beeswarm: loan_percent_income, DTI, and credit_score dominate overall portfolio risk."
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED

        # Right: Local Waterfall
        add_card(slide8, Inches(6.8), Inches(1.9), Inches(5.6), Inches(5.0))
        slide8.shapes.add_picture(wf_path, Inches(7.0), Inches(2.1), Inches(5.2), Inches(3.8))
        tb = slide8.shapes.add_textbox(Inches(7.0), Inches(6.0), Inches(5.2), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "Local Waterfall: Decomposes applicant score from baseline E[f(X)] to individual 98.5% default prediction."
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED

    # ========================================================
    # SLIDE 9: LIME & EMPIRICAL CONCORDANCE
    # ========================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "Explainable AI: LIME", "Local Linear Surrogates & SHAP Concordance Benchmark", "Translating continuous features into human-readable conditional rules")

    add_card(slide9, Inches(0.8), Inches(1.9), Inches(6.0), Inches(5.0))
    tb = slide9.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.6), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LIME Mechanics (Local Surrogates)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT

    lime_text = [
        "• Generates 5,000 synthetic perturbations around applicant.",
        "• Weights perturbations by exponential distance kernel: π_x(z) = exp(-D(x,z)² / σ²).",
        "• Fits a sparse Ridge regression minimizing fidelity loss + complexity: argmin L(f, g, π) + Ω(g).",
        "• Discretized Rule Examples:",
        "    - loan_percent_income > 0.40  (+0.231 to Default Risk)",
        "    - loan_int_rate > 17.50%       (+0.205 to Default Risk)",
        "    - credit_score <= 580          (+0.195 to Default Risk)",
        "    - loan_grade >= Grade D        (+0.184 to Default Risk)",
        "• Intuitive format for frontline loan officers."
    ]
    for lt in lime_text:
        p = tf.add_paragraph()
        p.text = lt
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_LIGHT

    # Right: Concordance Stats
    add_card(slide9, Inches(7.1), Inches(1.9), Inches(5.4), Inches(5.0))
    tb = slide9.shapes.add_textbox(Inches(7.3), Inches(2.1), Inches(5.0), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Empirical SHAP vs. LIME Concordance"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    add_metric_box(slide9, Inches(7.4), Inches(2.8), Inches(4.8), Inches(1.0), "0.879", "Spearman Feature Rank Correlation", TEAL_ACCENT)
    add_metric_box(slide9, Inches(7.4), Inches(4.0), Inches(4.8), Inches(1.0), "100.0%", "Directional Concordance Agreement", GREEN_ACCENT)
    add_metric_box(slide9, Inches(7.4), Inches(5.2), Inches(4.8), Inches(1.0), "8.6 ms vs 112 ms", "Inference Latency (TreeSHAP ~13× Faster)", CYAN_ACCENT)

    # ========================================================
    # SLIDE 10: REGULATORY ADVERSE ACTION NOTICE
    # ========================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "Regulatory Compliance", "Automated ECOA Adverse Action Notice & Recourse", "Translating SHAP attributions into legally required CFPB denial reasons with actionable recourse")

    # Center Notice Card
    add_card(slide10, Inches(1.0), Inches(1.9), Inches(11.333), Inches(5.0), CARD_BG, RED_ACCENT)
    tb = slide10.shapes.add_textbox(Inches(1.3), Inches(2.1), Inches(10.7), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "STATEMENT OF CREDIT DENIAL (ECOA REGULATION B / 12 CFR § 1002.9)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RED_ACCENT

    p = tf.add_paragraph()
    p.text = "Applicant ID: APP-TEST-001 | Status: REJECTED | Predicted Default Risk: 98.51% (Threshold: 35.0%)"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    p = tf.add_paragraph()
    p.text = "\nMandatory Principal Reasons for Adverse Action (CFPB Statement Codes):"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    reasons = [
        "1. Credit score does not meet minimum credit tier guidelines (FICO: 520, SHAP Impact: +1.334)",
        "2. Assigned underwriting risk rating exceeds risk tolerance threshold (Grade: E, SHAP Impact: +1.197)",
        "3. High loan amount relative to verifiable annual income (Loan % Income: 56.3%, SHAP Impact: +0.780)",
        "4. High borrowing cost tier assigned based on current credit profile (Interest Rate: 21.50%, SHAP: +0.742)"
    ]
    for r in reasons:
        p = tf.add_paragraph()
        p.text = r
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_LIGHT

    p = tf.add_paragraph()
    p.text = "\nActionable Counterfactual Recourse (Consumer Remediation Guidance):"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT

    recourse = [
        "• Reduce requested loan principal from $18,000 to $8,000 to lower leverage below 25%.",
        "• Maintain 6+ consecutive months of on-time payments to rebuild FICO credit score above 650 cutoff.",
        "• Pay down existing revolving lines to bring credit debt-to-income (DTI) below 30%."
    ]
    for rc in recourse:
        p = tf.add_paragraph()
        p.text = rc
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_LIGHT

    # ========================================================
    # SLIDE 11: WORKING PROTOTYPES & DEPLOYMENT
    # ========================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11)
    add_header(slide11, "Implementation", "Multi-Platform Working Prototypes & Deployment", "Accessible via Interactive Web UI, Terminal CLI, and REST API Microservices")

    proto_cards = [
        ("Web Dashboard (Streamlit)",
         "Full interactive underwriter portal with applicant parameter sliders, live probability gauges, real-time SHAP waterfall charts, LIME rule breakdowns, and PDF compliance notice generation.",
         Inches(0.8), TEAL_ACCENT),

        ("Terminal CLI Prototype",
         "Interactive terminal application (cli_prototype.py) enabling credit officers to evaluate pre-loaded profiles (Prime, Subprime, Borderline) or input custom applicant records instantly.",
         Inches(4.8), CYAN_ACCENT),

        ("REST API & Containers",
         "Production-ready REST microservice (api_prototype.py on Port 8080) with endpoints (/predict, /explain, /adverse-action), multi-stage Dockerfile, and docker-compose orchestration.",
         Inches(8.8), GOLD_ACCENT),
    ]
    for title, desc, left, accent in proto_cards:
        add_card(slide11, left, Inches(1.9), Inches(3.7), Inches(5.0), CARD_BG, accent)
        tb = slide11.shapes.add_textbox(left + Inches(0.2), Inches(2.1), Inches(3.3), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = accent
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_LIGHT

    # ========================================================
    # SLIDE 12: QA VERIFICATION & TESTING
    # ========================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12)
    add_header(slide12, "QA & Validation", "Automated Testing Suite & Stress Benchmarks", "Exhaustive unit testing, invariance checks, and concurrent latency audits")

    # Left: Test Summary Metrics
    add_metric_box(slide12, Inches(0.8), Inches(1.9), Inches(3.6), Inches(1.1), "100% Passed", "7/7 Test Cases Verified", GREEN_ACCENT)
    add_metric_box(slide12, Inches(0.8), Inches(3.2), Inches(3.6), Inches(1.1), "7.53 ms", "Mean API Latency (100 Requests)", CYAN_ACCENT)
    add_metric_box(slide12, Inches(0.8), Inches(4.5), Inches(3.6), Inches(1.1), "10.51 ms", "p95 Latency SLA (< 200 ms)", TEAL_ACCENT)
    add_metric_box(slide12, Inches(0.8), Inches(5.8), Inches(3.6), Inches(1.1), "0.8939 ± 0.0008", "5-Fold CV Stability (Zero Overfitting)", GOLD_ACCENT)

    # Right: Test Cases Table
    add_card(slide12, Inches(4.8), Inches(1.9), Inches(7.7), Inches(5.0))
    tb = slide12.shapes.add_textbox(Inches(5.0), Inches(2.1), Inches(7.3), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Verified Automated Test Matrix (run_test_suite.py)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    tests = [
        "• TC-01 [Data Integrity]: Schema validation, null checks across 100,000 records (PASSED)",
        "• TC-02 [Pipeline Transformation]: Output shape alignment & categorical encoding (PASSED)",
        "• TC-03 [Probability Bounds]: Enforces P(Default) strictly in [0.0, 1.0] interval (PASSED)",
        "• TC-04 [SHAP Efficiency Axiom]: Mathematical proof that Σ φ_i = f(x) - E[f(X)] (PASSED)",
        "• TC-05 [LIME Surrogate Fidelity]: Local neighborhood perturbation & rule extraction (PASSED)",
        "• TC-06 [Regulatory Compliance]: Enforces exactly top-4 CFPB reason codes (PASSED)",
        "• TC-07 [Boundary Stress Test]: Prime (FICO 850) vs Deep Subprime (FICO 350) (PASSED)"
    ]
    for t in tests:
        p = tf.add_paragraph()
        p.text = t
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_LIGHT

    # ========================================================
    # SLIDE 13: BUSINESS & P&L VALUE
    # ========================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13)
    add_header(slide13, "Business Impact", "Strategic P&L Value & Risk Reduction", "How Explainable AI maximizes credit portfolio revenue while safeguarding compliance")

    cards13 = [
        ("50.2% Reduction in Portfolio Losses",
         "By switching from traditional linear scorecards to tuned XGBoost, false negative defaults were cut dramatically, preventing unrecovered principal losses on defaulted loans under asymmetric 5:1 loss matrices.",
         Inches(0.8), Inches(1.9), Inches(5.6), Inches(2.3), TEAL_ACCENT),

        ("Zero Regulatory Non-Compliance Risk",
         "Automated generation of CFPB-compliant Adverse Action Notices eliminates legal penalties and regulatory enforcement risks under ECOA Regulation B and CFPB Circular 2022-03.",
         Inches(6.8), Inches(1.9), Inches(5.6), Inches(2.3), GREEN_ACCENT),

        ("Consumer Financial Inclusion",
         "Actionable counterfactual recourse empowers rejected borrowers with concrete steps to improve creditworthiness, building customer loyalty and driving secondary loan origination.",
         Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.3), CYAN_ACCENT),

        ("Sub-Millisecond Real-Time Decisioning",
         "8.6ms TreeSHAP computation allows live point-of-sale financing, e-commerce loan origination, and instant digital credit card approvals without batch latency bottlenecks.",
         Inches(6.8), Inches(4.5), Inches(5.6), Inches(2.3), GOLD_ACCENT),
    ]
    for title, desc, left, top, width, height, accent in cards13:
        add_card(slide13, left, top, width, height, CARD_BG, accent)
        tb = slide13.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = accent
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_LIGHT

    # ========================================================
    # SLIDE 14: CONCLUSION & ROADMAP
    # ========================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14)
    add_header(slide14, "Conclusion", "Capstone Defense Summary & Future Roadmap", "Enterprise-ready Explainable AI framework combining state-of-the-art ML with banking ethics")

    add_card(slide14, Inches(0.8), Inches(1.9), Inches(11.7), Inches(5.0))
    tb = slide14.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Key Project Achievements"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    achieve = [
        "✔ End-to-end Explainable AI pipeline trained and benchmarked on 100,000 loan applicants.",
        "✔ Champion XGBoost model achieving 0.8941 ROC-AUC and 0.7940 PR-AUC with sub-millisecond inference.",
        "✔ Implementation of both SHAP (Cooperative Game Theory) and LIME (Local Surrogates) with 100% directional agreement.",
        "✔ Automated legal Adverse Action Notice generator with CFPB reason codes and counterfactual guidance.",
        "✔ Complete suite of working prototypes: Web UI (Streamlit), Terminal CLI, and REST API Docker container."
    ]
    for a in achieve:
        p = tf.add_paragraph()
        p.text = a
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_LIGHT

    p = tf.add_paragraph()
    p.text = "\nFuture Roadmap & Enhancements"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT

    roadmap = [
        "1. Algorithmic Counterfactual Search: Integrate DiCE (Diverse Counterfactual Explanations) to automate shortest approval paths.",
        "2. Fairness-Aware ML: Implement Fairlearn adversarial debiasing to mathematically enforce demographic parity.",
        "3. Monotonic XGBoost Constraints: Enforce negative monotonic constraints on credit scores to guarantee zero risk inversion."
    ]
    for r in roadmap:
        p = tf.add_paragraph()
        p.text = r
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_LIGHT

    p = tf.add_paragraph()
    p.text = "\nOpen Source Repository: https://github.com/anshu4021/loan_default  |  Thank You! Questions?"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GOLD_ACCENT

    # Save Presentation
    prs.save(output_path)
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"[+] Successfully generated master presentation: {output_path} ({file_size_mb:.2f} MB)")

if __name__ == '__main__':
    create_presentation()
