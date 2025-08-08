#!/bin/bash

# Week 1 Sandbox Exercise: The Clean Machine
# Developer Hygiene & Environment Setup
# 
# Mission: Set up a complete, professional development environment
# Time Limit: 90 minutes
# Attempts: Unlimited (Work it until you solve it!)

echo "================================================"
echo "VIBECODER BOOTCAMP - WEEK 1 SANDBOX EXERCISE"
echo "The Clean Machine: Developer Environment Setup"
echo "================================================"
echo ""
echo "Your mission: Create a pristine development environment"
echo ""

# Check current environment
check_environment() {
    echo "📋 Checking current environment..."
    echo ""
    
    # Check Docker
    if command -v docker &> /dev/null; then
        echo "✅ Docker installed: $(docker --version)"
    else
        echo "❌ Docker not installed"
    fi
    
    # Check Node.js
    if command -v node &> /dev/null; then
        echo "✅ Node.js installed: $(node --version)"
    else
        echo "❌ Node.js not installed"
    fi
    
    # Check Git
    if command -v git &> /dev/null; then
        echo "✅ Git installed: $(git --version)"
    else
        echo "❌ Git not installed"
    fi
    
    # Check disk space
    echo ""
    echo "💾 Disk Space:"
    df -h . | head -2
    
    echo ""
}

# Task 1: Create Docker Development Container
task1_docker_container() {
    echo "📦 TASK 1: Create Docker Development Container"
    echo "----------------------------------------"
    echo "Requirements:"
    echo "1. Create a Dockerfile with Ubuntu or Alpine base"
    echo "2. Install Node.js, Python, and Git"
    echo "3. Configure VS Code connection"
    echo "4. Set up proper user permissions"
    echo ""
    echo "Files to create:"
    echo "- .devcontainer/Dockerfile"
    echo "- .devcontainer/devcontainer.json"
    echo ""
    
    # Check if files exist
    if [ -f ".devcontainer/Dockerfile" ] && [ -f ".devcontainer/devcontainer.json" ]; then
        echo "✅ Docker configuration files found!"
        
        # Validate Dockerfile
        if grep -q "FROM" .devcontainer/Dockerfile && \
           grep -q "node" .devcontainer/Dockerfile && \
           grep -q "python" .devcontainer/Dockerfile && \
           grep -q "git" .devcontainer/Dockerfile; then
            echo "✅ Dockerfile contains required components!"
        else
            echo "⚠️  Dockerfile missing required components"
        fi
    else
        echo "❌ Docker configuration files not found"
        echo ""
        echo "💡 Hint: Start with 'mkdir -p .devcontainer'"
    fi
    echo ""
}

# Task 2: File System Organization
task2_file_structure() {
    echo "📁 TASK 2: File System Organization"
    echo "----------------------------------------"
    echo "Required directory structure:"
    echo "project-root/"
    echo "├── .devcontainer/"
    echo "├── src/"
    echo "│   ├── frontend/"
    echo "│   ├── backend/"
    echo "│   └── shared/"
    echo "├── tests/"
    echo "├── docs/"
    echo "├── .env.example"
    echo "├── .gitignore"
    echo "├── README.md"
    echo "└── docker-compose.yml"
    echo ""
    
    # Check directory structure
    missing_dirs=()
    for dir in "src/frontend" "src/backend" "src/shared" "tests" "docs"; do
        if [ ! -d "$dir" ]; then
            missing_dirs+=("$dir")
        fi
    done
    
    missing_files=()
    for file in ".env.example" ".gitignore" "README.md" "docker-compose.yml"; do
        if [ ! -f "$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_dirs[@]} -eq 0 ] && [ ${#missing_files[@]} -eq 0 ]; then
        echo "✅ All required directories and files present!"
    else
        if [ ${#missing_dirs[@]} -gt 0 ]; then
            echo "❌ Missing directories: ${missing_dirs[*]}"
        fi
        if [ ${#missing_files[@]} -gt 0 ]; then
            echo "❌ Missing files: ${missing_files[*]}"
        fi
    fi
    echo ""
}

# Task 3: Environment Configuration
task3_environment_config() {
    echo "🔧 TASK 3: Environment Configuration"
    echo "----------------------------------------"
    echo "Requirements:"
    echo "1. Create .env file with at least 5 variables"
    echo "2. Implement .gitignore excluding sensitive files"
    echo "3. Set up git pre-commit hooks"
    echo ""
    
    # Check .env file
    if [ -f ".env" ]; then
        env_vars=$(grep -c "=" .env 2>/dev/null || echo 0)
        if [ "$env_vars" -ge 5 ]; then
            echo "✅ .env file has $env_vars variables (minimum 5 required)"
        else
            echo "⚠️  .env file has only $env_vars variables (need at least 5)"
        fi
    else
        echo "❌ .env file not found"
        echo "💡 Hint: Copy .env.example to .env and customize"
    fi
    
    # Check .gitignore
    if [ -f ".gitignore" ]; then
        if grep -q ".env" .gitignore && \
           grep -q "node_modules" .gitignore && \
           grep -q "*.log" .gitignore; then
            echo "✅ .gitignore properly configured!"
        else
            echo "⚠️  .gitignore missing important exclusions"
        fi
    else
        echo "❌ .gitignore not found"
    fi
    
    # Check git hooks
    if [ -d ".git/hooks" ] && [ -f ".git/hooks/pre-commit" ]; then
        echo "✅ Git pre-commit hook configured!"
    else
        echo "❌ Git pre-commit hook not configured"
        echo "💡 Hint: Create .git/hooks/pre-commit and make it executable"
    fi
    echo ""
}

# Task 4: Disk Space Management Script
task4_cleanup_script() {
    echo "🧹 TASK 4: Disk Space Management Script"
    echo "----------------------------------------"
    echo "Requirements:"
    echo "1. Clean Docker images older than 7 days"
    echo "2. Remove node_modules in non-active projects"
    echo "3. Delete log files larger than 100MB"
    echo "4. Ask for confirmation before deletion"
    echo ""
    
    if [ -f "cleanup.sh" ]; then
        echo "✅ cleanup.sh found!"
        
        # Check script contents
        if grep -q "docker" cleanup.sh && \
           grep -q "node_modules" cleanup.sh && \
           grep -q "confirm" cleanup.sh; then
            echo "✅ Script contains required functionality!"
        else
            echo "⚠️  Script missing some required features"
        fi
        
        # Check if executable
        if [ -x "cleanup.sh" ]; then
            echo "✅ Script is executable!"
        else
            echo "⚠️  Script not executable (use chmod +x cleanup.sh)"
        fi
    else
        echo "❌ cleanup.sh not found"
        echo "💡 Hint: Create a bash script that identifies and removes old files"
    fi
    echo ""
}

# Final validation
validate_sandbox() {
    echo "🎯 FINAL VALIDATION"
    echo "=================="
    
    passed=0
    total=4
    
    # Test 1: Docker container builds
    echo -n "Testing Docker container build... "
    if [ -f ".devcontainer/Dockerfile" ]; then
        if docker build -t test-sandbox .devcontainer &>/dev/null; then
            echo "✅ PASSED"
            ((passed++))
        else
            echo "❌ FAILED (container doesn't build)"
        fi
    else
        echo "❌ FAILED (Dockerfile not found)"
    fi
    
    # Test 2: Directory structure complete
    echo -n "Testing directory structure... "
    if [ -d "src/frontend" ] && [ -d "src/backend" ] && [ -d "tests" ] && [ -d "docs" ]; then
        echo "✅ PASSED"
        ((passed++))
    else
        echo "❌ FAILED"
    fi
    
    # Test 3: Environment configured
    echo -n "Testing environment configuration... "
    if [ -f ".env" ] && [ -f ".gitignore" ]; then
        echo "✅ PASSED"
        ((passed++))
    else
        echo "❌ FAILED"
    fi
    
    # Test 4: Cleanup script exists
    echo -n "Testing cleanup script... "
    if [ -f "cleanup.sh" ] && [ -x "cleanup.sh" ]; then
        echo "✅ PASSED"
        ((passed++))
    else
        echo "❌ FAILED"
    fi
    
    echo ""
    echo "=================="
    echo "SCORE: $passed/$total tests passed"
    
    if [ $passed -eq $total ]; then
        echo "🎉 CONGRATULATIONS! You've completed Week 1 Sandbox!"
        echo "You're ready to move on to Week 2: Planning & Architecture"
    else
        echo "🔄 Keep working! Remember: Work it until you solve it!"
        echo ""
        echo "Need help? Check the progressive hints:"
        echo "- After 15 mins: Review Docker multi-stage builds"
        echo "- After 30 mins: Check UID/GID matching for permissions"
        echo "- After 45 mins: Install VS Code Remote-Containers extension"
    fi
    echo ""
}

# Main execution
main() {
    clear
    check_environment
    
    echo "Starting sandbox exercise validation..."
    echo "======================================="
    echo ""
    
    task1_docker_container
    task2_file_structure
    task3_environment_config
    task4_cleanup_script
    
    validate_sandbox
    
    echo "Run this script again to re-validate your progress!"
    echo "Remember: There's no time limit - work it until you solve it!"
}

# Run main function
main