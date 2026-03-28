import mlflow
import datetime
import os
import pickle
import random
from joblib import dump
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, f1_score
from sklearn.ensemble import RandomForestClassifier
import argparse
import sys

sys.path.insert(0, os.path.abspath('..'))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", type=str, required=True)
    args = parser.parse_args()
    timestamp = args.timestamp

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

    os.makedirs('data/', exist_ok=True)
    with open('data/data.pickle', 'wb') as f:
        pickle.dump(X, f)
    with open('data/target.pickle', 'wb') as f:
        pickle.dump(y, f)

    mlflow.set_tracking_uri("./mlruns")
    dataset_name = "Reuters Corpus Volume"
    current_time = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    experiment_id = mlflow.create_experiment(f"{dataset_name}_{current_time}")
~
    with mlflow.start_run(experiment_id=experiment_id, run_name=dataset_name):
        mlflow.log_params({
            "dataset_name": dataset_name,
            "number of datapoints": X.shape[0],
            "number of dimensions": X.shape[1],
        })

        model = RandomForestClassifier(random_state=0)
        model.fit(X, y)
        y_pred = model.predict(X)

        mlflow.log_metrics({
            'Accuracy': accuracy_score(y, y_pred),
            'F1 Score': f1_score(y, y_pred),
        })

        os.makedirs('models/', exist_ok=True)
        model_filename = f'model_{timestamp}_dt_model.joblib'
        dump(model, model_filename)
