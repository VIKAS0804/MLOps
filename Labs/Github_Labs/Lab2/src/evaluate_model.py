import os
import json
import random
import argparse
import sys
import joblib
from sklearn.datasets import make_classification
from sklearn.metrics import f1_score

sys.path.insert(0, os.path.abspath('..'))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", type=str, required=True)
    args = parser.parse_args()
    timestamp = args.timestamp

    model_path = f'model_{timestamp}_dt_model.joblib'
    if not os.path.exists(model_path):
        raise FileNotFoundError(f'Model file not found: {model_path}')
    model = joblib.load(model_path)

    X, y = make_classification(
        n_samples=random.randint(100, 2000),
        n_features=6,
        n_informative=3,
        n_redundant=0,
        n_repeated=0,
        n_classes=2,
        random_state=0,
        shuffle=True,
    )

    y_pred = model.predict(X)
    metrics = {"F1_Score": f1_score(y, y_pred)}

    os.makedirs('metrics/', exist_ok=True)
    with open(f'{timestamp}_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
