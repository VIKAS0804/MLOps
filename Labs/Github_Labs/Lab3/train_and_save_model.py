import pandas as pd
import joblib
import io
import os
import logging
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris
from google.cloud import storage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def download_data():
    """Download the Iris dataset and return features and labels."""
    logger.info("Downloading Iris dataset...")
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target)
    logger.info(f"Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")
    return X, y


def preprocess_data(X, y):
    """Split data into train and test sets."""
    logger.info("Preprocessing data (80/20 train-test split)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    logger.info(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    return X_train, X_test, y_train, y_test


def train_random_forest(X_train, y_train):
    """Train a Random Forest classifier."""
    logger.info("Training RandomForestClassifier (n_estimators=100)...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    logger.info("RandomForest training complete.")
    return model


def train_gradient_boosting(X_train, y_train):
    """Train a Gradient Boosting classifier."""
    logger.info("Training GradientBoostingClassifier (n_estimators=100)...")
    model = GradientBoostingClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    logger.info("GradientBoosting training complete.")
    return model


def evaluate_model(model, X_test, y_test, model_name):
    """Evaluate a model and log the results."""
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, target_names=["setosa", "versicolor", "virginica"])
    logger.info(f"\n{'='*40}")
    logger.info(f"Model: {model_name}")
    logger.info(f"Accuracy: {accuracy:.4f}")
    logger.info(f"Classification Report:\n{report}")
    logger.info(f"{'='*40}")
    return accuracy


def save_model_to_gcs(model, bucket_name, blob_name):
    """Save model directly to GCS using an in-memory buffer."""
    try:
        logger.info(f"Uploading model to gs://{bucket_name}/{blob_name} ...")
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        buffer = io.BytesIO()
        joblib.dump(model, buffer)
        buffer.seek(0)

        blob.upload_from_file(buffer, content_type='application/octet-stream')
        logger.info(f"✅ Model successfully uploaded to gs://{bucket_name}/{blob_name}")
    except Exception as e:
        logger.error(f"❌ Failed to upload model: {e}")
        raise


def main():
    bucket_name = os.getenv("GCS_BUCKET_NAME", "mlops-lab3-vikas")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Step 1: Load and preprocess data
    X, y = download_data()
    X_train, X_test, y_train, y_test = preprocess_data(X, y)

    # Step 2: Train both models
    rf_model = train_random_forest(X_train, y_train)
    gb_model = train_gradient_boosting(X_train, y_train)

    # Step 3: Evaluate both models
    rf_accuracy = evaluate_model(rf_model, X_test, y_test, "Random Forest")
    gb_accuracy = evaluate_model(gb_model, X_test, y_test, "Gradient Boosting")

    # Step 4: Pick the best model
    if rf_accuracy >= gb_accuracy:
        best_model = rf_model
        best_name = "random_forest"
        logger.info(f"✅ Best model: Random Forest (accuracy={rf_accuracy:.4f})")
    else:
        best_model = gb_model
        best_name = "gradient_boosting"
        logger.info(f"✅ Best model: Gradient Boosting (accuracy={gb_accuracy:.4f})")

    # Step 5: Save best model to GCS
    blob_name = f"trained_models/iris_{best_name}_{timestamp}.joblib"
    save_model_to_gcs(best_model, bucket_name, blob_name)

    logger.info("🎉 Pipeline complete!")


if __name__ == "__main__":
    main()
