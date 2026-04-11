from __future__ import annotations

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split


def _normalize_feature_name(name: str) -> str:
    return name.replace("/", "_")


def load_data():
    """
    Load the Wine Recognition dataset and return the features, labels, feature names,
    and target names.
    """
    wine = load_wine()
    feature_names = [_normalize_feature_name(name) for name in wine.feature_names]
    return wine.data, wine.target, feature_names, list(wine.target_names)


def split_data(X, y, test_size: float = 0.25, random_state: int = 42):
    """
    Split the dataset into train and test partitions using stratification so that
    each wine class is represented in both splits.
    """
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )


def build_sample_payloads():
    """
    Build one sample payload per wine class for API documentation and testing.
    """
    X, y, feature_names, target_names = load_data()
    samples = {}

    for class_id, class_name in enumerate(target_names):
        sample_index = next(index for index, label in enumerate(y) if label == class_id)
        samples[class_name] = {
            feature_name: float(value)
            for feature_name, value in zip(feature_names, X[sample_index])
        }

    return samples
