from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .data import load_data, split_data


ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT_DIR / "model"
MODEL_PATH = MODEL_DIR / "wine_classifier.joblib"
METADATA_PATH = MODEL_DIR / "model_metadata.txt"


def train_model():
    """
    Train a Logistic Regression pipeline on the Wine Recognition dataset, then save
    the fitted model and training metadata.
    """
    X, y, feature_names, target_names = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)

    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=2000, solver="lbfgs")),
        ]
    )
    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    macro_f1 = f1_score(y_test, predictions, average="macro")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    metadata = {
        "dataset_name": "wine_recognition",
        "model_name": "standard_scaler_logistic_regression",
        "train_size": len(X_train),
        "test_size": len(X_test),
        "feature_names": feature_names,
        "class_labels": target_names,
        "test_accuracy": round(float(accuracy), 4),
        "test_macro_f1": round(float(macro_f1), 4),
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return metadata


if __name__ == "__main__":
    print(json.dumps(train_model(), indent=2))
