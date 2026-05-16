#!/bin/bash

# Task Management System - Test Script
# This script tests the application endpoints

set -e

echo "🧪 Testing Task Management System..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Base URLs
BACKEND_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local expected_code=$3
    
    echo -n "Testing $name... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    
    if [ "$response" = "$expected_code" ]; then
        echo -e "${GREEN}✅ PASSED${NC} (HTTP $response)"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC} (Expected $expected_code, got $response)"
        ((TESTS_FAILED++))
    fi
}

# Function to test POST endpoint
test_post_endpoint() {
    local name=$1
    local url=$2
    local data=$3
    local expected_code=$4
    
    echo -n "Testing $name... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
        -H "Content-Type: application/json" \
        -d "$data" \
        "$url" 2>/dev/null || echo "000")
    
    if [ "$response" = "$expected_code" ]; then
        echo -e "${GREEN}✅ PASSED${NC} (HTTP $response)"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC} (Expected $expected_code, got $response)"
        ((TESTS_FAILED++))
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🔍 Backend API Tests${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test backend health
test_endpoint "Backend Root" "$BACKEND_URL/" "200"
test_endpoint "API Docs" "$BACKEND_URL/docs" "200"
test_endpoint "OpenAPI Schema" "$BACKEND_URL/openapi.json" "200"

echo ""
echo -e "${BLUE}🔐 Authentication Endpoints${NC}"
echo ""

# Test auth endpoints (should return 422 for missing data)
test_post_endpoint "Register Endpoint" "$BACKEND_URL/api/v1/auth/register" '{}' "422"
test_post_endpoint "Login Endpoint" "$BACKEND_URL/api/v1/auth/login" '{}' "422"

echo ""
echo -e "${BLUE}📝 Task Endpoints (Unauthorized)${NC}"
echo ""

# Test task endpoints (should return 401 for unauthorized)
test_endpoint "Get Tasks (Unauthorized)" "$BACKEND_URL/api/v1/tasks/" "401"

echo ""
echo -e "${BLUE}👥 User Endpoints (Unauthorized)${NC}"
echo ""

# Test user endpoints (should return 401 for unauthorized)
test_endpoint "Get Current User (Unauthorized)" "$BACKEND_URL/api/v1/users/me" "401"

echo ""
echo -e "${BLUE}🏢 Team Endpoints (Unauthorized)${NC}"
echo ""

# Test team endpoints (should return 401 for unauthorized)
test_endpoint "Get Teams (Unauthorized)" "$BACKEND_URL/api/v1/teams/" "401"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🌐 Frontend Tests${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test frontend
test_endpoint "Frontend Root" "$FRONTEND_URL/" "200"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📊 Test Summary${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo -e "Total Tests:  $((TESTS_PASSED + TESTS_FAILED))"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi

# Made with Bob
