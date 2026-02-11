#!/bin/bash

# Smoke test script for post-deployment validation
# Usage: ./smoke_test.sh [service_url]

set -e

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

# Function to run a test
run_test() {
    local test_name="$1"
    local test_cmd="$2"
    
    echo "Test: $test_name"
    if eval "$test_cmd"; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((FAILED++))
    fi
    echo ""
}

# Wait for service to be ready
echo "Waiting for service to be ready..."
MAX_WAIT=60
WAITED=0
while [ $WAITED -lt $MAX_WAIT ]; do
    if curl -sf "${SERVICE_URL}/health" > /dev/null 2>&1; then
        echo "Service is ready!"
        break
    fi
    sleep 2
    WAITED=$((WAITED + 2))
    echo "  Waiting... ($WAITED/$MAX_WAIT seconds)"
done

if [ $WAITED -ge $MAX_WAIT ]; then
    echo -e "${RED}Service failed to become ready within ${MAX_WAIT} seconds${NC}"
    exit 1
fi
echo ""

# Test 1: Health Check
run_test "Health Check" "curl -sf ${SERVICE_URL}/health | grep -q 'healthy'"

# Test 2: Root Endpoint
run_test "Root Endpoint" "curl -sf ${SERVICE_URL}/ | grep -q 'Cats vs Dogs'"

# Test 3: Metrics Endpoint
run_test "Metrics Endpoint" "curl -sf ${SERVICE_URL}/metrics | grep -q 'total_requests'"

# Test 4: Model Info Endpoint
run_test "Model Info" "curl -sf ${SERVICE_URL}/model-info | grep -q 'Custom CNN'"

# Test 5: Model loaded check
run_test "Model Loaded" "curl -sf ${SERVICE_URL}/health | grep -q 'model_loaded.*true'"

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



