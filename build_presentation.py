import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions: 13.333 x 7.5 inches
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean Clinical Color Palette (All White Backgrounds)
    WHITE = RGBColor(255, 255, 255)
    NAVY_DARK = RGBColor(15, 23, 42)          # #0F172A
    NAVY_CARD = RGBColor(30, 41, 59)          # #1E293B
    TEXT_MAIN = RGBColor(15, 23, 42)          # #0F172A
    TEXT_MUTED = RGBColor(100, 116, 139)      # #64748B
    BLUE_PRIMARY = RGBColor(2, 132, 199)      # #0284C7
    BLUE_LIGHT = RGBColor(56, 189, 248)       # #38BDF8
    BLUE_BG = RGBColor(240, 249, 255)         # #F0F9FF
    CARD_BG = RGBColor(248, 250, 252)         # #F8FAFC
    CARD_BORDER = RGBColor(226, 232, 240)     # #E2E8F0
    CRIMSON = RGBColor(225, 29, 72)           # #E11D48
    EMERALD = RGBColor(16, 185, 129)          # #10B981
    ROW_ALT = RGBColor(241, 245, 249)         # #F1F5F9

    def add_slide():
        s = prs.slides.add_slide(blank_layout)
        # Set solid white background
        bg = s.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = WHITE
        # Add smooth fade transition for premium animated feel
        t_xml = '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med"><p:fade/></p:transition>'
        s._element.append(parse_xml(t_xml))
        return s

    def add_header(slide, title, category=None):
        if category:
            cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.30))
            tf_cat = cat_box.text_frame
            tf_cat.word_wrap = True
            tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
            p_cat = tf_cat.paragraphs[0]
            p_cat.text = category.upper()
            p_cat.font.name = 'Calibri'
            p_cat.font.size = Pt(9.5)
            p_cat.font.bold = True
            p_cat.font.color.rgb = BLUE_PRIMARY

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.7), Inches(0.55))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = 'Calibri'
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.24), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.color.rgb = CARD_BORDER

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1)
        else:
            shape.line.fill.background()
        return shape

    def add_metric_badge(slide, left, top, width, height, num_str, label_str, num_color=BLUE_PRIMARY):
        add_card(slide, left, top, width, height, bg_color=WHITE, border_color=CARD_BORDER)
        box = slide.shapes.add_textbox(left + Inches(0.12), top + Inches(0.10), width - Inches(0.24), height - Inches(0.20))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p_num = tf.paragraphs[0]
        p_num.text = num_str
        p_num.font.name = 'Calibri'
        p_num.font.size = Pt(24)
        p_num.font.bold = True
        p_num.font.color.rgb = num_color
        p_num.alignment = PP_ALIGN.CENTER

        p_lbl = tf.add_paragraph()
        p_lbl.text = label_str
        p_lbl.font.name = 'Calibri'
        p_lbl.font.size = Pt(9.5)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = TEXT_MUTED
        p_lbl.alignment = PP_ALIGN.CENTER

    def add_footer(slide, current_idx, total_slides=10):
        box = slide.shapes.add_textbox(Inches(0.8), Inches(7.12), Inches(11.733), Inches(0.25))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"CSE 4114: Introduction to Data Science Lab  |  Rumman Islam  |  Slide {current_idx} of {total_slides}"
        p.font.name = 'Calibri'
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Clean Clinical White Background)
    # =========================================================================
    s1 = add_slide()

    # Blue top accent strip
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.7), Inches(2.2), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = BLUE_PRIMARY
    top_bar.line.fill.background()

    # Title Card container
    add_card(s1, Inches(0.8), Inches(0.95), Inches(11.733), Inches(3.4), bg_color=CARD_BG, border_color=CARD_BORDER)
    tbox1 = s1.shapes.add_textbox(Inches(1.1), Inches(1.15), Inches(11.1), Inches(3.0))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True

    p_c = tf1.paragraphs[0]
    p_c.text = "CSE 4114: INTRODUCTION TO DATA SCIENCE LAB  •  PROJECT DEFENSE"
    p_c.font.name = 'Calibri'
    p_c.font.size = Pt(13)
    p_c.font.bold = True
    p_c.font.color.rgb = BLUE_PRIMARY

    p_t = tf1.add_paragraph()
    p_t.text = "Breast Cancer Diagnosis & Morphometric Modeling\nUsing Logistic Regression"
    p_t.font.name = 'Calibri'
    p_t.font.size = Pt(32)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY_DARK
    p_t.space_before = Pt(8)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Complete Data Science Workflow: Preprocessing, 8-D EDA, Classification, Clustering & Regression"
    p_sub.font.name = 'Calibri'
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_before = Pt(8)

    p_meta = tf1.add_paragraph()
    p_meta.text = "Student: Rumman Islam  |  Dataset: Wisconsin Diagnostic (WDBC, N = 1,138)  |  September 2026"
    p_meta.font.name = 'Calibri'
    p_meta.font.size = Pt(12)
    p_meta.font.bold = True
    p_meta.font.color.rgb = BLUE_PRIMARY
    p_meta.space_before = Pt(10)

    # 4 Key Stat Badges at the Bottom (White Cards with subtle border)
    stat_items = [
        ("93.42%", "LOGISTIC REGRESSION ACCURACY", BLUE_PRIMARY),
        ("0.9887", "AUC-ROC PROBABILISTIC POWER", EMERALD),
        ("0.9962", "R² PERIMETER REGRESSION", BLUE_PRIMARY),
        ("1,138", "AUGMENTED PATIENT BIOPSIES", NAVY_DARK)
    ]
    for i, (num_str, lbl_str, col) in enumerate(stat_items):
        bx = Inches(0.8 + i * 2.98)
        by = Inches(4.7)
        bw = Inches(2.78)
        bh = Inches(1.8)
        add_card(s1, bx, by, bw, bh, bg_color=WHITE, border_color=CARD_BORDER)

        box = s1.shapes.add_textbox(bx + Inches(0.15), by + Inches(0.25), bw - Inches(0.3), bh - Inches(0.5))
        tf = box.text_frame
        tf.word_wrap = True
        p_n = tf.paragraphs[0]
        p_n.text = num_str
        p_n.font.name = 'Calibri'
        p_n.font.size = Pt(30)
        p_n.font.bold = True
        p_n.font.color.rgb = col
        p_n.alignment = PP_ALIGN.CENTER

        p_l = tf.add_paragraph()
        p_l.text = lbl_str
        p_l.font.name = 'Calibri'
        p_l.font.size = Pt(9.5)
        p_l.font.bold = True
        p_l.font.color.rgb = TEXT_MUTED
        p_l.alignment = PP_ALIGN.CENTER
        p_l.space_before = Pt(6)

    add_footer(s1, 1, 10)

    # =========================================================================
    # SLIDE 2: 2.1 PROBLEM STATEMENT & PROJECT OBJECTIVES
    # =========================================================================
    s2 = add_slide()
    add_header(s2, "2.1 Problem Statement and Project Objectives", "Section 2.1 · Clinical Context & Workflow")
    add_footer(s2, 2, 10)

    # Left Card
    add_card(s2, Inches(0.8), Inches(1.45), Inches(5.7), Inches(4.2))
    b2_l = s2.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(5.2), Inches(3.8))
    tf2_l = b2_l.text_frame
    tf2_l.word_wrap = True

    p = tf2_l.paragraphs[0]
    p.text = "Clinical Problem & Motivation"
    p.font.name = 'Calibri'
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    bullets_2l = [
        "Breast cancer is one of the most prevalent and lethal malignancies worldwide.",
        "Early detection dramatically improves patient survival (>98% 5-year localized survival).",
        "Fine Needle Aspirate (FNA) biopsy evaluation by pathologists is time-intensive, subjective, and prone to fatigue.",
        "Need: An automated, highly explainable decision-support algorithm to assist oncologists."
    ]
    for b in bullets_2l:
        p = tf2_l.add_paragraph()
        p.text = "• " + b
        p.font.name = 'Calibri'
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    # Right Card
    add_card(s2, Inches(6.8), Inches(1.45), Inches(5.733), Inches(4.2), bg_color=BLUE_BG, border_color=BLUE_PRIMARY)
    b2_r = s2.shapes.add_textbox(Inches(7.05), Inches(1.65), Inches(5.2), Inches(3.8))
    tf2_r = b2_r.text_frame
    tf2_r.word_wrap = True

    p = tf2_r.paragraphs[0]
    p.text = "Research Question & Project Objectives"
    p.font.name = 'Calibri'
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BLUE_PRIMARY

    bullets_2r = [
        "Primary Research Question:\nCan Logistic Regression classify breast tumor malignancy with high accuracy, high sensitivity, and explainable feature weights?",
        "Target Output:\nBinary classification predicting Malignant (M = 1) vs Benign (B = 0) with calibrated probability outputs.",
        "Core Deliverables:\n1. Supervised Classification (Logistic Regression, DT, RF)\n2. Unsupervised Clustering (K-Means, Silhouette, PCA)\n3. Predictive Regression (Linear Regression on Perimeter)"
    ]
    for b in bullets_2r:
        p = tf2_r.add_paragraph()
        p.text = "• " + b
        p.font.name = 'Calibri'
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    # Bottom Workflow Ribbon
    add_card(s2, Inches(0.8), Inches(5.85), Inches(11.733), Inches(1.05), bg_color=CARD_BG)
    strip_box = s2.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.3), Inches(0.8))
    tf_str = strip_box.text_frame
    p_str = tf_str.paragraphs[0]
    p_str.text = "Complete Data Science Workflow (CSE 4114 Pipeline):"
    p_str.font.name = 'Calibri'
    p_str.font.size = Pt(11)
    p_str.font.bold = True
    p_str.font.color.rgb = NAVY_DARK

    p_str2 = tf_str.add_paragraph()
    p_str2.text = "Problem Definition → Dataset Acquisition → Preprocessing → EDA → Visualization → Feature Engineering → Selection → Machine Learning → Evaluation → Conclusion"
    p_str2.font.name = 'Calibri'
    p_str2.font.size = Pt(11)
    p_str2.font.bold = True
    p_str2.font.color.rgb = BLUE_PRIMARY
    p_str2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 3: 2.2 DATASET DESCRIPTION & 2.3 DATA COLLECTION
    # =========================================================================
    s3 = add_slide()
    add_header(s3, "2.2 Dataset Description, Source & 2.3 Data Collection", "Section 2.2 - 2.3 · Data Acquisition")
    add_footer(s3, 3, 10)

    # Left: Native Specs Table
    table_shape3 = s3.shapes.add_table(8, 2, Inches(0.8), Inches(1.45), Inches(6.8), Inches(5.4))
    t3 = table_shape3.table
    t3.columns[0].width = Inches(2.4)
    t3.columns[1].width = Inches(4.4)

    specs = [
        ("Dataset Name", "Breast Cancer Wisconsin Diagnostic (WDBC)"),
        ("Source", "Kaggle — mehmetisik/breast-cancercsv"),
        ("Original Records", "569 patient biopsy samples"),
        ("Augmented Records", "1,138 records (duplicated for >= 1,000 lab quota)"),
        ("Total Features", "31 columns (30 numerical features + 1 target)"),
        ("Target Variable", "diagnosis: Malignant (M = 1) / Benign (B = 0)"),
        ("Missing Values", "0 (100% complete data integrity verified)"),
        ("Data Scaling", "StandardScaler applied across all continuous features")
    ]
    for row_idx, (item, details) in enumerate(specs):
        c0, c1 = t3.cell(row_idx, 0), t3.cell(row_idx, 1)
        c0.text, c1.text = item, details
        bg = NAVY_DARK if row_idx == 0 else (ROW_ALT if row_idx % 2 == 1 else WHITE)
        fg = WHITE if row_idx == 0 else TEXT_MAIN
        for cell, is_hdr in [(c0, True), (c1, False)]:
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cp = cell.text_frame.paragraphs[0]
            cp.font.name = 'Calibri'
            cp.font.size = Pt(10.5)
            cp.font.bold = is_hdr or (row_idx == 0)
            cp.font.color.rgb = fg

    # Right: Metric Badges
    add_metric_badge(s3, Inches(7.9), Inches(1.45), Inches(4.6), Inches(1.5), "1,138", "Total Augmented Patient Records", BLUE_PRIMARY)
    add_metric_badge(s3, Inches(7.9), Inches(3.3), Inches(4.6), Inches(1.5), "0 Missing", "100% Data Completeness Across 31 Columns", EMERALD)
    add_metric_badge(s3, Inches(7.9), Inches(5.15), Inches(4.6), Inches(1.5), "30 Features", "Digitized Nuclear Morphometric Metrics", NAVY_DARK)

    # =========================================================================
    # SLIDE 4: 2.4 DATA CLEANING AND PREPROCESSING
    # =========================================================================
    s4 = add_slide()
    add_header(s4, "2.4 Data Cleaning and Preprocessing Pipeline", "Section 2.4 · Data Quality & Scaling")
    add_footer(s4, 4, 10)

    prep_cards = [
        ("1. Missing Value Audit", "Programmatic verification using df.isnull().sum() confirmed 0 missing values across all 31 columns (100% data completeness). No imputation required.", EMERALD),
        ("2. Duplicate & Row Augmentation", "Augmented dataset from 569 original clinical samples to 1,138 rows to fulfill the CSE 4114 requirement (>= 1,000 rows) while strictly preserving joint distributions.", BLUE_PRIMARY),
        ("3. Outlier Analysis & Preservation", "Interquartile Range (IQR) boxplots revealed extreme area values (>2,000 mm²) in malignant samples. These were preserved as genuine pathological indicators of tumor growth.", CRIMSON),
        ("4. Feature Standardization & Encoding", "Target variable was label encoded: Malignant (M) → 1, Benign (B) → 0. Continuous features standardized using StandardScaler (mean = 0, variance = 1).", NAVY_DARK)
    ]
    for i, (title, desc, col) in enumerate(prep_cards):
        cx = Inches(0.8 + (i % 2) * 5.98)
        cy = Inches(1.45 + (i // 2) * 2.5)
        cw = Inches(5.75)
        ch = Inches(2.3)
        add_card(s4, cx, cy, cw, ch)
        cb = s4.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.2), cw - Inches(0.5), ch - Inches(0.4))
        ctf = cb.text_frame
        ctf.word_wrap = True

        p = ctf.paragraphs[0]
        p.text = title
        p.font.name = 'Calibri'
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col

        p = ctf.add_paragraph()
        p.text = desc
        p.font.name = 'Calibri'
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(6)

    # Bottom code ribbon
    add_card(s4, Inches(0.8), Inches(6.1), Inches(11.733), Inches(0.8), bg_color=CARD_BG)
    b4_c = s4.shapes.add_textbox(Inches(1.0), Inches(6.2), Inches(11.3), Inches(0.6))
    tf4_c = b4_c.text_frame
    p = tf4_c.paragraphs[0]
    p.text = "Python Scikit-Learn Pipeline:  scaler = StandardScaler()  |  X_train_scaled = scaler.fit_transform(X_train)  |  X_test_scaled = scaler.transform(X_test)"
    p.font.name = 'Courier New'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_PRIMARY

    # =========================================================================
    # SLIDE 5: 2.5 EXPLORATORY DATA ANALYSIS (EDA) & CLASS DISTRIBUTION
    # =========================================================================
    s5 = add_slide()
    add_header(s5, "2.5 Exploratory Data Analysis (EDA) & Class Distribution", "Section 2.5 · Statistical Exploration")
    add_footer(s5, 5, 10)

    img_p1 = "images/01_bar_diagnosis_count.png"
    img_p2 = "images/02_pie_diagnosis_ratio.png"
    if os.path.exists(img_p1):
        s5.shapes.add_picture(img_p1, Inches(0.8), Inches(1.45), Inches(5.7), Inches(4.2))
    if os.path.exists(img_p2):
        s5.shapes.add_picture(img_p2, Inches(6.8), Inches(1.45), Inches(5.7), Inches(4.2))

    # Bottom Card
    add_card(s5, Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.15))
    b5 = s5.shapes.add_textbox(Inches(1.0), Inches(5.9), Inches(11.3), Inches(0.95))
    tf5 = b5.text_frame
    p = tf5.paragraphs[0]
    p.text = "Key Findings from Exploratory Analysis:"
    p.font.name = 'Calibri'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    p = tf5.add_paragraph()
    p.text = "• Class Distribution: 714 Benign (62.7%) vs 424 Malignant (37.3%). Mild class imbalance requires reporting Precision, Recall, and AUC alongside raw Accuracy.\n• Morphometric Disparity: Malignant nuclei display substantially higher mean dimensions (Radius: 17.46 mm vs 12.15 mm; Area: 978 mm² vs 463 mm²)."
    p.font.name = 'Calibri'
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(2)

    # =========================================================================
    # SLIDE 6: 2.6 DATA VISUALIZATION GALLERY
    # =========================================================================
    s6 = add_slide()
    add_header(s6, "2.6 Data Visualization — Diagnostic Patterns", "Section 2.6 · Multi-Dimensional Visual Evidence")
    add_footer(s6, 6, 10)

    # 4-image grid
    imgs_6 = [
        ("images/03_histogram_radius_distribution.png", Inches(0.8), Inches(1.45), Inches(5.7), Inches(2.55)),
        ("images/04_boxplot_area_by_diagnosis.png", Inches(6.8), Inches(1.45), Inches(5.7), Inches(2.55)),
        ("images/05_scatterplot_radius_vs_texture.png", Inches(0.8), Inches(4.2), Inches(5.7), Inches(2.55)),
        ("images/08_line_feature_profile.png", Inches(6.8), Inches(4.2), Inches(5.7), Inches(2.55))
    ]
    for path, left, top, width, height in imgs_6:
        if os.path.exists(path):
            s6.shapes.add_picture(path, left, top, width, height)

    add_footer(s6, 6, 10)

    # =========================================================================
    # SLIDE 7: 2.7 FEATURE ENGINEERING & 2.8 FEATURE SELECTION
    # =========================================================================
    s7 = add_slide()
    add_header(s7, "2.7 Feature Engineering & 2.8 Feature Selection", "Section 2.7 - 2.8 · Feature Optimization")
    add_footer(s7, 7, 10)

    img_p6 = "images/06_heatmap_correlation.png"
    if os.path.exists(img_p6):
        s7.shapes.add_picture(img_p6, Inches(0.8), Inches(1.45), Inches(5.8), Inches(4.5))

    add_card(s7, Inches(6.9), Inches(1.45), Inches(5.633), Inches(5.3))
    b7 = s7.shapes.add_textbox(Inches(7.15), Inches(1.65), Inches(5.1), Inches(4.9))
    tf7 = b7.text_frame
    tf7.word_wrap = True

    p = tf7.paragraphs[0]
    p.text = "Selected 7 Core Features"
    p.font.name = 'Calibri'
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    feats_selected = [
        ("1. radius_mean", "Strongest primary morphometric discriminator"),
        ("2. texture_mean", "Independent gray-scale variance in FNA image"),
        ("3. smoothness_mean", "Quantile binned: local radius length variations"),
        ("4. compactness_mean", "Shape complexity: perimeter² / area - 1.0"),
        ("5. concavity_mean", "Severity of concave contour indents"),
        ("6. concave points_mean", "Number of contour concave portions"),
        ("7. symmetry_mean", "Cell nucleus asymmetry indicator")
    ]
    for feat, reas in feats_selected:
        p = tf7.add_paragraph()
        p.text = f"• {feat}: {reas}"
        p.font.name = 'Calibri'
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(4)

    p = tf7.add_paragraph()
    p.text = "Multicollinearity Elimination (r > 0.98):"
    p.font.name = 'Calibri'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = CRIMSON
    p.space_before = Pt(8)

    p = tf7.add_paragraph()
    p.text = "perimeter_mean and area_mean were dropped due to near-perfect collinearity with radius_mean, preventing variance inflation and unstable beta weights."
    p.font.name = 'Calibri'
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(2)

    # =========================================================================
    # SLIDE 8: 2.9 MACHINE LEARNING MODEL DEVELOPMENT
    # =========================================================================
    s8 = add_slide()
    add_header(s8, "2.9 Machine Learning Model Development (Tri-Faceted Suite)", "Section 2.9 · ML Suite (Classification, Clustering, Regression)")
    add_footer(s8, 8, 10)

    # 3 Category Cards
    ml_categories = [
        ("1. CLASSIFICATION (PRIMARY)", "Logistic Regression: P(Y=1|X) = 1 / (1 + e^(-z))\nOutputs calibrated probability & explainable odds-ratios.\nBenchmarks: Decision Tree (depth=5) & Random Forest (100 trees).", BLUE_PRIMARY),
        ("2. CLUSTERING (UNSUPERVISED)", "K-Means Clustering (K=2):\nGroups patient morphometric profiles without diagnosis labels.\nEvaluated via Elbow Curve & Silhouette score (~0.41) in 2D PCA space.", NAVY_DARK),
        ("3. REGRESSION (PREDICTIVE)", "Multiple Linear Regression:\nPredicts continuous tumor perimeter_mean from radius, area & texture.\nAchieves R² = 0.9962 and MAE = 0.81 mm, validating geometric linearity.", EMERALD)
    ]
    for i, (m_title, m_desc, m_col) in enumerate(ml_categories):
        cx = Inches(0.8 + i * 3.98)
        cy = Inches(1.45)
        cw = Inches(3.8)
        gh = Inches(2.5)
        add_card(s8, cx, cy, cw, gh)
        gb = s8.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.18), cw - Inches(0.4), gh - Inches(0.36))
        gtf = gb.text_frame
        gtf.word_wrap = True

        p = gtf.paragraphs[0]
        p.text = m_title
        p.font.name = 'Calibri'
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = m_col

        p = gtf.add_paragraph()
        p.text = m_desc
        p.font.name = 'Calibri'
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(4)

    # Bottom Images (Regression Fit + Feature Importance)
    img_reg = "images/12_regression_actual_vs_pred.png"
    img_imp = "images/14_feature_importance.png"
    if os.path.exists(img_reg):
        s8.shapes.add_picture(img_reg, Inches(0.8), Inches(4.15), Inches(5.7), Inches(2.75))
    if os.path.exists(img_imp):
        s8.shapes.add_picture(img_imp, Inches(6.8), Inches(4.15), Inches(5.7), Inches(2.75))

    # =========================================================================
    # SLIDE 9: 2.10 MODEL EVALUATION & COMPARISON
    # =========================================================================
    s9 = add_slide()
    add_header(s9, "2.10 Model Evaluation & Comparison", "Section 2.10 · Benchmark Performance")
    add_footer(s9, 9, 10)

    # Top Benchmark Table
    table_shape9 = s9.shapes.add_table(4, 6, Inches(0.8), Inches(1.45), Inches(11.733), Inches(1.8))
    t9 = table_shape9.table
    t9.columns[0].width = Inches(2.5)
    t9.columns[1].width = Inches(1.6)
    t9.columns[2].width = Inches(1.6)
    t9.columns[3].width = Inches(1.6)
    t9.columns[4].width = Inches(1.6)
    t9.columns[5].width = Inches(2.833)

    headers9 = ["Algorithm", "Accuracy", "Precision", "Recall", "F1-Score", "Key Clinical Trait"]
    rows9 = [
        ["Decision Tree (depth=5)", "97.81%", "98.78%", "95.29%", "97.01%", "Hierarchical rule tree"],
        ["Random Forest (100 trees)", "99.12%", "100.00%", "97.65%", "98.81%", "Top raw accuracy ensemble"],
        ["Logistic Regression", "93.42%", "90.67%", "89.47%", "90.07%", "Clinically explainable log-odds"]
    ]
    for col_idx, h in enumerate(headers9):
        c = t9.cell(0, col_idx)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = NAVY_DARK
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = c.text_frame.paragraphs[0]
        p.font.name = 'Calibri'
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

    for row_idx, r_data in enumerate(rows9, 1):
        for col_idx, val in enumerate(r_data):
            c = t9.cell(row_idx, col_idx)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = ROW_ALT if row_idx % 2 == 1 else WHITE
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = c.text_frame.paragraphs[0]
            p.font.name = 'Calibri'
            p.font.size = Pt(10.5)
            p.font.bold = (row_idx == 3) or (col_idx == 0)
            p.font.color.rgb = BLUE_PRIMARY if (row_idx == 3 and col_idx == 0) else TEXT_MAIN
            p.alignment = PP_ALIGN.CENTER if col_idx in [1, 2, 3, 4] else PP_ALIGN.LEFT

    # Bottom Images: Confusion Matrix + ROC Curve
    img_cm = "images/09_confusion_matrix.png"
    img_roc = "images/13_roc_curve.png"
    if os.path.exists(img_cm):
        s9.shapes.add_picture(img_cm, Inches(0.8), Inches(3.45), Inches(4.8), Inches(3.45))
    if os.path.exists(img_roc):
        s9.shapes.add_picture(img_roc, Inches(5.9), Inches(3.45), Inches(4.8), Inches(3.45))

    # Right Card: Diagnostic Insights
    add_card(s9, Inches(10.9), Inches(3.45), Inches(1.633), Inches(3.45), bg_color=CARD_BG)
    b9_r = s9.shapes.add_textbox(Inches(10.95), Inches(3.55), Inches(1.5), Inches(3.25))
    tf9_r = b9_r.text_frame
    tf9_r.word_wrap = True
    p = tf9_r.paragraphs[0]
    p.text = "DIAGNOSIS"
    p.font.name = 'Calibri'
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE_PRIMARY

    p = tf9_r.add_paragraph()
    p.text = "TN = 145\nTP = 68\nFN = 8\nFP = 7\n\nAUC = 0.9887 confirms 98.9% true ranking power."
    p.font.name = 'Calibri'
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 10: 2.11 RESULTS, DISCUSSION, LIMITATIONS & CONCLUSION
    # =========================================================================
    s10 = add_slide()
    add_header(s10, "2.11 Results, Discussion, Limitations & Conclusion", "Section 2.11 · Clinical Takeaways & Defense")
    add_footer(s10, 10, 10)

    conc_cards = [
        ("1. Dominant Biomarkers Identified", "Cellular contour indentations (concave points_mean, β = +2.40) and nuclear enlargement (radius_mean, β = +2.84) are the primary physical drivers of tumor malignancy.", BLUE_PRIMARY),
        ("2. Clinical Interpretability Advantage", "While Random Forest achieved higher raw accuracy (99.12%), Logistic Regression provides transparent odds-ratio weights essential for medical ethics, clinician trust, and regulatory auditability.", NAVY_DARK),
        ("3. Risk Threshold Calibration", "With an AUC of 0.9887, clinicians can shift down the operational decision threshold to 0.35 in high-risk screening to drive False Negatives close to zero without causing severe false alarms.", EMERALD),
        ("4. Limitations & Future Work", "Synthetic duplication was used to satisfy the 1,000-row lab quota; mild class imbalance exists. Future work: SMOTE resampling, non-linear SVM, and CNN computer vision on raw biopsy tiles.", CRIMSON)
    ]

    for i, (ctitle, cdesc, ccol) in enumerate(conc_cards):
        cx = Inches(0.8 + (i % 2) * 5.98)
        cy = Inches(1.45 + (i // 2) * 2.5)
        cw = Inches(5.75)
        ch = Inches(2.3)
        add_card(s10, cx, cy, cw, ch)
        cb = s10.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.18), cw - Inches(0.5), ch - Inches(0.36))
        ctf = cb.text_frame
        ctf.word_wrap = True

        p = ctf.paragraphs[0]
        p.text = ctitle
        p.font.name = 'Calibri'
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = ccol

        p = ctf.add_paragraph()
        p.text = cdesc
        p.font.name = 'Calibri'
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(6)

    # Bottom Banner
    add_card(s10, Inches(0.8), Inches(6.1), Inches(11.733), Inches(0.85), bg_color=CARD_BG, border_color=CARD_BORDER)
    b10_sub = s10.shapes.add_textbox(Inches(1.0), Inches(6.2), Inches(11.3), Inches(0.65))
    tf10_s = b10_sub.text_frame
    p = tf10_s.paragraphs[0]
    p.text = "References: [1] Street et al. (1993) IS&T/SPIE  |  [2] Mehmed Isik Kaggle WDBC  |  [3] Pedregosa et al. (2011) JMLR  |  Thank You! Ready for Defense & Q&A."
    p.font.name = 'Calibri'
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = BLUE_PRIMARY

    # Save presentation
    output_filename = "DS_LAB_PRESENTATION.pptx"
    prs.save(output_filename)
    print(f"10-slide white animated presentation saved successfully as '{output_filename}'!")

if __name__ == '__main__':
    create_presentation()
