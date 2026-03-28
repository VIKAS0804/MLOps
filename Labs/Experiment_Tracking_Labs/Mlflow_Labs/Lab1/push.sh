#!/bin/bash
set -e
cd /Users/vikasneriyanuru/Desktop/Mlops/MLOps

git stash
git pull origin main --rebase
git stash pop
git add -A
git commit -m "Lab5: Add GitHub Actions workflow for MLflow heart disease experiment" || echo "Nothing new to commit"
git push origin main

echo ""
echo "✅ All pushed! Check actions at:"
echo "https://github.com/VIKAS0804/MLOps/actions"
