"""
MLflow Experiment Tracking - Modified Lab
Original: Wine Quality Prediction with ElasticNet (regression)
Modified by: Vikas Neriyanuru

Changes made vs original:
  - Dataset: UCI Heart Disease (local CSV, no network needed) instead of Wine Quality
  - Task: Binary classification instead of regression
  - Models: Logistic Regression + Random Forest + Gradient Boosting (param sweep)
  - Metrics: Accuracy, F1, ROC-AUC instead of RMSE/MAE/R2
  - Artifacts: Confusion matrix PNG + Feature importance PNG logged per run
  - Multi-run parameter sweep across 9 total configurations
"""

import os
import tempfile
import warnings
import logging
import itertools

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    confusion_matrix, ConfusionMatrixDisplay,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


# ── Data Loading ──────────────────────────────────────────────────────────────

def load_heart_disease_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path   = os.path.join(script_dir, "data", "heart_disease.csv")
    df = pd.read_csv(csv_path)
    df["target"] = (df["target"] > 0).astype(int)
    return df


# ── Metrics ───────────────────────────────────────────────────────────────────

def eval_metrics(y_true, y_pred, y_prob):
    acc = accuracy_score(y_true, y_pred)
    f1  = f1_score(y_true, y_pred)
    auc = roc_auc_score(y_true, y_prob)
    return acc, f1, auc


# ── Artifact helpers ──────────────────────────────────────────────────────────

def save_confusion_matrix(y_true, y_pred, run_name: str, tmp_dir: str) -> str:
    cm   = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=["No Disease", "Disease"])
    fig, ax = plt.subplots(figsize=(5, 4))
    disp.plot(ax=ax, colorbar=False)
    ax.set_title(f"Confusion Matrix - {run_name}")
    fname = f"confusion_matrix_{run_name.replace(' ', '_').replace('=', '_')}.png"
    path  = os.path.join(tmp_dir, fname)
    fig.savefig(path, bbox_inches="tight", dpi=120)
    plt.close(fig)
    return path


def save_feature_importance(model, feature_names: list, run_name: str, tmp_dir: str):
    if not hasattr(model, "feature_importances_"):
        return None
    importances = model.feature_importances_
    indices     = np.argsort(importances)[::-1]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(range(len(importances)), importances[indices])
    ax.set_xticks(range(len(importances)))
    ax.set_xticklabels([feature_names[i] for i in indices], rotation=45, ha="right")
    ax.set_title(f"Feature Importances - {run_name}")
    ax.set_ylabel("Importance")
    fname = f"feature_importance_{run_name.replace(' ', '_').replace('=', '_')}.png"
    path  = os.path.join(tmp_dir, fname)
    fig.savefig(path, bbox_inches="tight", dpi=120)
    plt.close(fig)
    return path


# ── Single MLflow run ─────────────────────────────────────────────────────────

def run_experiment(model, params: dict, run_name: str,
                   X_train, X_test, y_train, y_test, feature_names):
    with tempfile.TemporaryDirectory() as tmp_dir:
        with mlflow.start_run(run_name=run_name):
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]

            acc, f1, auc = eval_metrics(y_test, y_pred, y_prob)

            mlflow.log_params(params)
            mlflow.log_metric("accuracy", round(acc, 4))
            mlflow.log_metric("f1_score", round(f1,  4))
            mlflow.log_metric("roc_auc",  round(auc, 4))

            print(f"  [{run_name}]  acc={acc:.4f}  f1={f1:.4f}  auc={auc:.4f}")

            cm_path = save_confusion_matrix(y_test, y_pred, run_name, tmp_dir)
            mlflow.log_artifact(cm_path, artifact_path="plots")

            fi_path = save_feature_importance(model, feature_names, run_name, tmp_dir)
            if fi_path:
                mlflow.log_artifact(fi_path, artifact_path="plots")

            signature = infer_signature(X_train, y_pred)
            mlflow.sklearn.log_model(model, "model", signature=signature)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    np.random.seed(42)

    # Set tracking URI to a fresh local path — avoids stale absolute paths in mlflow.db
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mlflow.set_tracking_uri(f"sqlite:///{os.path.join(script_dir, 'mlflow.db')}")

    print("Loading UCI Heart Disease dataset from local CSV...")
    df = load_heart_disease_data()
    print(f"Dataset shape: {df.shape}  |  Disease prevalence: {df['target'].mean():.2%}")

    X = df.drop("target", axis=1).astype(float)
    y = df["target"]
    feature_names = list(X.columns)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    mlflow.set_tracking_uri("mlruns")
    mlflow.set_experiment("heart-disease-classification")

    print("\n-- Logistic Regression sweep --")
    for C in [0.01, 0.1, 1.0, 10.0]:
        model  = LogisticRegression(C=C, max_iter=1000, random_state=42)
        params = {"model": "LogisticRegression", "C": C, "max_iter": 1000}
        run_experiment(model, params, f"LogReg_C={C}",
                       X_train, X_test, y_train, y_test, feature_names)

    print("\n-- Random Forest sweep --")
    for n_est, max_d in itertools.product([50, 100], [3, 5]):
        model  = RandomForestClassifier(n_estimators=n_est, max_depth=max_d, random_state=42)
        params = {"model": "RandomForest", "n_estimators": n_est, "max_depth": max_d}
        run_experiment(model, params, f"RF_n={n_est}_d={max_d}",
                       X_train, X_test, y_train, y_test, feature_names)

    print("\n-- Gradient Boosting --")
    model  = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1,
                                        max_depth=3, random_state=42)
    params = {"model": "GradientBoosting", "n_estimators": 100,
              "learning_rate": 0.1, "max_depth": 3}
    run_experiment(model, params, "GradientBoosting",
                   X_train, X_test, y_train, y_test, feature_names)

    print("\nAll 9 runs complete!")
    print("Launch MLflow UI:  mlflow ui")
    print("Then open:         http://localhost:5000")
