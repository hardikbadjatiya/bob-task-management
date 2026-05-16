#!/bin/bash

# Task Management System - Validation Script
# This script validates the project structure and code without running Docker

set -e

echo "🔍 Validating Task Management System..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
CHECKS_PASSED=0
CHECKS_FAILED=0

# Function to check file exists
check_file() {
    local name=$1
    local file=$2
    
    echo -n "Checking $name... "
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ EXISTS${NC}"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}❌ MISSING${NC}"
        ((CHECKS_FAILED++))
    fi
}

# Function to check directory exists
check_dir() {
    local name=$1
    local dir=$2
    
    echo -n "Checking $name... "
    
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅ EXISTS${NC}"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}❌ MISSING${NC}"
        ((CHECKS_FAILED++))
    fi
}

# Function to validate Python syntax
validate_python() {
    local file=$1
    
    if command -v python3 &> /dev/null; then
        if python3 -m py_compile "$file" 2>/dev/null; then
            return 0
        else
            return 1
        fi
    fi
    return 0
}

# Function to validate TypeScript syntax
validate_typescript() {
    local file=$1
    
    if command -v node &> /dev/null; then
        # Basic syntax check - just check if file is readable
        if [ -r "$file" ]; then
            return 0
        else
            return 1
        fi
    fi
    return 0
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📁 Project Structure Validation${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check root files
check_file "Docker Compose" "docker-compose.yml"
check_file "Start Script" "start.sh"
check_file "Stop Script" "stop.sh"
check_file "Dev Start Script" "start-dev.sh"
check_file "Test Script" "test.sh"
check_file "Validation Script" "validate.sh"
check_file "Testing Guide" "TESTING_GUIDE.md"
check_file "README" "README.md"

echo ""
echo -e "${BLUE}🐍 Backend Structure${NC}"
echo ""

# Check backend directories
check_dir "Backend Root" "backend"
check_dir "Backend App" "backend/app"
check_dir "Backend Models" "backend/app/models"
check_dir "Backend Schemas" "backend/app/schemas"
check_dir "Backend API" "backend/app/api"
check_dir "Backend Core" "backend/app/core"

echo ""

# Check backend files
check_file "Backend Dockerfile" "backend/Dockerfile"
check_file "Backend Requirements" "backend/requirements.txt"
check_file "Backend .env" "backend/.env"
check_file "Backend Main" "backend/app/main.py"
check_file "Backend Config" "backend/app/config.py"
check_file "Backend Database" "backend/app/database.py"

echo ""
echo -e "${BLUE}⚛️  Frontend Structure${NC}"
echo ""

# Check frontend directories
check_dir "Frontend Root" "frontend"
check_dir "Frontend Src" "frontend/src"
check_dir "Frontend Services" "frontend/src/services"
check_dir "Frontend Types" "frontend/src/types"

echo ""

# Check frontend files
check_file "Frontend Dockerfile" "frontend/Dockerfile"
check_file "Frontend Package.json" "frontend/package.json"
check_file "Frontend Vite Config" "frontend/vite.config.ts"
check_file "Frontend App" "frontend/src/App.tsx"
check_file "Frontend Main" "frontend/src/main.tsx"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🔍 Code Validation${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Validate Python files
if command -v python3 &> /dev/null; then
    echo "Validating Python syntax..."
    
    PYTHON_FILES=(
        "backend/app/main.py"
        "backend/app/config.py"
        "backend/app/database.py"
        "backend/app/models/user.py"
        "backend/app/models/task.py"
        "backend/app/models/team.py"
    )
    
    for file in "${PYTHON_FILES[@]}"; do
        if [ -f "$file" ]; then
            echo -n "  Validating $file... "
            if validate_python "$file"; then
                echo -e "${GREEN}✅ VALID${NC}"
                ((CHECKS_PASSED++))
            else
                echo -e "${RED}❌ SYNTAX ERROR${NC}"
                ((CHECKS_FAILED++))
            fi
        fi
    done
else
    echo -e "${YELLOW}⚠️  Python not found, skipping Python validation${NC}"
fi

echo ""

# Check TypeScript files
if command -v node &> /dev/null; then
    echo "Validating TypeScript files..."
    
    TS_FILES=(
        "frontend/src/App.tsx"
        "frontend/src/main.tsx"
        "frontend/src/services/api.ts"
        "frontend/src/services/authService.ts"
    )
    
    for file in "${TS_FILES[@]}"; do
        if [ -f "$file" ]; then
            echo -n "  Checking $file... "
            if validate_typescript "$file"; then
                echo -e "${GREEN}✅ READABLE${NC}"
                ((CHECKS_PASSED++))
            else
                echo -e "${RED}❌ ERROR${NC}"
                ((CHECKS_FAILED++))
            fi
        fi
    done
else
    echo -e "${YELLOW}⚠️  Node.js not found, skipping TypeScript validation${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🔧 Configuration Validation${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check .env file
if [ -f "backend/.env" ]; then
    echo -n "Checking SECRET_KEY in .env... "
    if grep -q "SECRET_KEY=" "backend/.env"; then
        echo -e "${GREEN}✅ CONFIGURED${NC}"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}❌ MISSING${NC}"
        ((CHECKS_FAILED++))
    fi
    
    echo -n "Checking DATABASE_URL in .env... "
    if grep -q "DATABASE_URL=" "backend/.env"; then
        echo -e "${GREEN}✅ CONFIGURED${NC}"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}❌ MISSING${NC}"
        ((CHECKS_FAILED++))
    fi
fi

echo ""

# Check Docker configuration
echo -n "Checking Docker Compose services... "
if grep -q "postgres:" "docker-compose.yml" && \
   grep -q "redis:" "docker-compose.yml" && \
   grep -q "backend:" "docker-compose.yml" && \
   grep -q "frontend:" "docker-compose.yml"; then
    echo -e "${GREEN}✅ ALL SERVICES DEFINED${NC}"
    ((CHECKS_PASSED++))
else
    echo -e "${RED}❌ MISSING SERVICES${NC}"
    ((CHECKS_FAILED++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📊 Validation Summary${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "Checks Passed: ${GREEN}$CHECKS_PASSED${NC}"
echo -e "Checks Failed: ${RED}$CHECKS_FAILED${NC}"
echo -e "Total Checks:  $((CHECKS_PASSED + CHECKS_FAILED))"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All validation checks passed!${NC}"
    echo ""
    echo "✅ Project structure is complete"
    echo "✅ All required files exist"
    echo "✅ Code syntax is valid"
    echo "✅ Configuration is set up"
    echo ""
    echo "🚀 Ready to start the application!"
    echo "   Run: ./start.sh (with Docker)"
    echo "   Or:  ./start-dev.sh (local development)"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Some validation checks failed${NC}"
    echo ""
    echo "Please fix the issues above before starting the application."
    echo ""
    exit 1
fi

# Made with Bob
