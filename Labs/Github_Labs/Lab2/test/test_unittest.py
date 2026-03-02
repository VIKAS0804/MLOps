import os
import sys
import json
import joblib
import unittest
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import f1_score
from sklearn.calibration import CalibratedClassifierCV

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def make_data(n_samples=300):
    return make_classification(
        n_samples=n_samples,
        n_features=6,
        n_informative=3,
        n_redundant=0,
        n_repeated=0,
        n_classes=2,
        random_state=42,
        shuffle=True,
    )


class TestTrainModel(unittest.TestCase):

    def setUp(self):
        self.X, self.y = make_data()
        self.model = RandomForestClassifier(random_state=0)
        self.model.fit(self.X, self.y)

    def test_data_shape(self):
        self.assertEqual(self.X.shape[1], 6)
        self.assertEqual(len(self.X), len(self.y))

    def test_model_trains(self):
        self.assertIsNotNone(self.model)

    def test_predictions_shape(self):
        preds = self.model.predict(self.X)
        self.assertEqual(len(preds), len(self.y))

    def test_predictions_valid_classes(self):
        preds = self.model.predict(self.X)
        self.assertTrue(set(preds).issubset({0, 1}))

    def test_model_save_and_load(self):
        path = '/tmp/test_lab2_model.joblib'
        joblib.dump(self.model, path)
        loaded = joblib.load(path)
        self.assertIsInstance(loaded, RandomForestClassifier)
        os.remove(path)

    def test_loaded_model_predictions_match(self):
        path = '/tmp/test_lab2_model_match.joblib'
        joblib.dump(self.model, path)
        loaded = joblib.load(path)
        np.testing.assert_array_equal(
            self.model.predict(self.X),
            loaded.predict(self.X)
        )
        os.remove(path)


class TestEvaluateModel(unittest.TestCase):

    def setUp(self):
        self.X, self.y = make_data()
        self.model = RandomForestClassifier(random_state=0)
        self.model.fit(self.X, self.y)
        self.y_pred = self.model.predict(self.X)

    def test_f1_score_in_range(self):
        score = f1_score(self.y, self.y_pred)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_metrics_json_serializable(self):
        metrics = {"F1_Score": f1_score(self.y, self.y_pred)}
        parsed = json.loads(json.dumps(metrics))
        self.assertIn("F1_Score", parsed)
        self.assertIsInstance(parsed["F1_Score"], float)

    def test_metrics_directory_creation(self):
        path = '/tmp/test_lab2_metrics'
        os.makedirs(path, exist_ok=True)
        self.assertTrue(os.path.isdir(path))
        os.rmdir(path)


class TestModelCalibration(unittest.TestCase):

    def setUp(self):
        self.X, self.y = make_data(500)

    def test_calibration_sigmoid(self):
        cal = CalibratedClassifierCV(RandomForestClassifier(random_state=0), method='sigmoid', cv=3)
        cal.fit(self.X, self.y)
        probs = cal.predict_proba(self.X)
        self.assertEqual(probs.shape, (len(self.X), 2))

    def test_calibration_isotonic(self):
        cal = CalibratedClassifierCV(RandomForestClassifier(random_state=0), method='isotonic', cv=3)
        cal.fit(self.X, self.y)
        probs = cal.predict_proba(self.X)
        self.assertEqual(probs.shape, (len(self.X), 2))

    def test_probabilities_sum_to_one(self):
        cal = CalibratedClassifierCV(RandomForestClassifier(random_state=0), method='sigmoid', cv=3)
        cal.fit(self.X, self.y)
        probs = cal.predict_proba(self.X)
        np.testing.assert_array_almost_equal(probs.sum(axis=1), 1.0)

    def test_calibrated_predictions_valid(self):
        cal = CalibratedClassifierCV(RandomForestClassifier(random_state=0), method='sigmoid', cv=3)
        cal.fit(self.X, self.y)
        preds = cal.predict(self.X)
        self.assertTrue(set(preds).issubset({0, 1}))


if __name__ == '__main__':
    unittest.main()
