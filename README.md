# data-science

# 🔬 Breast Cancer Diagnostic Preprocessing, EDA & Advanced Machine Learning

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-Academic%20Lab-green.svg)](#)
[![Accuracy](https://img.shields.io/badge/Logistic%20Regression-93.42%25-brightgreen)](#)
[![AUC-ROC](https://img.shields.io/badge/AUC--ROC-0.9887-cyan)](#)

A comprehensive data science and medical machine learning project analyzing the **Breast Cancer Wisconsin Diagnostic Dataset (WDBC)**. This project encompasses end-to-end data preprocessing, 8-dimensional exploratory data analysis (EDA), supervised classification, unsupervised clustering, and predictive regression for clinical decision support.

---

## 🖥️ Interactive Presentation & Research Deck (`index.html`)

The repository includes a modern, responsive web presentation deck and research report built with vanilla HTML5, CSS3, and modern JavaScript:

- **Two Viewing Modes:**
  - **Slide Deck Mode:** Fullscreen interactive keynote presentation with keyboard navigation (`←` / `→` / `Space`), progress tracking, fullscreen toggle (`F`), slide overview grid (`O`), and presenter rehearsal stopwatch.
  - **Continuous Report Mode:** Detailed executive dashboard with high-resolution visual inspectors.
- **Live Machine Learning Simulator:** Interactive Logistic Regression inference calculator testing how variations in `radius_mean`, `texture_mean`, `concave points_mean`, and `compactness_mean` shift the calculated malignancy probability in real-time.
- **Viva Voce Defense Accordion:** Bilingual (English & বাংলা) answers to top examiner questions.

> **To view the presentation:** Simply open [`index.html`](index.html) in any modern web browser or host it via GitHub Pages.

---

## 📊 Dataset Overview

| Attribute | Details |
| :--- | :--- |
| **Dataset Name** | Breast Cancer Wisconsin Diagnostic Dataset (WDBC) |
| **Source** | Kaggle (`mehmetisik/breast-cancercsv`) |
| **Total Records** | **1,138 samples** (augmented from 569 to meet $\ge 1,000$ row requirements) |
| **Total Features** | 31 columns (30 continuous nuclear features + 1 target) |
| **Target Variable** | `diagnosis` (`M` = Malignant / `B` = Benign) |
| **Missing Values** | **0 null values** (100% complete) |
| **Class Distribution** | 714 Benign (62.7%) vs 424 Malignant (37.3%) |

---

## 🛠️ Methodology & Pipeline

```
Raw Biopsy Data (Kaggle) 
   │
   ▼
[1] Preprocessing & Cleaning ──► 0 Nulls · Label Encoding (M=1, B=0) · Row Augmentation (1,138)
   │
   ▼
[2] Standardization ─────────► StandardScaler (μ = 0, σ = 1) across all continuous metrics
   │
   ▼
[3] Exploratory Analysis ────► 8-D Visualization: Distributions, Boxplots, Scatter, Heatmap
   │
   ▼
[4] Feature Selection ───────► VIF Reduction (Dropped perimeter & area due to r > 0.98 collinearity)
   │
   ▼
[5] Machine Learning ────────► Logistic Regression · Decision Tree · Random Forest · K-Means (K=2)
   │
   ▼
[6] Diagnostic Validation ───► Accuracy (93.42%), AUC-ROC (0.9887), Sensitivity & Specificity
```

---

## 🏆 Model Benchmark & Performance Results

### Classification Metrics (Test Set: 20% Split, N = 228)

| Model | Accuracy | Precision | Recall | F1-Score | AUC-ROC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest** | **99.12%** | **100.00%** | **97.65%** | **98.81%** | 0.999 |
| **Decision Tree** | 97.81% | 98.78% | 95.29% | 97.01% | 0.978 |
| **Logistic Regression** | 93.42% | 91.00% | 89.47% | 90.22% | **0.9887** |

> **Clinical Note:** While Random Forest achieves higher raw accuracy, **Logistic Regression** is the preferred clinical standard due to complete model transparency and direct odds-ratio interpretability ($\beta$ coefficients).

---

## 📈 Visualizations & Key Figures

All charts are generated with `generate_report_assets.py` and saved under `images/`:

- `images/01_bar_diagnosis_count.png` — Benign (714) vs Malignant (424) class balance
- `images/02_pie_diagnosis_ratio.png` — Diagnosis class proportions
- `images/03_histogram_radius_distribution.png` — Radius distribution shift between diagnoses
- `images/04_boxplot_area_by_diagnosis.png` — Area outliers and high variance in malignant nuclei
- `images/05_scatterplot_radius_vs_texture.png` — Bivariate scatter separation
- `images/06_heatmap_correlation.png` — Pearson correlation matrix showing multicollinearity
- `images/07_countplot_smoothness.png` — Frequency of smoothness levels across classes
- `images/08_line_feature_profile.png` — Mean feature profile curves
- `images/09_confusion_matrix.png` — Logistic Regression test confusion matrix
- `images/10_kmeans_elbow.png` — Unsupervised K-Means elbow plot confirming $K=2$
- `images/11_kmeans_clusters_pca.png` — 2D PCA cluster space projection
- `images/12_regression_actual_vs_pred.png` — Multiple Linear Regression fit ($R^2 > 0.99$)
- `images/13_roc_curve.png` — Receiver Operating Characteristic (AUC = 0.9887)
- `images/14_feature_importance.png` — Standardized Logistic Regression coefficient weights

---

## 📁 Repository Structure

```
data-science/
├── index.html                      # Interactive full presentation deck & web report
├── README.md                       # Repository overview and documentation
├── .gitignore                      # Git ignore configuration (excluding .venv, .kilo, etc.)
├── breast-cancer.csv               # Kaggle Wisconsin Diagnostic Breast Cancer dataset
├── lab_report_breast_cancer.ipynb  # Interactive Jupyter Notebook analysis
├── DS_LAB_REPORT.md                # Full academic laboratory report (Markdown)
├── DS_LAB_REPORT.docx              # Formatted Microsoft Word lab report
├── DS_LAB_REPORT.pdf               # Print-ready academic PDF report
├── LAB_REPORT.md                   # Data Warehousing & Data Mining lab document
├── VIVA_QUESTIONS_ANSWERS.md       # Comprehensive Viva Voce defense Q&A guide (Bilingual)
├── analysis_summary.txt            # Analytical summary and statistical metrics
├── build_notebook.py               # Notebook builder automation
├── convert_to_docx.py              # Word document generator
├── convert_to_pdf.py               # PDF document generator
├── generate_report_assets.py       # Matplotlib & Seaborn visualization generator
└── images/                         # 22 High-resolution visualization charts
```

---

## 🚀 Getting Started

### 1. View Presentation
Double-click `index.html` to open it in your browser. Use the arrow keys or the on-screen dock controls to navigate through the slides.

### 2. Run the Jupyter Notebook
```bash
# Clone the repository
git clone https://github.com/rumman-islam/data-science.git
cd data-science

# Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn jupyter

# Launch notebook
jupyter notebook lab_report_breast_cancer.ipynb
```

---

## 👤 Author & Lab Defense
- **Author:** Rumman Islam / Rumman Khatun (Aduri)
- **Course:** Data Warehousing, Data Mining & Data Science Lab
- **GitHub:** [@rumman-islam](https://github.com/rumman-islam)
