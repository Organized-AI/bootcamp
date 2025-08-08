#!/bin/bash

# GitHub Repository Setup Script for VibeCoders Bootcamp
# Organization: Organized-AI

echo "======================================"
echo "GitHub Repository Setup for VibeCoders"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Repository details
REPO_NAME="bootcamp"
ORG_NAME="organized-ai"
REPO_URL="https://github.com/${ORG_NAME}/${REPO_NAME}"

echo ""
echo -e "${YELLOW}📋 Step 1: Create the repository on GitHub${NC}"
echo "----------------------------------------"
echo "1. Go to: https://github.com/organizations/organized-ai/repositories/new"
echo "2. Repository name: bootcamp"
echo "3. Description: VibeCoders Bootcamp - 6-Week Engineering Principles for AI-Assisted Development"
echo "4. Set to Public or Private (your choice)"
echo "5. DO NOT initialize with README (we already have one)"
echo "6. Click 'Create repository'"
echo ""
read -p "Press Enter when you've created the repository..."

echo ""
echo -e "${YELLOW}📤 Step 2: Pushing code to GitHub${NC}"
echo "----------------------------------------"

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d ".git" ]; then
    echo -e "${RED}❌ Error: Not in the vibecoder-bootcamp directory${NC}"
    echo "Please run this script from the project root"
    exit 1
fi

# Add remote if not exists
echo "Adding GitHub remote..."
git remote remove origin 2>/dev/null
git remote add origin ${REPO_URL}

# Create and switch to main branch
echo "Setting up main branch..."
git branch -M main

# Push to GitHub
echo ""
echo -e "${GREEN}🚀 Pushing to GitHub...${NC}"
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
    echo "Repository URL: ${REPO_URL}"
    echo ""
    echo "Next steps:"
    echo "1. Add collaborators: ${REPO_URL}/settings/access"
    echo "2. Set up branch protection: ${REPO_URL}/settings/branches"
    echo "3. Configure GitHub Pages: ${REPO_URL}/settings/pages"
    echo "4. Add topics: 'bootcamp', 'education', 'ai-development', 'vibecoding'"
else
    echo ""
    echo -e "${RED}❌ Push failed. Common issues:${NC}"
    echo "1. Repository doesn't exist on GitHub yet"
    echo "2. Authentication issues - you may need to:"
    echo "   - Set up SSH keys: https://github.com/settings/keys"
    echo "   - Or use GitHub CLI: gh auth login"
    echo "   - Or use Personal Access Token"
    echo ""
    echo "To manually push:"
    echo "git remote add origin ${REPO_URL}"
    echo "git branch -M main"
    echo "git push -u origin main"
fi

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================" 