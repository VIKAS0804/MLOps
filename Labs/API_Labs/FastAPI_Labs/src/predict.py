from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np


ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_DIR / "model" / "wine_classifier.joblib"
METADATA_PATH = ROOT_DIR / "model" / "model_metadata.txt"


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model file not found. Run `python3 -m src.train` before starting the API."
        )

    return joblib.load(MODEL_PATH)


@lru_cache(maxsize=1)
def load_metadata():
    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            "Metadata file not found. Run `python3 -m src.train` before calling this endpoint."
        )

    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def get_model_info():
    return load_metadata()


def predict_data(X):
    """
    Predict the wine class for the provided features and return human-readable
    probabilities for each class.
    """
    model = load_model()
    metadata = load_metadata()

    probabilities = model.predict_proba(X)[0]
    predicted_class_id = int(np.argmax(probabilities))

    return {
        "predicted_class_id": predicted_class_id,
        "predicted_class_name": metadata["class_labels"][predicted_class_id],
        "class_probabilities": {
            class_name: round(float(probability), 6)
            for class_name, probability in zip(metadata["class_labels"], probabilities)
        },
    }
