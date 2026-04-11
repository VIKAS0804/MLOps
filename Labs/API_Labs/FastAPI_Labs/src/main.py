from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .data import build_sample_payloads
from .predict import get_model_info, load_model, predict_data


app = FastAPI(
    title="Wine Classification API",
    version="1.0.0",
    description=(
        "A custom FastAPI lab project that predicts the wine cultivar from "
        "chemical measurements."
    ),
)


class WineFeatures(BaseModel):
    alcohol: float
    malic_acid: float
    ash: float
    alcalinity_of_ash: float
    magnesium: float
    total_phenols: float
    flavanoids: float
    nonflavanoid_phenols: float
    proanthocyanins: float
    color_intensity: float
    hue: float
    od280_od315_of_diluted_wines: float
    proline: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "alcohol": 14.23,
                "malic_acid": 1.71,
                "ash": 2.43,
                "alcalinity_of_ash": 15.6,
                "magnesium": 127.0,
                "total_phenols": 2.8,
                "flavanoids": 3.06,
                "nonflavanoid_phenols": 0.28,
                "proanthocyanins": 2.29,
                "color_intensity": 5.64,
                "hue": 1.04,
                "od280_od315_of_diluted_wines": 3.92,
                "proline": 1065.0,
            }
        }
    )


class PredictionResponse(BaseModel):
    predicted_class_id: int
    predicted_class_name: str
    class_probabilities: dict[str, float]


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {
        "message": "Wine Classification API is running.",
        "docs_url": "/docs",
        "prediction_endpoint": "/predict",
    }


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    try:
        load_model()
        return {"status": "healthy", "model_ready": True}
    except FileNotFoundError:
        return {"status": "healthy", "model_ready": False}


@app.get("/model-info", status_code=status.HTTP_200_OK)
async def model_info():
    try:
        return get_model_info()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


@app.get("/sample-payloads", status_code=status.HTTP_200_OK)
async def sample_payloads():
    return build_sample_payloads()


@app.post("/predict", response_model=PredictionResponse)
async def predict_wine(features: WineFeatures):
    try:
        payload = [[
            features.alcohol,
            features.malic_acid,
            features.ash,
            features.alcalinity_of_ash,
            features.magnesium,
            features.total_phenols,
            features.flavanoids,
            features.nonflavanoid_phenols,
            features.proanthocyanins,
            features.color_intensity,
            features.hue,
            features.od280_od315_of_diluted_wines,
            features.proline,
        ]]

        prediction = predict_data(payload)
        return PredictionResponse(**prediction)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {exc}",
        ) from exc
