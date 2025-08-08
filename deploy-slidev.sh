#!/bin/bash

# SliDev Deployment Script for GitHub Pages
# Deploys the presentation to https://organized-ai.github.io/bootcamp/

echo "========================================="
echo "SliDev Presentation Deployment"
echo "========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed. Please install Node.js first.${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Installing dependencies...${NC}"
npm install

echo -e "${BLUE}🔨 Building SliDev presentation...${NC}"
npm run slides:build -- --base /bootcamp/

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Build successful!${NC}"

# Create a temporary directory for gh-pages
echo -e "${YELLOW}📤 Preparing for deployment...${NC}"

# Check if we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${YELLOW}⚠️  Not on main branch. Switching to main...${NC}"
    git checkout main
fi

# Stash any uncommitted changes
git stash

# Create or switch to gh-pages branch
if git show-ref --verify --quiet refs/heads/gh-pages; then
    echo "Switching to existing gh-pages branch..."
    git checkout gh-pages
    git pull origin gh-pages
else
    echo "Creating new gh-pages branch..."
    git checkout -b gh-pages
fi

# Copy the built files
echo -e "${BLUE}📁 Copying built files...${NC}"
cp -r dist/* .

# Add and commit
git add .
git commit -m "Deploy SliDev presentation - $(date '+%Y-%m-%d %H:%M:%S')"

# Push to GitHub
echo -e "${YELLOW}🚀 Deploying to GitHub Pages...${NC}"
git push origin gh-pages

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    echo ""
    echo "Your presentation will be available at:"
    echo -e "${BLUE}https://organized-ai.github.io/bootcamp/${NC}"
    echo ""
    echo "Note: It may take a few minutes for GitHub Pages to update."
    echo ""
    echo "To view locally:"
    echo "  npm run slides:dev"
    echo ""
    echo "To export as PDF:"
    echo "  npm run slides:export"
else
    echo -e "${RED}❌ Deployment failed!${NC}"
    echo "Please check your GitHub credentials and try again."
fi

# Switch back to main branch
git checkout main
git stash pop 2>/dev/null

echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
