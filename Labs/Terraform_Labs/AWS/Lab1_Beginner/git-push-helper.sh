#!/bin/bash

# Git Push Script for Terraform Lab Submission
# This script helps commit and push your enhanced Terraform lab to GitHub

echo "========================================="
echo "Terraform Lab - Git Push Helper"
echo "========================================="
echo ""

# Navigate to the MLOps directory
cd /Users/vikasneriyanuru/Desktop/Mlops/MLOps

echo "Current directory: $(pwd)"
echo ""

# Check git status
echo "📊 Checking git status..."
git status
echo ""

# Add the Terraform lab files
echo "➕ Adding Terraform Lab files..."
git add Labs/Terraform_Labs/AWS/Lab1_Beginner/

echo ""
echo "📝 Files to be committed:"
git status --short Labs/Terraform_Labs/AWS/Lab1_Beginner/
echo ""

# Create commit message
COMMIT_MSG="Enhanced Terraform Beginner Lab with variables, outputs, and security

Changes:
- Added variables.tf for centralized configuration management
- Added outputs.tf to display resource information after deployment
- Enhanced main.tf with:
  * Internet Gateway for public internet access
  * Route table and associations
  * Security group with SSH, HTTP, HTTPS access
  * User data script to auto-install and configure Nginx web server
- Added comprehensive README.md with:
  * Step-by-step setup instructions
  * Architecture diagram
  * Troubleshooting guide
  * Best practices
- Added QUICKSTART.md for quick reference
- Added .gitignore for Terraform-specific files

Improvements:
- Proper network architecture (VPC, IGW, Subnet, Routes)
- Security best practices with security groups
- Automated web server setup with user data
- Resource tagging for better management
- Modular and reusable configuration
- Complete documentation

This is an enhanced version created for MLOps lab submission."

# Show the commit message
echo "📄 Commit message:"
echo "---"
echo "$COMMIT_MSG"
echo "---"
echo ""

# Ask for confirmation
read -p "Do you want to commit these changes? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Commit changes
    echo "✅ Committing changes..."
    git commit -m "$COMMIT_MSG"
    echo ""
    
    # Push to GitHub
    echo "🚀 Ready to push to GitHub"
    echo ""
    read -p "Do you want to push to GitHub now? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "📤 Pushing to GitHub..."
        git push origin main || git push origin master
        echo ""
        echo "✅ Successfully pushed to GitHub!"
        echo ""
        echo "📋 Next steps:"
        echo "1. Go to your GitHub repository"
        echo "2. Copy the repository URL"
        echo "3. Submit the URL in Canvas"
        echo ""
        echo "Your GitHub URL should be something like:"
        echo "https://github.com/YOUR_USERNAME/MLOps"
        echo "or more specifically:"
        echo "https://github.com/YOUR_USERNAME/MLOps/tree/main/Labs/Terraform_Labs/AWS/Lab1_Beginner"
    else
        echo "⏸️  Push cancelled. You can push later with: git push"
    fi
else
    echo "⏸️  Commit cancelled. No changes made."
fi

echo ""
echo "========================================="
echo "Script completed!"
echo "========================================="
