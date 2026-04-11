from __future__ import annotations

from pathlib import Path
import sys

from fastapi.testclient import TestClient


LAB_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = LAB_ROOT / "src"

if str(LAB_ROOT) not in sys.path:
    sys.path.insert(0, str(LAB_ROOT))

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


from src.data import build_sample_payloads  # noqa: E402
from src.main import app  # noqa: E402
from src.train import MODEL_PATH, METADATA_PATH, train_model  # noqa: E402


def ensure_model_artifacts():
    if not MODEL_PATH.exists() or not METADATA_PATH.exists():
        train_model()


ensure_model_artifacts()
client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Wine Classification API is running."
    assert payload["prediction_endpoint"] == "/predict"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "healthy"
    assert payload["model_ready"] is True


def test_model_info_endpoint():
    response = client.get("/model-info")

    assert response.status_code == 200
    payload = response.json()
    assert payload["dataset_name"] == "wine_recognition"
    assert payload["model_name"] == "standard_scaler_logistic_regression"
    assert len(payload["feature_names"]) == 13
    assert len(payload["class_labels"]) == 3


def test_sample_payloads_endpoint():
    response = client.get("/sample-payloads")

    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == {"class_0", "class_1", "class_2"}


def test_predict_endpoint_returns_probabilities():
    sample_payload = build_sample_payloads()["class_0"]

    response = client.post("/predict", json=sample_payload)

    assert response.status_code == 200
    payload = response.json()
    assert payload["predicted_class_name"] in {"class_0", "class_1", "class_2"}
    assert set(payload["class_probabilities"].keys()) == {"class_0", "class_1", "class_2"}
    assert abs(sum(payload["class_probabilities"].values()) - 1.0) < 1e-4


def test_predict_endpoint_validates_missing_fields():
    response = client.post("/predict", json={"alcohol": 13.5})

    assert response.status_code == 422
