#!/bin/bash

# Simple Git Commands for Lab Submission
# Copy and paste these commands one by one in your terminal

echo "🔧 Step-by-step Git commands for Terraform Lab submission"
echo ""
echo "Copy and paste these commands in your terminal:"
echo ""
echo "================================================================"
echo "STEP 1: Navigate to MLOps directory"
echo "================================================================"
echo "cd /Users/vikasneriyanuru/Desktop/Mlops/MLOps"
echo ""

echo "================================================================"
echo "STEP 2: Check current status"
echo "================================================================"
echo "git status"
echo ""

echo "================================================================"
echo "STEP 3: Add your Terraform lab files"
echo "================================================================"
echo "git add Labs/Terraform_Labs/AWS/Lab1_Beginner/"
echo ""

echo "================================================================"
echo "STEP 4: Commit with a descriptive message"
echo "================================================================"
cat << 'EOF'
git commit -m "Enhanced Terraform Beginner Lab with comprehensive improvements

- Added variables.tf for configuration management
- Added outputs.tf for resource information display
- Enhanced main.tf with Internet Gateway, Security Group, Routes
- Added user data script for automated Nginx installation
- Created comprehensive README with diagrams and guides
- Added QUICKSTART.md for quick reference
- Implemented security best practices
- Complete documentation for lab submission"
EOF
echo ""

echo "================================================================"
echo "STEP 5: Push to GitHub"
echo "================================================================"
echo "git push origin main"
echo ""
echo "# If the above fails, try:"
echo "git push origin master"
echo ""

echo "================================================================"
echo "STEP 6: Verify on GitHub"
echo "================================================================"
echo "1. Open your browser"
echo "2. Go to your GitHub repository"
echo "3. Navigate to Labs/Terraform_Labs/AWS/Lab1_Beginner"
echo "4. Verify all files are there"
echo "5. Copy the URL for Canvas submission"
echo ""

echo "================================================================"
echo "ALTERNATIVE: All in one command sequence"
echo "================================================================"
cat << 'EOF'
cd /Users/vikasneriyanuru/Desktop/Mlops/MLOps && \
git add Labs/Terraform_Labs/AWS/Lab1_Beginner/ && \
git commit -m "Enhanced Terraform Beginner Lab - MLOps Submission" && \
git push origin main
EOF
echo ""

echo "================================================================"
echo "After pushing, your GitHub URL will be:"
echo "================================================================"
echo "https://github.com/YOUR_USERNAME/MLOps/tree/main/Labs/Terraform_Labs/AWS/Lab1_Beginner"
echo ""
echo "Replace YOUR_USERNAME with your actual GitHub username"
echo "================================================================"
