# Lab Assignment 6: Wine Classification API with FastAPI

Prepared by: Vikas Neriyanuru

## Overview

For this lab submission, I built a FastAPI application that predicts the wine
cultivar from 13 chemical measurements using the Wine Recognition dataset from
`scikit-learn`.

## How my version is different

- Replaced the original dataset with the Wine Recognition dataset
- Replaced the original model with a `StandardScaler + LogisticRegression` pipeline
- Added a `/model-info` endpoint to show the saved model metadata and evaluation metrics
- Added a `/sample-payloads` endpoint to make testing easier
- Updated the prediction response to include both the predicted class name and class probabilities
- Added automated API tests using `pytest`
- Wrote a new README with my own setup, rerun steps, and sample API call

## Project structure

```text
FastAPI_Labs/
├── model/
├── src/
│   ├── __init__.py
│   ├── data.py
│   ├── main.py
│   ├── predict.py
│   └── train.py
├── tests/
│   └── test_api.py
├── README.md
└── requirements.txt
```

## How to rerun the lab

1. Move into the lab folder:

```bash
cd Labs/API_Labs/FastAPI_Labs
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Train the model and save the artifacts:

```bash
python3 -m src.train
```

5. Start the FastAPI application:

```bash
uvicorn src.main:app --reload
```

6. Open the Swagger UI in your browser:

```text
http://127.0.0.1:8000/docs
```

## Available endpoints

- `GET /` returns a basic status message and quick links
- `GET /health` checks if the API is running and whether the model artifact exists
- `GET /model-info` returns model metadata, feature names, class labels, and evaluation metrics
- `GET /sample-payloads` returns sample JSON payloads for each wine class
- `POST /predict` predicts the wine class from the request body

## Example request

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
    "proline": 1065.0
  }'
```

## Example response

```json
{
  "predicted_class_id": 0,
  "predicted_class_name": "class_0",
  "class_probabilities": {
    "class_0": 0.999591,
    "class_1": 0.000377,
    "class_2": 0.000031
  }
}
```

## Latest training result

After running `python3 -m src.train`, the saved metadata reported:

- Test accuracy: `1.0`
- Test macro F1 score: `1.0`
- Training rows: `133`
- Test rows: `45`

## Running the tests

```bash
python3 -m pytest tests/test_api.py -v
```

## Notes for submission

- This lab is from the `API_Labs` folder, which is different from the folders I used in earlier submissions
- The dataset and model are different from the original repo version
- The README is fully customized for my version of the lab
