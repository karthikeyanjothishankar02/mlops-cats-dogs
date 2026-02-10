#!/bin/bash

# Smoke test script for post-deployment validation
# Usage: ./smoke_test.sh <service_url>

SERVICE_URL="${1:-http://localhost:8000}"

echo "=================================="
echo "Running Smoke Tests"
echo "=================================="
echo "Service URL: $SERVICE_URL"
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Counter for passed/failed tests
PASSED=0
FAILED=0

# Test 1: Health Check
echo "Test 1: Health Check"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" ${SERVICE_URL}/health)
if [ "$RESPONSE" -eq 200 ]; then
    echo -e "${GREEN}✓ Health check passed (HTTP 200)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Health check failed (HTTP ${RESPONSE})${NC}"
    ((FAILED++))
fi
echo ""

# Test 2: Root Endpoint
echo "Test 2: Root Endpoint"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" ${SERVICE_URL}/)
if [ "$RESPONSE" -eq 200 ]; then
    echo -e "${GREEN}✓ Root endpoint accessible (HTTP 200)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Root endpoint failed (HTTP ${RESPONSE})${NC}"
    ((FAILED++))
fi
echo ""

# Test 3: Metrics Endpoint
echo "Test 3: Metrics Endpoint"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" ${SERVICE_URL}/metrics)
if [ "$RESPONSE" -eq 200 ]; then
    echo -e "${GREEN}✓ Metrics endpoint accessible (HTTP 200)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Metrics endpoint failed (HTTP ${RESPONSE})${NC}"
    ((FAILED++))
fi
echo ""

# Test 4: Model Info Endpoint
echo "Test 4: Model Info Endpoint"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" ${SERVICE_URL}/model-info)
if [ "$RESPONSE" -eq 200 ]; then
    echo -e "${GREEN}✓ Model info endpoint accessible (HTTP 200)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Model info endpoint failed (HTTP ${RESPONSE})${NC}"
    ((FAILED++))
fi
echo ""

# Test 5: Check if model is loaded (from health check response)
echo "Test 5: Model Load Status"
MODEL_STATUS=$(curl -s ${SERVICE_URL}/health | grep -o '"model_loaded":true' | wc -l)
if [ "$MODEL_STATUS" -gt 0 ]; then
    echo -e "${GREEN}✓ Model is loaded${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Model not loaded${NC}"
    ((FAILED++))
fi
echo ""

# Summary
echo "=================================="
echo "Smoke Test Summary"
echo "=================================="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All smoke tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some smoke tests failed!${NC}"
    exit 1
fi
