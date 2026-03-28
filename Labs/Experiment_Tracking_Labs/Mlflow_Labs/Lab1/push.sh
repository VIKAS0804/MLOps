#!/bin/bash
set -e
cd /Users/vikasneriyanuru/Desktop/Mlops/MLOps

# Switch remote to HTTPS with correct username
git remote set-url origin https://VIKAS0804@github.com/VIKAS0804/MLOps.git

echo "==> Adding files..."
git add Labs/Experiment_Tracking_Labs/Mlflow_Labs/Lab1/
git add .github/workflows/mlflow_heart_disease.yml

echo "==> Committing..."
git commit -m "Lab5: Add GitHub Actions workflow to run MLflow heart disease experiment on push"

echo "==> Pushing..."
git push origin main

echo ""
echo "✅ Done! Submit this link on Canvas:"
echo "https://github.com/VIKAS0804/MLOps/tree/main/Labs/Experiment_Tracking_Labs/Mlflow_Labs/Lab1"
