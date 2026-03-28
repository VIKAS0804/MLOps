#!/bin/bash
# Kill anything running on port 5000
lsof -ti:5000 | xargs kill -9 2>/dev/null
sleep 1
# Start MLflow UI with allowed hosts
cd /Users/vikasneriyanuru/Desktop/Mlops/MLOps/Labs/Experiment_Tracking_Labs/Mlflow_Labs/Lab1
mlflow ui --allowed-hosts localhost,127.0.0.1 --port 5000
