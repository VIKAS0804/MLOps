# MLflow Experiment Tracking — Heart Disease Classification

**Modified by:** Vikas Neriyanuru
**Original Lab:** `Experiment_Tracking_Labs/Mlflow_Labs/Lab1`
**Original Dataset:** UCI Wine Quality (regression)
**Modified Dataset:** UCI Heart Disease / Cleveland (binary classification)

---

## What Changed from the Original

| | Original | This Version |
|---|---|---|
| Dataset | Wine Quality (red) | UCI Heart Disease (Cleveland) |
| Task | Regression (quality score) | Binary Classification (disease vs. none) |
| Model | Single ElasticNet run | 9 runs: LogReg sweep + RF sweep + GBM |
| Params logged | alpha, l1_ratio | C / n_estimators / max_depth / learning_rate |
| Metrics logged | RMSE, MAE, R² | Accuracy, F1, ROC-AUC |
| Artifacts | None | Confusion matrix PNG + Feature importance PNG per run |
| MLflow UI | Basic | Multi-run comparison across 3 model families |

---

## Dataset

**UCI Heart Disease (Cleveland)**
- 303 patients, 13 clinical features (age, sex, chest pain type, cholesterol, etc.)
- Target: `0` = no heart disease, `1` = heart disease
- Source: https://archive.ics.uci.edu/ml/datasets/heart+disease

---

## Project Structure

```
Lab1/
├── heart_disease_tracking.py   # Main training + MLflow tracking script (modified)
├── linear_regression.py        # Original lab script (unchanged, for reference)
├── requirements.txt            # Updated dependencies
├── screenshots/                # MLflow UI screenshots (see below)
│   ├── experiment_runs.png
│   ├── run_detail_rf.png
│   └── confusion_matrix_artifact.png
├── starter.ipynb               # Original notebook
├── serving.py                  # Original serving script
└── README.md                   # This file
```

---

## How to Re-run This Lab

### 1. Clone the repo

```bash
git clone https://github.com/VIKAS0804/MLOps.git
cd MLOps/Labs/Experiment_Tracking_Labs/Mlflow_Labs/Lab1
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the experiment

```bash
python heart_disease_tracking.py
```

This will:
- Download the UCI Heart Disease dataset automatically
- Run **9 MLflow experiments** across 3 model families:
  - Logistic Regression (4 runs, C ∈ {0.01, 0.1, 1.0, 10.0})
  - Random Forest (4 runs, n_estimators × max_depth grid)
  - Gradient Boosting (1 run)
- Log params, metrics, and artifacts (confusion matrix + feature importance) per run

### 5. Launch the MLflow UI

```bash
mlflow ui
```

Open **http://127.0.0.1:5000** in your browser.

You will see all 9 runs under the `heart-disease-classification` experiment with sortable metrics and downloadable artifact plots.

---

## Sample Output

```
Loading UCI Heart Disease dataset...
Dataset shape: (297, 14)  |  Disease prevalence: 54.55%

── Logistic Regression sweep ──
  [LogReg_C=0.01]  acc=0.8136  f1=0.8197  auc=0.8986
  [LogReg_C=0.1]   acc=0.8305  f1=0.8361  auc=0.9127
  [LogReg_C=1.0]   acc=0.8305  f1=0.8333  auc=0.9104
  [LogReg_C=10.0]  acc=0.8305  f1=0.8333  auc=0.9088

── Random Forest sweep ──
  [RF_n=50_d=3]    acc=0.8475  f1=0.8525  auc=0.9201
  [RF_n=50_d=5]    acc=0.8305  f1=0.8361  auc=0.9143
  [RF_n=100_d=3]   acc=0.8475  f1=0.8525  auc=0.9254
  [RF_n=100_d=5]   acc=0.8475  f1=0.8525  auc=0.9221

── Gradient Boosting ──
  [GradientBoosting]  acc=0.8644  f1=0.8689  auc=0.9337
```

---

## Key MLflow Concepts Demonstrated

- `mlflow.set_experiment()` — group all runs under one experiment
- `mlflow.start_run(run_name=...)` — named runs for easy comparison
- `mlflow.log_params()` — track hyperparameters per run
- `mlflow.log_metric()` — track accuracy, F1, ROC-AUC
- `mlflow.log_artifact()` — store confusion matrix and feature importance plots
- `mlflow.sklearn.log_model()` — save the trained model with input signature
- `infer_signature()` — automatically capture model input/output schema
