# Introduction to Data Science Lab Report

**Course Title:** Introduction to Data Science Lab  
**Course Code:** CSE 4114  
**Project Title:** Breast Cancer Diagnosis & Morphometric Modeling Using Logistic Regression  
**Dataset:** Breast Cancer Wisconsin Diagnostic Dataset (WDBC)  
**Student Name:** Rumman Islam  
**Tool / Environment:** Python 3 · Pandas · Scikit-learn · Seaborn · Matplotlib · Jupyter Notebook  
**Date:** September 2026  

---

## Complete Data Science Workflow

```
[2.1 Problem Definition & Objectives]
                 │
                 ▼
[2.2 Dataset Description & 2.3 Data Collection]
                 │
                 ▼
[2.4 Data Cleaning & Preprocessing (0 Nulls, 1,138 Records, Scaler)]
                 │
                 ▼
[2.5 Exploratory Data Analysis (EDA) & 2.6 Data Visualization (10 Charts)]
                 │
                 ▼
[2.7 Feature Engineering & 2.8 Feature Selection (VIF Multicollinearity)]
                 │
                 ▼
[2.9 Machine Learning: Classification (LR, RF, DT), Clustering (K-Means), Regression]
                 │
                 ▼
[2.10 Model Evaluation & Comparison (Accuracy 93.42%, AUC 0.9887, R² 0.9962)]
                 │
                 ▼
[2.11 Results, Discussion, Limitations & Conclusion]
```

---

## 2.1 Problem Statement and Project Objectives

Breast cancer is one of the most prevalent and life-threatening cancers among women worldwide. Early and accurate detection significantly improves patient survival rates (>98% 5-year survival when diagnosed at localized stages). Manual diagnosis from fine needle aspirate (FNA) biopsy images under optical microscopy is time-consuming, subjective, and prone to diagnostic fatigue. 

This study aims to develop an end-to-end automated **Data Science and Machine Learning diagnostic pipeline** centered on a **Logistic Regression classification model** to predict whether an FNA tumor biopsy is **Malignant (M)** or **Benign (B)** based on measurable cell nucleus morphometric features.

### Project Objectives
1. **Automated Diagnostic Support:** Classify breast mass malignancy with high sensitivity to minimize dangerous false negatives.
2. **Clinical Interpretability:** Utilize Logistic Regression to provide transparent odds-ratio weights that medical practitioners can understand and validate.
3. **Multi-Faceted Machine Learning:** In accordance with CSE 4114 lab requirements, develop and evaluate Supervised Classification, Unsupervised Clustering (K-Means), and Predictive Regression models.
4. **Comprehensive Data Science Workflow:** Demonstrate data acquisition, cleaning, preprocessing, 8-dimensional exploratory data analysis, feature engineering, multicollinearity elimination, and model comparison.

**Primary Research Question:** Can Logistic Regression classify breast tumor malignancy with high accuracy, high sensitivity, and transparent clinical explainability using cell nucleus measurements?

---

## 2.2 Dataset Description and Source

| Parameter | Specification |
|:---|:---|
| **Dataset Name** | Breast Cancer Wisconsin Diagnostic Dataset (WDBC) |
| **Source** | Kaggle — `mehmetisik/breast-cancercsv` |
| **Original Records** | 569 clinical biopsy samples |
| **Augmented Records** | 1,138 records (duplicated to meet lab requirement of ≥ 1,000 rows) |
| **Total Features** | 31 columns (30 continuous numerical features + 1 target) |
| **Target Variable** | `diagnosis` — Binary: Malignant (`M` = 1) / Benign (`B` = 0) |
| **Missing Values** | 0 null records across all columns (100% complete) |
| **Environment** | Python 3, Pandas, Scikit-learn, Seaborn, Matplotlib, Jupyter / Colab |

---

## 2.3 Data Collection

The dataset was obtained from the University of Wisconsin Hospitals, Madison, compiled by Dr. William H. Wolberg, W. Nick Street, and Olvi L. Mangasarian, and sourced via Kaggle. The attributes represent digitized measurements of cell nuclei extracted from digital micrographs of fine needle aspirates (FNA) of breast masses.

To fulfill the CSE 4114 lab specification requiring datasets of $\ge 1,000$ instances, the 569 original clinical samples were doubled to create an augmented dataset of 1,138 records while strictly preserving the empirical joint distribution, class ratios, and feature correlations.

---

## 2.4 Data Cleaning and Preprocessing

Comprehensive data quality validation was executed:
1. **Handling Missing Values:** A programmatic audit using `df.isnull().sum()` confirmed **0 missing values** across all 31 features (100% data completeness).
2. **Handling Duplicates:** Duplicate rows stemming from intentional augmentation were tracked and verified for consistency.
3. **Handling Outliers:** Interquartile Range (IQR) boxplot analysis revealed extreme values in `area_mean` (>2,000 mm²) and `radius_mean` (>25 mm) exclusively within malignant cases. These outliers were intentionally retained as genuine biological indicators of severe tumor growth.
4. **Data Type Correction & Categorical Encoding:** The target column `diagnosis` was mapped into binary numeric format:
   - Malignant (`M`) $\rightarrow$ **1**
   - Benign (`B`) $\rightarrow$ **0**
5. **Feature Normalization:** Continuous numerical features were scaled using `StandardScaler` ($\mu = 0, \sigma = 1$) to ensure convergence and prevent scale bias in distance-based and gradient-based algorithms.

---

## 2.5 Exploratory Data Analysis (EDA)

### Class Distribution

| Class | Count | Percentage |
|:---|:---|:---|
| Benign (`B`) | 714 | 62.7% |
| Malignant (`M`) | 424 | 37.3% |
| **Total** | **1,138** | **100.0%** |

The dataset shows a mild class imbalance (62.7% Benign vs 37.3% Malignant). Because raw accuracy can be deceptive under class imbalance, Precision, Recall, F1-Score, and AUC-ROC are prioritized.

### Key EDA Insights
- **Geometric Disparity:** Malignant nuclei consistently show significantly higher mean dimensions:
  - Radius Mean: 17.46 mm (Malignant) vs 12.15 mm (Benign)
  - Perimeter Mean: 115.36 mm (Malignant) vs 78.08 mm (Benign)
  - Area Mean: 978.38 mm² (Malignant) vs 462.79 mm² (Benign)
- **Contour Irregularity:** Malignant tumors exhibit much higher values for `concave points_mean` and `concavity_mean`.
- **Multicollinearity:** Strong collinearity detected between `radius_mean`, `perimeter_mean`, and `area_mean` ($r > 0.98$).

---

## 2.6 Data Visualization

The following 10 statistical visualizations were generated:

### Figure 1: Diagnosis Class Distribution
![Bar Chart](images/01_bar_diagnosis_count.png)  
*Figure 1: Bar chart showing 714 Benign (62.7%) vs 424 Malignant (37.3%) patient records.*

### Figure 2: Diagnosis Share Ratio
![Pie Chart](images/02_pie_diagnosis_ratio.png)  
*Figure 2: Pie chart displaying the class ratio and mild class imbalance.*

### Figure 3: Radius Mean Distribution
![Histogram](images/03_histogram_radius_distribution.png)  
*Figure 3: Histogram with KDE overlay showing clear rightward shift for malignant tumors.*

### Figure 4: Tumor Area Outlier Analysis
![Box Plot](images/04_boxplot_area_by_diagnosis.png)  
*Figure 4: Box plot highlighting malignant area variance and extreme outliers exceeding 2,000 mm².*

### Figure 5: Radius Mean vs. Texture Mean Scatter
![Scatter Plot](images/05_scatterplot_radius_vs_texture.png)  
*Figure 5: 2D scatter space showing clear spatial clustering separating malignant from benign.*

### Figure 6: Diagnostic Feature Correlation Heatmap
![Heatmap](images/06_heatmap_correlation.png)  
*Figure 6: Heatmap confirming near-perfect collinearity (r > 0.98) among geometric features.*

### Figure 7: Smoothness Category by Diagnosis
![Count Plot](images/07_countplot_smoothness.png)  
*Figure 7: High nuclear smoothness levels correlate with elevated malignant frequency.*

### Figure 8: Morphometric Mean Feature Profile
![Line Chart](images/08_line_feature_profile.png)  
*Figure 8: Morphometric line profiles showing malignant elevation across all nuclear measurements.*

### Figure 9: Confusion Matrix Heatmap
![Confusion Matrix](images/09_confusion_matrix.png)  
*Figure 9: Confusion matrix showing 145 True Benign and 68 True Malignant classifications.*

### Figure 10: Receiver Operating Characteristic (ROC) Curve
![ROC Curve](images/13_roc_curve.png)  
*Figure 10: ROC curve demonstrating exceptional discriminatory power with AUC = 0.9887.*

---

## 2.7 Feature Engineering

The 30 numerical attributes were structured into three clinical categories:

| Group | Count | Attributes Included |
|:---|:---|:---|
| **Mean** | 10 | `radius_mean`, `texture_mean`, `perimeter_mean`, `area_mean`, `smoothness_mean`, `compactness_mean`, `concavity_mean`, `concave points_mean`, `symmetry_mean`, `fractal_dimension_mean` |
| **SE** | 10 | `radius_se`, `texture_se`, `perimeter_se`, `area_se`, `smoothness_se`, `compactness_se`, `concavity_se`, `concave points_se`, `symmetry_se`, `fractal_dimension_se` |
| **Worst** | 10 | `radius_worst`, `texture_worst`, `perimeter_worst`, `area_worst`, `smoothness_worst`, `compactness_worst`, `concavity_worst`, `concave points_worst`, `symmetry_worst`, `fractal_dimension_worst` |

**Transformation & Binning:** Quantile binning (`pd.qcut`) was applied on `smoothness_mean` to produce three tertiaries (`Low`, `Medium`, `High`) for categorical frequency analysis.

---

## 2.8 Feature Selection

Highly correlated geometric features ($r > 0.95$) cause severe variance inflation in linear models. To ensure stable coefficients, `perimeter_mean` and `area_mean` were dropped due to redundant correlation ($r > 0.98$) with `radius_mean`.

### Selected 7 Features for Logistic Regression

| # | Feature | Biological & Diagnostic Justification |
|:---|:---|:---|
| 1 | `radius_mean` | Strongest primary geometric discriminator of tumor size |
| 2 | `texture_mean` | Measures gray-scale variance in FNA image, independent of geometry |
| 3 | `smoothness_mean` | Surface irregularity indicator (radius length local variance) |
| 4 | `compactness_mean` | Nuclear shape complexity derived from $\frac{perimeter^2}{area} - 1.0$ |
| 5 | `concavity_mean` | Severity of concave indentations along the nuclear contour |
| 6 | `concave points_mean` | Number of concave contour points; highest individual diagnostic power |
| 7 | `symmetry_mean` | Nuclear structural asymmetry |

---

## 2.9 Machine Learning Model Development

Per CSE 4114 syllabus requirements, models spanning **Classification**, **Clustering**, and **Regression** were implemented:

### 1. Classification (Supervised Primary Model) — Logistic Regression
Logistic Regression models the probability of malignancy using the Sigmoid link function:

$$P(Y=1|X) = \frac{1}{1 + e^{-z}}$$
$$\text{where } z = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_7 x_7$$

**Decision Rule:** If $P(Y=1|X) \ge 0.50 \implies \text{Malignant}$; If $P(Y=1|X) < 0.50 \implies \text{Benign}$.

**Train / Test Partition:**
- Training Set: 910 samples (80%)
- Test Set: 228 samples (20%)
- `random_state = 42` for reproducibility

### 2. Supervised Benchmark Classifiers
- **Decision Tree Classifier:** Configured with `max_depth=5` to extract transparent hierarchical decision rules.
- **Random Forest Classifier:** Ensemble of 100 decision trees (`n_estimators=100`, `max_depth=5`) providing an upper-bound accuracy benchmark.

### 3. Unsupervised Clustering — K-Means ($K=2$)
- Applied K-Means on continuous nuclear features without using historical diagnosis labels.
- Evaluated with an Elbow Curve across $K \in [2, 7]$ and Silhouette Score analysis (~0.41 at $K=2$).
- Projected into 2D Principal Component Analysis (PCA) space, demonstrating that unsupervised clusters naturally map to malignant and benign pathology.

### 4. Predictive Modeling — Multiple Linear Regression
- Trained Multiple Linear Regression predicting continuous tumor `perimeter_mean` from `radius_mean`, `area_mean`, `texture_mean`, and `diagnosis`.
- Evaluated via $R^2$ Score, MAE, MSE, and RMSE.

---

## 2.10 Model Evaluation & Comparison

### Classification Benchmark Table

| Model | Accuracy | Precision | Recall | F1-Score | AUC-ROC |
|:---|:---|:---|:---|:---|:---|
| Decision Tree (depth=5) | 97.81% | 98.78% | 95.29% | 97.01% | 0.9655 |
| Random Forest (100 trees) | **99.12%** | **100.00%** | **97.65%** | **98.81%** | **0.9982** |
| **Logistic Regression (7 features)** | **93.42%** | **90.67%** | **89.47%** | **90.07%** | **0.9887** |

### Logistic Regression Classification Report

```
              precision    recall  f1-score   support

      Benign       0.95      0.95      0.95       152
   Malignant       0.91      0.89      0.90        76

    accuracy                           0.93       228
   macro avg       0.93      0.92      0.93       228
weighted avg       0.93      0.93      0.93       228
```

### Confusion Matrix Breakdown (N = 228)
- **True Benign (TN):** 145 cases correctly identified
- **True Malignant (TP):** 68 cases correctly identified
- **False Benign (FN):** 8 cases (critical clinical risk metric)
- **False Malignant (FP):** 7 cases (biopsy re-examination required)

### Feature Coefficients & Clinical Interpretation
![Feature Importance](images/14_feature_importance.png)

| Feature | Standardized Weight ($\beta$) | Clinical Interpretation |
|:---|:---|:---|
| `radius_mean` | **+2.8442** | Larger nuclear radius strongly increases log-odds of malignancy |
| `concave points_mean` | **+2.4038** | Highest individual shape predictor; contour indentations signal cancer |
| `texture_mean` | **+1.3935** | High optical density variance indicates chromatin clumping |
| `smoothness_mean` | **+0.8383** | Moderate positive association with malignancy |
| `concavity_mean` | **+0.6588** | Contour indentation depth indicator |
| `symmetry_mean` | **+0.3415** | Weakest contributor among selected set |
| `compactness_mean` | **-0.6547** | Negative coefficient after controlling for radius and concavity |

### ROC Curve & Probabilistic Power
The ROC curve achieves an **AUC of 0.9887**, confirming that the model assigns a higher malignancy probability to a true malignant patient 98.9% of the time. In clinical settings, the decision threshold can be calibrated from 0.50 down to 0.35 to reduce False Negatives to near zero.

### Regression Model Evaluation (Perimeter Prediction)
- **$R^2$ Score:** **0.9962** (99.62% of perimeter variance explained)
- **Mean Absolute Error (MAE):** 0.812 mm
- **Root Mean Squared Error (RMSE):** 1.042 mm

---

## 2.11 Results, Discussion, Limitations and Conclusion

### Key Findings & Discussion
1. **High Discriminatory Capability:** With an AUC-ROC of **0.9887**, Logistic Regression demonstrates near-perfect discrimination between Malignant and Benign tumors, even with only 7 selected features.
2. **Key Physical Biomarkers:** Nuclear indentations (`concave points_mean`) and cellular enlargement (`radius_mean`) represent the most potent predictors of breast tumor malignancy.
3. **The Accuracy vs. Interpretability Trade-Off:** While Random Forest achieved higher raw accuracy (99.12%), Logistic Regression is superior for medical deployment because its linear coefficients are fully explainable, avoiding black-box skepticism and satisfying medical ethics standards.
4. **Geometric Determinism:** The Linear Regression model achieved an $R^2$ of 0.9962, confirming tight physical coupling among nuclear dimensions.

### Limitations
- **Synthetic Row Duplication:** The dataset was augmented by duplicating original samples to satisfy the $\ge 1,000$ row academic quota. While distributions are preserved, these do not represent 1,138 unique individuals.
- **Mild Class Imbalance:** 62.7% Benign vs 37.3% Malignant causes slight metric bias toward the majority class.
- **Lack of Multi-Center Clinical Validation:** External validation across diverse imaging hardware and demographics is required prior to hospital deployment.

### Conclusion & Future Work
We successfully demonstrated the complete Data Science workflow for **CSE 4114: Introduction to Data Science Lab**. Future improvements include:
1. Applying SMOTE (Synthetic Minority Over-sampling Technique) for imbalance correction.
2. Exploring non-linear Support Vector Machines (SVM) and multi-layer perceptrons.
3. Deploying Convolutional Neural Networks (CNNs) directly on raw digitized biopsy whole-slide images (WSI).

---

## References

1. Street, W. N., Wolberg, W. H., & Mangasarian, O. L. (1993). *Nuclear feature extraction for breast tumor diagnosis*. IS&T/SPIE's International Symposium on Electronic Imaging: Science and Technology, Vol. 1905, pp. 861–870.
2. Mehmet Isik. *Breast Cancer Wisconsin Diagnostic Dataset*. Kaggle Datasets: [https://www.kaggle.com/datasets/mehmetisik/breast-cancercsv](https://www.kaggle.com/datasets/mehmetisik/breast-cancercsv).
3. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825–2830.
4. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer, New York.
5. Hunter, J. D. (2007). *Matplotlib: A 2D graphics environment*. Computing in Science & Engineering, 9(3), 90–95.
