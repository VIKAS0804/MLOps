#!/bin/bash
cd /Users/vikasneriyanuru/Desktop/Mlops/MLOps

echo "==> Current git status..."
git status

echo "==> Pulling latest..."
git fetch origin
git reset --hard origin/main

echo "==> Re-adding fixed file..."
git add Labs/Experiment_Tracking_Labs/Mlflow_Labs/Lab1/heart_disease_tracking.py

echo "==> Committing..."
git commit -m "Lab5: Fix tempfile for cross-platform CI - no hardcoded /tmp paths" || echo "Already committed"

echo "==> Pushing..."
git push origin main

echo ""
echo "✅ Done! Action will auto-trigger."
echo "Watch: https://github.com/VIKAS0804/MLOps/actions"
