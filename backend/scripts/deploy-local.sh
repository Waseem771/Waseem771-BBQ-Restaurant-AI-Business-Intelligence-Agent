#!/bin/bash

##############################################################################
# LOCAL DOCKER DEPLOYMENT SCRIPT
# Purpose: Automated setup and testing for local development
# Usage: ./scripts/deploy-local.sh
##############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}══════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    print_success "Docker installed: $(docker --version)"

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    print_success "Docker Compose installed: $(docker-compose --version)"

    # Check Git
    if ! command -v git &> /dev/null; then
        print_warning "Git is not installed (optional)"
    else
        print_success "Git installed: $(git --version | head -n1)"
    fi

    # Check available disk space
    AVAILABLE_SPACE=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
    if [ "$AVAILABLE_SPACE" -lt 5 ]; then
        print_error "Insufficient disk space (need 5GB, have ${AVAILABLE_SPACE}GB)"
        exit 1
    fi
    print_success "Disk space available: ${AVAILABLE_SPACE}GB"
}

# Create environment file
create_env_file() {
    print_header "Setting Up Environment"

    if [ -f .env ]; then
        print_warning ".env file already exists"
        read -p "Overwrite? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Keeping existing .env"
            return
        fi
    fi

    if [ ! -f .env.example ]; then
        print_error ".env.example not found"
        exit 1
    fi

    cp .env.example .env
    print_success ".env file created"

    # Generate secure passwords
    print_info "Generating secure passwords..."
    DB_PASSWORD=$(openssl rand -base64 32)
    SECRET_KEY=$(openssl rand -base64 32)
    JWT_SECRET=$(openssl rand -base64 32)

    # Update .env file with generated values
    sed -i "s|change_this_secure_password_12345|$DB_PASSWORD|g" .env
    sed -i "s|your_generated_secret_key_here_change_this|$SECRET_KEY|g" .env
    sed -i "s|your_generated_jwt_secret_here_change_this|$JWT_SECRET|g" .env
    sed -i "s|APP_ENV=production|APP_ENV=development|g" .env
    sed -i "s|APP_DEBUG=false|APP_DEBUG=true|g" .env

    print_success "Environment variables configured"
    print_info "DB_PASSWORD: ${DB_PASSWORD:0:20}..."
    print_info "SECRET_KEY: ${SECRET_KEY:0:20}..."
    print_info "JWT_SECRET: ${JWT_SECRET:0:20}..."
}

# Stop existing containers
stop_existing() {
    print_header "Cleaning Up"

    if docker-compose ps | grep -q "Up"; then
        print_info "Stopping existing containers..."
        docker-compose down || true
        sleep 2
        print_success "Existing containers stopped"
    else
        print_info "No existing containers running"
    fi
}

# Build containers
build_containers() {
    print_header "Building Docker Images"

    print_info "Building containers (this may take 2-3 minutes)..."
    docker-compose build --no-cache

    print_success "Containers built successfully"
}

# Start services
start_services() {
    print_header "Starting Services"

    print_info "Starting services..."
    docker-compose up -d

    print_success "Services started"
}

# Wait for services to be healthy
wait_for_services() {
    print_header "Waiting for Services to Be Ready"

    # Wait for postgres
    print_info "Waiting for PostgreSQL..."
    for i in {1..30}; do
        if docker-compose exec -T postgres pg_isready -U bbq_user > /dev/null 2>&1; then
            print_success "PostgreSQL is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            print_error "PostgreSQL failed to start"
            docker-compose logs postgres
            exit 1
        fi
        echo -n "."
        sleep 1
    done

    # Wait for redis
    print_info "Waiting for Redis..."
    for i in {1..30}; do
        if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
            print_success "Redis is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            print_error "Redis failed to start"
            docker-compose logs redis
            exit 1
        fi
        echo -n "."
        sleep 1
    done

    # Wait for backend
    print_info "Waiting for Backend API..."
    for i in {1..60}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            print_success "Backend API is ready"
            break
        fi
        if [ $i -eq 60 ]; then
            print_error "Backend API failed to start"
            docker-compose logs backend
            exit 1
        fi
        echo -n "."
        sleep 1
    done

    # Wait for frontend
    print_info "Waiting for Frontend..."
    for i in {1..30}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            print_success "Frontend is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            print_warning "Frontend may still be building"
        fi
        echo -n "."
        sleep 1
    done
}

# Run tests
run_tests() {
    print_header "Running Tests"

    print_info "Testing Backend API..."
    BACKEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
    if [ "$BACKEND_RESPONSE" = "200" ]; then
        print_success "Backend API is responding"
    else
        print_error "Backend API returned status $BACKEND_RESPONSE"
    fi

    print_info "Testing Frontend..."
    FRONTEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
    if [ "$FRONTEND_RESPONSE" = "200" ]; then
        print_success "Frontend is responding"
    else
        print_warning "Frontend returned status $FRONTEND_RESPONSE (may be still loading)"
    fi

    print_info "Testing Database..."
    DB_TEST=$(docker-compose exec -T postgres psql -U bbq_user -d bbq_db -c "SELECT 1" 2>&1 | grep -c "1 row")
    if [ "$DB_TEST" = "1" ]; then
        print_success "Database connection successful"
    else
        print_error "Database connection failed"
    fi

    print_info "Testing Redis..."
    REDIS_TEST=$(docker-compose exec -T redis redis-cli ping)
    if [ "$REDIS_TEST" = "PONG" ]; then
        print_success "Redis connection successful"
    else
        print_error "Redis connection failed"
    fi
}

# Display summary
display_summary() {
    print_header "Deployment Complete! 🎉"

    echo -e "${GREEN}Your application is now running!${NC}\n"

    echo "📋 Services Status:"
    docker-compose ps

    echo -e "\n🌐 Access Points:"
    echo -e "  ${BLUE}Frontend:${NC}        http://localhost:3000"
    echo -e "  ${BLUE}Backend API:${NC}     http://localhost:8000"
    echo -e "  ${BLUE}API Docs:${NC}        http://localhost:8000/docs"
    echo -e "  ${BLUE}Database:${NC}        postgres://bbq_user@localhost:5432/bbq_db"
    echo -e "  ${BLUE}Redis:${NC}           redis://localhost:6379"

    echo -e "\n📝 Useful Commands:"
    echo -e "  View logs:        ${BLUE}docker-compose logs -f${NC}"
    echo -e "  View backend logs: ${BLUE}docker-compose logs -f backend${NC}"
    echo -e "  View frontend logs:${BLUE}docker-compose logs -f frontend${NC}"
    echo -e "  Stop services:    ${BLUE}docker-compose down${NC}"
    echo -e "  Restart services: ${BLUE}docker-compose restart${NC}"
    echo -e "  DB shell:         ${BLUE}docker-compose exec postgres psql -U bbq_user -d bbq_db${NC}"
    echo -e "  Redis shell:      ${BLUE}docker-compose exec redis redis-cli${NC}"

    echo -e "\n📚 Next Steps:"
    echo -e "  1. Open ${BLUE}http://localhost:3000${NC} in your browser"
    echo -e "  2. Log in with your credentials"
    echo -e "  3. Test the AI assistant"
    echo -e "  4. Check the API documentation at ${BLUE}http://localhost:8000/docs${NC}"
    echo -e "  5. Review logs if there are any issues"

    echo -e "\n⚠️  Important:"
    echo -e "  This is development mode (APP_ENV=development)"
    echo -e "  For production, use environment-specific configurations"
    echo -e "  Change APP_ENV to 'production' and APP_DEBUG to 'false' in .env"
}

# Main execution
main() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║  BBQ Restaurant AI - Local Docker Deployment Script     ║"
    echo "║  Version 1.0.0                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    check_prerequisites
    create_env_file
    stop_existing
    build_containers
    start_services
    wait_for_services
    run_tests
    display_summary

    print_success "Deployment completed successfully!"
}

# Run main function
main
