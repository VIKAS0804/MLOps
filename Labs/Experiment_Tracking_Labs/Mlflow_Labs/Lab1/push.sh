#!/bin/bash
set -e
cd /Users/vikasneriyanuru/Desktop/Mlops/MLOps

echo "==> Adding files..."
git add Labs/Experiment_Tracking_Labs/Mlflow_Labs/Lab1/

echo "==> Committing..."
git commit -m "Lab5: MLflow experiment tracking - Heart Disease dataset, 9 runs (LogReg sweep + RF sweep + GBM), confusion matrix & feature importance artifacts, local CSV data, custom README"

echo "==> Pushing..."
git push origin main

echo ""
echo "✅ Done! Submit this link on Canvas:"
echo "https://github.com/VIKAS0804/MLOps/tree/main/Labs/Experiment_Tracking_Labs/Mlflow_Labs/Lab1"
