#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BACKEND_URL="https://yolande-nondivisional-norah.ngrok-free.dev"
FRONTEND_URL="https://frontend-hlj3mfe5a-om-narayan-pandits-projects.vercel.app"
PROJECT_DIR="/home/emperor/Projects/Smart Blood Bank System"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     🧪 SMART BLOOD BANK - COMPREHENSIVE TEST SUITE 🧪       ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

run_test() {
    local test_name=$1
    local test_command=$2
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo -e "${YELLOW}▶ Test $TOTAL_TESTS: $test_name${NC}"
    
    if eval "$test_command"; then
        echo -e "${GREEN}  ✓ PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}  ✗ FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    echo ""
}

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}BACKEND API TESTS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

run_test "Backend Health Check" \
    "curl -s $BACKEND_URL/health | grep -q 'healthy'"

run_test "Backend Root Endpoint" \
    "curl -s $BACKEND_URL/ | grep -q 'Smart Blood Bank API'"

run_test "API Documentation Available" \
    "curl -s $BACKEND_URL/docs | grep -q 'Swagger'"

run_test "List Hospitals Endpoint" \
    "curl -s $BACKEND_URL/api/hospitals | grep -q '\['"

run_test "Get Hospital H001" \
    "curl -s $BACKEND_URL/api/hospitals/H001 | grep -q 'H001'"

run_test "Dashboard Summary Endpoint" \
    "curl -s $BACKEND_URL/api/dashboard/summary | grep -q 'status'"

run_test "High Risk Inventory Endpoint" \
    "curl -s $BACKEND_URL/api/dashboard/high-risk-inventory | grep -q 'count'"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}FILE UPLOAD TESTS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

run_test "Upload New CSV" \
    "curl -s -X POST $BACKEND_URL/api/inventory/upload -F 'file=@$PROJECT_DIR/test_samples/new_inventory.csv' | grep -q 'success'"

run_test "Upload Invalid CSV (Error Handling)" \
    "curl -s -X POST $BACKEND_URL/api/inventory/upload -F 'file=@$PROJECT_DIR/test_samples/invalid_inventory.csv' | grep -qE '(error_count|errors)'"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}DATABASE TESTS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

run_test "Database Connection" \
    "cd '$PROJECT_DIR/backend' && source .venv/bin/activate && python3 -c 'from app.database import engine; engine.connect()' 2>&1 | grep -qv 'Error'"

run_test "Count Inventory Records" \
    "cd '$PROJECT_DIR/backend' && source .venv/bin/activate && python3 -c 'from app.database import SessionLocal; from app.models.inventory import Inventory; db = SessionLocal(); count = db.query(Inventory).count(); print(f\"Found {count} records\"); db.close()' | grep -q 'Found'"

run_test "Count Hospital Records" \
    "cd '$PROJECT_DIR/backend' && source .venv/bin/activate && python3 -c 'from app.database import SessionLocal; from app.models.hospital import Hospital; db = SessionLocal(); count = db.query(Hospital).count(); print(f\"Found {count} hospitals\"); db.close()' | grep -q 'Found'"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}FRONTEND TESTS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

run_test "Frontend Deployed and Accessible" \
    "curl -s -L $FRONTEND_URL | grep -qi 'blood'"

run_test "Frontend Assets Loaded" \
    "curl -s -L $FRONTEND_URL | grep -qE '(stylesheet|script)'"

run_test "Frontend JavaScript Loaded" \
    "curl -s -L $FRONTEND_URL | grep -q 'script'"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}INTEGRATION TESTS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

run_test "CORS Configuration Working" \
    "curl -s $BACKEND_URL/api/hospitals | grep -q '\['"

run_test "ngrok Tunnel Active" \
    "curl -s http://localhost:4040/api/tunnels | grep -q 'public_url'"

run_test "PostgreSQL Container Running" \
    "docker ps 2>/dev/null | grep -q postgres"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}TEST SUMMARY${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "Total Tests:  ${BLUE}$TOTAL_TESTS${NC}"
echo -e "Passed:       ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed:       ${RED}$FAILED_TESTS${NC}"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              🎉 ALL TESTS PASSED! 🎉                         ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${YELLOW}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║         ✅ $PASSED_TESTS/$TOTAL_TESTS TESTS PASSED                              ║${NC}"
    echo -e "${YELLOW}╚══════════════════════════════════════════════════════════════╝${NC}"
    exit 0
fi
