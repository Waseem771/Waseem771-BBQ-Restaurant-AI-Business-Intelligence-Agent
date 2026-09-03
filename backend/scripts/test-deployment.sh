#!/bin/bash

##############################################################################
# DOCKER DEPLOYMENT TESTING & VALIDATION SCRIPT
# Purpose: Comprehensive testing of all services after deployment
# Usage: ./scripts/test-deployment.sh [environment]
# Environments: local, staging, production
##############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

ENVIRONMENT=${1:-"local"}
TEST_RESULTS="test_results_$(date +%Y%m%d_%H%M%S).log"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Functions
print_header() {
    echo -e "\n${BLUE}======================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
    echo "[PASS] $1" >> "$TEST_RESULTS"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    echo "[FAIL] $1" >> "$TEST_RESULTS"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    echo "[WARN] $1" >> "$TEST_RESULTS"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
    echo "[INFO] $1" >> "$TEST_RESULTS"
}

print_test() {
    echo -e "${MAGENTA}▶ Testing: $1${NC}"
    echo "[TEST] $1" >> "$TEST_RESULTS"
}

run_test() {
    local test_name=$1
    local command=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    print_test "$test_name"

    if eval "$command" > /dev/null 2>&1; then
        print_success "$test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_error "$test_name"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Determine API URLs based on environment
set_environment_urls() {
    print_header "Configuring for $ENVIRONMENT Environment"

    case $ENVIRONMENT in
        local)
            API_URL="http://localhost:8000"
            FRONTEND_URL="http://localhost:3000"
            DB_HOST="localhost"
            REDIS_HOST="localhost"
            print_success "Using local URLs"
            ;;
        staging)
            API_URL="${STAGING_API_URL:-http://staging.api}"
            FRONTEND_URL="${STAGING_FRONTEND_URL:-http://staging.app}"
            DB_HOST="${STAGING_DB_HOST:-staging-db}"
            REDIS_HOST="${STAGING_REDIS_HOST:-staging-redis}"
            print_success "Using staging URLs"
            ;;
        production)
            API_URL="${PROD_API_URL:-https://api.yourdomain.com}"
            FRONTEND_URL="${PROD_FRONTEND_URL:-https://yourdomain.com}"
            DB_HOST="${PROD_DB_HOST:-prod-db}"
            REDIS_HOST="${PROD_REDIS_HOST:-prod-redis}"
            print_success "Using production URLs"
            ;;
    esac
}

# Test Docker services
test_docker_services() {
    print_header "Testing Docker Services"

    run_test "Docker is running" "docker ps > /dev/null"
    run_test "Docker Compose is available" "docker-compose --version"
    run_test "Containers are running" "docker-compose ps | grep -q Up"
}

# Test backend API
test_backend_api() {
    print_header "Testing Backend API"

    run_test "Backend health check" "curl -s -f $API_URL/health"
    run_test "API docs available" "curl -s -f $API_URL/docs"
    run_test "OpenAPI schema available" "curl -s -f $API_URL/openapi.json"
    run_test "Backend responds to requests" "curl -s -f $API_URL/api/v1/dashboard"
}

# Test database
test_database() {
    print_header "Testing Database"

    run_test "PostgreSQL container running" "docker-compose ps postgres | grep -q Up"
    run_test "PostgreSQL accepting connections" "docker-compose exec -T postgres pg_isready -U bbq_user"
    run_test "Database exists" "docker-compose exec -T postgres psql -U bbq_user -d bbq_db -c 'SELECT 1'"
}

# Test Redis
test_redis() {
    print_header "Testing Redis"

    run_test "Redis container running" "docker-compose ps redis | grep -q Up"
    run_test "Redis accepting connections" "docker-compose exec -T redis redis-cli ping | grep -q PONG"
    run_test "Redis can store data" "docker-compose exec -T redis redis-cli SET test_key test_value"
    run_test "Redis can retrieve data" "docker-compose exec -T redis redis-cli GET test_key | grep -q test_value"
}

# Test frontend
test_frontend() {
    print_header "Testing Frontend"

    run_test "Frontend is running" "curl -s -f $FRONTEND_URL > /dev/null"
    run_test "Frontend serves HTML" "curl -s -I $FRONTEND_URL | grep -q 'text/html'"
    run_test "Frontend assets are available" "curl -s -f $FRONTEND_URL/index.html"
}

# Test API endpoints
test_api_endpoints() {
    print_header "Testing API Endpoints"

    run_test "Dashboard endpoint responds" "curl -s -f $API_URL/api/v1/dashboard"
    run_test "Sales endpoint responds" "curl -s -f $API_URL/api/v1/sales"
    run_test "Products endpoint responds" "curl -s -f $API_URL/api/v1/products"
    run_test "Orders endpoint responds" "curl -s -f $API_URL/api/v1/orders"
    run_test "Metrics endpoint responds" "curl -s -f $API_URL/metrics"
}

# Test authentication
test_authentication() {
    print_header "Testing Authentication"

    run_test "Auth endpoint exists" "curl -s -f $API_URL/api/v1/auth/login"
    run_test "Unauthorized access rejected" "! curl -s -f $API_URL/api/v1/dashboard -H 'Authorization: Bearer invalid'"
}

# Test WebSocket connectivity
test_websockets() {
    print_header "Testing WebSocket Connectivity"

    print_test "WebSocket endpoints are configured"
    if grep -q "location /ws" frontend/nginx.conf; then
        print_success "WebSocket proxy configured in Nginx"
    else
        print_warning "WebSocket proxy not found in Nginx config"
    fi
}

# Test SSL/HTTPS (for production)
test_ssl() {
    print_header "Testing SSL/HTTPS"

    if [ "$ENVIRONMENT" = "production" ]; then
        run_test "HTTPS is enforced" "curl -s -I $FRONTEND_URL | grep -q 'HTTP/2'"
        run_test "SSL certificate is valid" "echo | openssl s_client -servername $(echo $FRONTEND_URL | cut -d'/' -f3) -connect $(echo $FRONTEND_URL | cut -d'/' -f3):443 2>/dev/null | grep -q 'Verify return code'"
    else
        print_info "Skipping SSL tests for non-production environment"
    fi
}

# Test container logs for errors
test_logs() {
    print_header "Testing Container Logs"

    print_test "Checking for critical errors in backend logs"
    if docker-compose logs backend 2>&1 | grep -i "critical\|fatal" > /dev/null; then
        print_warning "Critical errors found in backend logs"
    else
        print_success "No critical errors in backend logs"
    fi

    print_test "Checking for critical errors in frontend logs"
    if docker-compose logs frontend 2>&1 | grep -i "critical\|fatal" > /dev/null; then
        print_warning "Critical errors found in frontend logs"
    else
        print_success "No critical errors in frontend logs"
    fi

    print_test "Checking for database connection errors"
    if docker-compose logs backend 2>&1 | grep -i "database.*error\|connection.*refused" > /dev/null; then
        print_warning "Database connection errors found"
    else
        print_success "No database connection errors"
    fi
}

# Test performance
test_performance() {
    print_header "Testing Performance"

    print_test "API response time"
    START=$(date +%s%N | cut -b1-13)
    curl -s -f $API_URL/api/v1/dashboard > /dev/null
    END=$(date +%s%N | cut -b1-13)
    RESPONSE_TIME=$((END - START))

    if [ $RESPONSE_TIME -lt 1000 ]; then
        print_success "API response time: ${RESPONSE_TIME}ms (good)"
    elif [ $RESPONSE_TIME -lt 2000 ]; then
        print_warning "API response time: ${RESPONSE_TIME}ms (acceptable)"
    else
        print_warning "API response time: ${RESPONSE_TIME}ms (slow)"
    fi

    print_test "Frontend load time"
    START=$(date +%s%N | cut -b1-13)
    curl -s -f $FRONTEND_URL > /dev/null
    END=$(date +%s%N | cut -b1-13)
    LOAD_TIME=$((END - START))

    if [ $LOAD_TIME -lt 1000 ]; then
        print_success "Frontend load time: ${LOAD_TIME}ms (good)"
    elif [ $LOAD_TIME -lt 2000 ]; then
        print_warning "Frontend load time: ${LOAD_TIME}ms (acceptable)"
    else
        print_warning "Frontend load time: ${LOAD_TIME}ms (slow)"
    fi
}

# Test security headers
test_security_headers() {
    print_header "Testing Security Headers"

    print_test "Checking X-Frame-Options header"
    if curl -s -I $FRONTEND_URL | grep -q "X-Frame-Options"; then
        print_success "X-Frame-Options header present"
    else
        print_warning "X-Frame-Options header missing"
    fi

    print_test "Checking X-Content-Type-Options header"
    if curl -s -I $FRONTEND_URL | grep -q "X-Content-Type-Options"; then
        print_success "X-Content-Type-Options header present"
    else
        print_warning "X-Content-Type-Options header missing"
    fi

    print_test "Checking X-XSS-Protection header"
    if curl -s -I $FRONTEND_URL | grep -q "X-XSS-Protection"; then
        print_success "X-XSS-Protection header present"
    else
        print_warning "X-XSS-Protection header missing"
    fi
}

# Test disk space
test_disk_space() {
    print_header "Testing Disk Space"

    AVAILABLE=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')

    if [ "$AVAILABLE" -lt 1 ]; then
        print_error "Critical: Less than 1GB disk space available"
    elif [ "$AVAILABLE" -lt 5 ]; then
        print_warning "Low disk space: ${AVAILABLE}GB available"
    else
        print_success "Adequate disk space: ${AVAILABLE}GB available"
    fi
}

# Test container resource usage
test_resource_usage() {
    print_header "Testing Resource Usage"

    print_info "Container Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.MemUsage}}\t{{.CPUPerc}}" | head -10
}

# Generate test report
generate_report() {
    print_header "Test Summary"

    echo -e "\n${BLUE}═════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}Test Results Summary${NC}"
    echo -e "${BLUE}═════════════════════════════════════════════════════════${NC}\n"

    echo "Environment: $ENVIRONMENT"
    echo "Total Tests: $TESTS_RUN"
    echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Failed: ${RED}$TESTS_FAILED${NC}"

    if [ $TESTS_FAILED -eq 0 ]; then
        SUCCESS_RATE=100
        echo -e "Success Rate: ${GREEN}${SUCCESS_RATE}%${NC}"
    else
        SUCCESS_RATE=$((TESTS_PASSED * 100 / TESTS_RUN))
        echo -e "Success Rate: ${YELLOW}${SUCCESS_RATE}%${NC}"
    fi

    echo -e "\nDetailed results saved to: ${BLUE}$TEST_RESULTS${NC}"

    # Print report file
    echo -e "\n${BLUE}Full Test Report:${NC}\n"
    cat "$TEST_RESULTS"
}

# Main execution
main() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║  BBQ Restaurant AI - Deployment Testing Suite       ║"
    echo "║  Version 1.0.0                                      ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    # Initialize test results file
    echo "BBQ Restaurant AI - Deployment Test Results" > "$TEST_RESULTS"
    echo "Environment: $ENVIRONMENT" >> "$TEST_RESULTS"
    echo "Date: $(date)" >> "$TEST_RESULTS"
    echo "================================" >> "$TEST_RESULTS"

    set_environment_urls
    test_docker_services
    test_backend_api
    test_database
    test_redis
    test_frontend
    test_api_endpoints
    test_authentication
    test_websockets
    test_ssl
    test_logs
    test_performance
    test_security_headers
    test_disk_space
    test_resource_usage
    generate_report

    echo -e "\n${BLUE}═════════════════════════════════════════════════════════${NC}"

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed! Deployment is healthy.${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some tests failed. Review the results above.${NC}"
        exit 1
    fi
}

main
