#!/bin/bash

# Quick GitHub Deployment Setup
# This helps you push to GitHub and deploy

echo "🚀 GitHub Deployment Setup"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    git branch -M main
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Commit
echo "💾 Creating commit..."
read -p "Enter commit message (or press Enter for default): " commit_msg
commit_msg=${commit_msg:-"Update: Ready for deployment"}
git commit -m "$commit_msg"

# Check if remote exists
if ! git remote | grep -q origin; then
    echo ""
    echo "🔗 No remote repository found."
    echo ""
    echo "Steps to create GitHub repo:"
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository (don't initialize with README)"
    echo "3. Copy the repository URL"
    echo ""
    read -p "Enter your GitHub repository URL: " repo_url
    git remote add origin "$repo_url"
fi

# Push to GitHub
echo ""
echo "⬆️  Pushing to GitHub..."
git push -u origin main

echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ Code pushed to GitHub!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "🎯 Next Steps - Choose one:"
echo ""
echo "Option 1: Deploy to Render.com (FREE, EASIEST)"
echo "  1. Go to https://render.com"
echo "  2. Sign in with GitHub"
echo "  3. New + → Web Service"
echo "  4. Connect your repository"
echo "  5. Click 'Create Web Service'"
echo "  6. Done! You'll get a URL in 2 minutes"
echo ""
echo "Option 2: Deploy to Railway.app (\$5/month)"
echo "  1. Go to https://railway.app"
echo "  2. Sign in with GitHub"
echo "  3. New Project → Deploy from GitHub"
echo "  4. Select your repo"
echo "  5. Done! Always-on deployment"
echo ""
echo "════════════════════════════════════════════════════════"
