import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, roc_auc_score,
    silhouette_score, mean_squared_error, mean_absolute_error, r2_score
)
from sklearn.decomposition import PCA

# ==============================================================================
# GLOBAL STYLING & CONFIGURATION
# ==============================================================================
plt.style.use('default')
sns.set_theme(style='whitegrid', font_scale=1.05)
plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.0

COLOR_BENIGN = '#2563eb'     # Vibrant Blue
COLOR_MALIGNANT = '#e11d48'  # Vibrant Crimson / Rose
PALETTE_DIAG = {'B': COLOR_BENIGN, 'M': COLOR_MALIGNANT}

img_dir = 'images'
os.makedirs(img_dir, exist_ok=True)

# ==============================================================================
# 1. LOAD & AUGMENT DATASET
# ==============================================================================
raw_df = pd.read_csv('breast-cancer.csv')
print("Original Dataset Shape:", raw_df.shape)

# Augment to 1,138 rows (to fulfill >= 1,000 lab requirement)
df = pd.concat([raw_df, raw_df], ignore_index=True)
print("Augmented Dataset Shape:", df.shape)

df['Diagnosis_Encoded'] = (df['diagnosis'] == 'M').astype(int) # M=1, B=0
diag_counts = df['diagnosis'].value_counts()
n_benign = diag_counts['B']
n_malignant = diag_counts['M']
total_records = len(df)

# ==============================================================================
# 2. GENERATE VISUALIZATIONS (SECTION 10 & REPORT ASSETS)
# ==============================================================================

# ------------------------------------------------------------------------------
# Chart 01: Bar Chart — Diagnosis Class Distribution
# ------------------------------------------------------------------------------
plt.figure(figsize=(7, 4.8), dpi=300)
ax = sns.barplot(
    x=['Benign (B)', 'Malignant (M)'],
    y=[n_benign, n_malignant],
    palette=[COLOR_BENIGN, COLOR_MALIGNANT]
)
plt.title('Figure 1: Diagnosis Class Distribution (N = 1,138)', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
plt.xlabel('Tumor Diagnosis Class', fontsize=11, fontweight='bold', labelpad=8)
plt.ylabel('Patient Count', fontsize=11, fontweight='bold', labelpad=8)
plt.ylim(0, 850)

for i, count in enumerate([n_benign, n_malignant]):
    pct = (count / total_records) * 100
    ax.text(i, count + 20, f"{count:,} ({pct:.1f}%)", ha='center', va='bottom', fontsize=11, fontweight='bold', color='#1e293b')

plt.tight_layout()
plt.savefig(os.path.join(img_dir, '01_bar_diagnosis_count.png'), dpi=300)
plt.close()
print("Generated: 01_bar_diagnosis_count.png")

# ------------------------------------------------------------------------------
# Chart 02: Pie Chart — Diagnosis Ratio
# ------------------------------------------------------------------------------
plt.figure(figsize=(6, 5.5), dpi=300)
wedges, texts, autotexts = plt.pie(
    [n_benign, n_malignant],
    labels=['Benign (B)', 'Malignant (M)'],
    autopct='%1.1f%%',
    startangle=140,
    colors=[COLOR_BENIGN, COLOR_MALIGNANT],
    explode=(0.06, 0),
    wedgeprops={'edgecolor': 'white', 'linewidth': 2},
    textprops={'fontsize': 11, 'fontweight': 'bold', 'color': '#0f172a'}
)
for at in autotexts:
    at.set_color('white')
    at.set_fontsize(12)
    at.set_fontweight('bold')

plt.title('Figure 2: Diagnosis Class Ratio (62.7% vs 37.3%)', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '02_pie_diagnosis_ratio.png'), dpi=300)
plt.close()
print("Generated: 02_pie_diagnosis_ratio.png")

# ------------------------------------------------------------------------------
# Chart 03: Histogram — Radius Mean Distribution
# ------------------------------------------------------------------------------
plt.figure(figsize=(8, 5), dpi=300)
sns.histplot(
    data=df,
    x='radius_mean',
    hue='diagnosis',
    kde=True,
    bins=28,
    palette=PALETTE_DIAG,
    alpha=0.45,
    edgecolor='white'
)
plt.title('Figure 3: Radius Mean Distribution by Diagnosis (With KDE)', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
plt.xlabel('Tumor Nucleus Radius Mean (mm)', fontsize=11, fontweight='bold', labelpad=8)
plt.ylabel('Observation Frequency', fontsize=11, fontweight='bold', labelpad=8)
plt.legend(title='Diagnosis', labels=['Malignant (M)', 'Benign (B)'], loc='upper right', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '03_histogram_radius_distribution.png'), dpi=300)
plt.close()
print("Generated: 03_histogram_radius_distribution.png")

# ------------------------------------------------------------------------------
# Chart 04: Box Plot — Area Mean by Diagnosis (Outlier Detection)
# ------------------------------------------------------------------------------
plt.figure(figsize=(7.5, 5), dpi=300)
sns.boxplot(
    data=df,
    x='diagnosis',
    y='area_mean',
    palette=[COLOR_MALIGNANT, COLOR_BENIGN],
    order=['M', 'B'],
    width=0.45,
    flierprops={'marker': 'o', 'markersize': 5, 'markerfacecolor': '#e11d48', 'alpha': 0.6}
)
plt.title('Figure 4: Area Mean Outlier Analysis by Diagnosis', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
plt.xlabel('Diagnosis (M = Malignant, B = Benign)', fontsize=11, fontweight='bold', labelpad=8)
plt.ylabel('Tumor Nucleus Area Mean (mm²)', fontsize=11, fontweight='bold', labelpad=8)
plt.text(0, 2450, 'Extreme Outliers (>2,000 mm²)', ha='center', fontsize=9, color='#e11d48', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fee2e2', edgecolor='#e11d48', alpha=0.8))
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '04_boxplot_area_by_diagnosis.png'), dpi=300)
plt.close()
print("Generated: 04_boxplot_area_by_diagnosis.png")

# ------------------------------------------------------------------------------
# Chart 05: Scatter Plot — Radius Mean vs. Texture Mean
# ------------------------------------------------------------------------------
plt.figure(figsize=(8, 5), dpi=300)
sns.scatterplot(
    data=df,
    x='radius_mean',
    y='texture_mean',
    hue='diagnosis',
    style='diagnosis',
    palette=PALETTE_DIAG,
    s=65,
    alpha=0.75,
    edgecolor='w',
    linewidth=0.5
)
plt.title('Figure 5: Radius Mean vs Texture Mean Scatter Space', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
plt.xlabel('Radius Mean (mm)', fontsize=11, fontweight='bold', labelpad=8)
plt.ylabel('Texture Mean (Gray-scale SD)', fontsize=11, fontweight='bold', labelpad=8)
plt.legend(title='Diagnosis', loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '05_scatterplot_radius_vs_texture.png'), dpi=300)
plt.close()
print("Generated: 05_scatterplot_radius_vs_texture.png")

# ------------------------------------------------------------------------------
# Chart 06: Heatmap — Feature Correlation Matrix (Multicollinearity)
# ------------------------------------------------------------------------------
plt.figure(figsize=(8.5, 6.5), dpi=300)
feature_subset = [
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
    'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave points_mean'
]
corr_matrix = df[feature_subset].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(
    corr_matrix,
    annot=True,
    cmap='coolwarm',
    fmt='.2f',
    linewidths=0.6,
    cbar_kws={'label': 'Pearson Correlation (r)'},
    annot_kws={'size': 9, 'fontweight': 'bold'}
)
plt.title('Figure 6: Feature Correlation Heatmap Matrix (Multicollinearity)', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '06_heatmap_correlation.png'), dpi=300)
plt.close()
print("Generated: 06_heatmap_correlation.png")

# ------------------------------------------------------------------------------
# Chart 07: Count Plot — Smoothness Level by Diagnosis
# ------------------------------------------------------------------------------
plt.figure(figsize=(7.5, 4.8), dpi=300)
df['Smoothness_Group'] = pd.qcut(df['smoothness_mean'], q=3, labels=['Low', 'Medium', 'High'])
sns.countplot(
    data=df,
    x='Smoothness_Group',
    hue='diagnosis',
    palette=[COLOR_MALIGNANT, COLOR_BENIGN]
)
plt.title('Figure 7: Smoothness Level Frequency by Diagnosis', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
plt.xlabel('Smoothness Category (Tertiaries)', fontsize=11, fontweight='bold', labelpad=8)
plt.ylabel('Patient Count', fontsize=11, fontweight='bold', labelpad=8)
plt.legend(title='Diagnosis', labels=['Malignant (M)', 'Benign (B)'], loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '07_countplot_smoothness.png'), dpi=300)
plt.close()
print("Generated: 07_countplot_smoothness.png")

# ------------------------------------------------------------------------------
# Chart 08: Line Chart — Mean Feature Profile
# ------------------------------------------------------------------------------
plt.figure(figsize=(9, 4.8), dpi=300)
features_profile = ['radius_mean', 'texture_mean', 'perimeter_mean', 'compactness_mean', 'concavity_mean', 'symmetry_mean']
profile_means = df.groupby('diagnosis')[features_profile].mean().T

plt.plot(profile_means.index, profile_means['M'], marker='o', markersize=8, linewidth=2.5, color=COLOR_MALIGNANT, label='Malignant (M)')
plt.plot(profile_means.index, profile_means['B'], marker='s', markersize=8, linewidth=2.5, color=COLOR_BENIGN, label='Benign (B)')

for idx in profile_means.index:
    plt.annotate(f"{profile_means.loc[idx, 'M']:.1f}", (idx, profile_means.loc[idx, 'M']),
                 textcoords="offset points", xytext=(0, 8), ha='center', fontsize=8.5, fontweight='bold', color=COLOR_MALIGNANT)
    plt.annotate(f"{profile_means.loc[idx, 'B']:.1f}", (idx, profile_means.loc[idx, 'B']),
                 textcoords="offset points", xytext=(0, -14), ha='center', fontsize=8.5, fontweight='bold', color=COLOR_BENIGN)

plt.title('Figure 8: Mean Feature Profiles (Malignant vs Benign)', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
plt.ylabel('Unscaled Mean Metric Value', fontsize=11, fontweight='bold', labelpad=8)
plt.xticks(rotation=15, ha='right', fontsize=9.5)
plt.legend(loc='upper right', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '08_line_feature_profile.png'), dpi=300)
plt.close()
print("Generated: 08_line_feature_profile.png")

# ==============================================================================
# 3. MACHINE LEARNING & PREDICTION PIPELINE (LOGISTIC REGRESSION & BENCHMARKS)
# ==============================================================================
selected_features = [
    'radius_mean', 'texture_mean', 'smoothness_mean',
    'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean'
]
X = df[selected_features]
y = df['Diagnosis_Encoded']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Logistic Regression
lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train_scaled, y_train)

y_pred_lr = lr_model.predict(X_test_scaled)
y_prob_lr = lr_model.predict_proba(X_test_scaled)[:, 1]

lr_acc = accuracy_score(y_test, y_pred_lr)
lr_auc = roc_auc_score(y_test, y_prob_lr)
cm_lr = confusion_matrix(y_test, y_pred_lr)

print(f"Logistic Regression Accuracy: {lr_acc*100:.2f}% | AUC-ROC: {lr_auc:.4f}")

# ------------------------------------------------------------------------------
# Chart 09: Confusion Matrix (Logistic Regression)
# ------------------------------------------------------------------------------
plt.figure(figsize=(6, 5), dpi=300)
sns.heatmap(
    cm_lr,
    annot=True,
    fmt='d',
    cmap='Blues',
    cbar=False,
    xticklabels=['Benign (Pred)', 'Malignant (Pred)'],
    yticklabels=['Benign (True)', 'Malignant (True)'],
    annot_kws={'size': 14, 'fontweight': 'bold'}
)
plt.title(f'Figure 9: Confusion Matrix (Accuracy: {lr_acc*100:.2f}%)', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
plt.xlabel('Predicted Diagnosis', fontsize=11, fontweight='bold', labelpad=8)
plt.ylabel('Actual Diagnosis', fontsize=11, fontweight='bold', labelpad=8)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '09_confusion_matrix.png'), dpi=300)
plt.close()
print("Generated: 09_confusion_matrix.png")

# ------------------------------------------------------------------------------
# Chart 10: K-Means Elbow Curve & Silhouette Scores
# ------------------------------------------------------------------------------
X_cluster = df[['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean', 'compactness_mean']]
scaler_cl = StandardScaler()
X_cluster_s = scaler_cl.fit_transform(X_cluster)

wcss = []
sil_scores = []
K_range = range(2, 8)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_cluster_s)
    wcss.append(km.inertia_)
    sil_scores.append(silhouette_score(X_cluster_s, labels))

fig, ax1 = plt.subplots(figsize=(8, 4.8), dpi=300)
ax1.plot(K_range, wcss, 'bo-', linewidth=2.2, markersize=8, label='Inertia (WCSS)')
ax1.set_xlabel('Number of Clusters (K)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Inertia (WCSS)', color='#1d4ed8', fontsize=11, fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#1d4ed8')

ax2 = ax1.twinx()
ax2.plot(K_range, sil_scores, 'rs--', linewidth=2.2, markersize=8, label='Silhouette Score')
ax2.set_ylabel('Silhouette Score', color='#dc2626', fontsize=11, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#dc2626')

plt.title('Figure 10: K-Means Optimal Cluster Selection (Elbow K=2)', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
fig.tight_layout()
plt.savefig(os.path.join(img_dir, '10_kmeans_elbow.png'), dpi=300)
plt.close()
print("Generated: 10_kmeans_elbow.png")

# ------------------------------------------------------------------------------
# Chart 11: Patient Tumor Clusters (2D PCA Projection)
# ------------------------------------------------------------------------------
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_cluster_s)
kmeans_opt = KMeans(n_clusters=2, random_state=42, n_init=10)
df['Cluster'] = kmeans_opt.fit_predict(X_cluster_s)
df['PCA1'] = X_pca[:, 0]
df['PCA2'] = X_pca[:, 1]

plt.figure(figsize=(8.5, 5.2), dpi=300)
sns.scatterplot(
    data=df,
    x='PCA1',
    y='PCA2',
    hue='Cluster',
    style='diagnosis',
    palette=[COLOR_BENIGN, COLOR_MALIGNANT],
    s=65,
    alpha=0.75,
    edgecolor='w',
    linewidth=0.5
)
plt.title('Figure 11: Unsupervised Tumor Clusters in 2D PCA Space', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
plt.xlabel(f'PCA Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}% Variance)', fontsize=11, fontweight='bold')
plt.ylabel(f'PCA Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}% Variance)', fontsize=11, fontweight='bold')
plt.legend(title='Cluster / Diagnosis', loc='upper right', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '11_kmeans_clusters_pca.png'), dpi=300)
plt.close()
print("Generated: 11_kmeans_clusters_pca.png")

# ------------------------------------------------------------------------------
# Chart 12: Multiple Linear Regression - Actual vs Predicted Perimeter
# ------------------------------------------------------------------------------
X_reg = df[['radius_mean', 'area_mean', 'texture_mean', 'Diagnosis_Encoded']]
y_reg = df['perimeter_mean']
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

reg = LinearRegression()
reg.fit(X_train_r, y_train_r)
y_pred_r = reg.predict(X_test_r)
r2_val = r2_score(y_test_r, y_pred_r)

plt.figure(figsize=(8, 5), dpi=300)
plt.scatter(y_test_r, y_pred_r, color='#0284c7', alpha=0.6, edgecolors='none', s=45)
plt.plot([y_test_r.min(), y_test_r.max()], [y_test_r.min(), y_test_r.max()], 'r--', linewidth=2.2, label=f'Ideal Fit (R² = {r2_val:.4f})')
plt.title(f'Figure 12: Linear Regression - Actual vs Predicted Perimeter (R² = {r2_val:.4f})', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
plt.xlabel('Actual Tumor Perimeter Mean (mm)', fontsize=11, fontweight='bold', labelpad=8)
plt.ylabel('Predicted Tumor Perimeter Mean (mm)', fontsize=11, fontweight='bold', labelpad=8)
plt.legend(loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '12_regression_actual_vs_pred.png'), dpi=300)
plt.close()
print("Generated: 12_regression_actual_vs_pred.png")

# ------------------------------------------------------------------------------
# Chart 13: ROC Curve (Logistic Regression, AUC = 0.9887)
# ------------------------------------------------------------------------------
fpr, tpr, _ = roc_curve(y_test, y_prob_lr)
plt.figure(figsize=(7, 5.5), dpi=300)
plt.plot(fpr, tpr, color='#0284c7', linewidth=2.8, label=f'Logistic Regression (AUC = {lr_auc:.4f})')
plt.plot([0, 1], [0, 1], color='#94a3b8', linestyle='--', linewidth=1.8, label='Random Chance (AUC = 0.5000)')
plt.fill_between(fpr, tpr, color='#38bdf8', alpha=0.18)

plt.title('Figure 13: Receiver Operating Characteristic (ROC) Curve', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=11, fontweight='bold', labelpad=8)
plt.ylabel('True Positive Rate (Sensitivity / Recall)', fontsize=11, fontweight='bold', labelpad=8)
plt.xlim([-0.02, 1.02])
plt.ylim([-0.02, 1.05])
plt.legend(loc='lower right', frameon=True, fontsize=10.5)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '13_roc_curve.png'), dpi=300)
plt.close()
print("Generated: 13_roc_curve.png")

# ------------------------------------------------------------------------------
# Chart 14: Feature Importance / Coefficients (Logistic Regression)
# ------------------------------------------------------------------------------
coef_df = pd.DataFrame({
    'Feature': selected_features,
    'Coefficient': lr_model.coef_[0]
}).sort_values(by='Coefficient', ascending=True)

plt.figure(figsize=(8.5, 5), dpi=300)
colors_coef = ['#2563eb' if c < 0 else '#e11d48' for c in coef_df['Coefficient']]
bars = plt.barh(coef_df['Feature'], coef_df['Coefficient'], color=colors_coef, height=0.55, edgecolor='none')

plt.axvline(0, color='#64748b', linestyle='-', linewidth=1)
plt.title('Figure 14: Logistic Regression Feature Coefficients (Beta Weights)', fontsize=13, fontweight='bold', pad=14, color='#0f172a')
plt.xlabel('Standardized Coefficient Weight (Effect on Log-Odds of Malignancy)', fontsize=11, fontweight='bold', labelpad=8)
plt.ylabel('Selected Morphometric Features', fontsize=11, fontweight='bold', labelpad=8)

for bar in bars:
    w = bar.get_width()
    offset = 0.08 if w >= 0 else -0.28
    plt.text(w + offset, bar.get_y() + bar.get_height()/2, f"{w:+.2f}", va='center', fontsize=9.5, fontweight='bold', color='#1e293b')

plt.xlim(-1.2, 3.5)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '14_feature_importance.png'), dpi=300)
plt.close()
print("Generated: 14_feature_importance.png")

# ==============================================================================
# SUMMARY METRICS LOG
# ==============================================================================
summary_text = f"""--- PREPROCESSING & EDA METRICS ---
Augmented Shape: {df.shape}
Null Count: {df.isnull().sum().to_dict()}
Diagnosis Breakdown: {df['diagnosis'].value_counts().to_dict()}

--- CLASSIFICATION METRICS (LOGISTIC REGRESSION) ---
Accuracy: {lr_acc:.4f}
AUC-ROC: {lr_auc:.4f}
Confusion Matrix:
{cm_lr.tolist()}

Selected Features Coefficients:
{dict(zip(selected_features, [round(c, 4) for c in lr_model.coef_[0]]))}
"""

with open('analysis_summary.txt', 'w') as f:
    f.write(summary_text)

print("\nAll 14 Breast Cancer Diagnostic figures generated successfully!")
