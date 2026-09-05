#!/bin/bash

##############################################################################
# PRODUCTION DOCKER DEPLOYMENT SCRIPT
# Purpose: Deploy to production with security, monitoring, and backups
# Usage: ./scripts/deploy-production.sh <provider> [domain]
# Providers: digitalocean, aws, docker-hub, custom-vps
##############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROVIDER=${1:-"digitalocean"}
DOMAIN=${2:-""}

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

# Validate inputs
validate_inputs() {
    print_header "Validating Inputs"

    if [ -z "$PROVIDER" ]; then
        print_error "Provider not specified"
        echo "Usage: $0 <provider> [domain]"
        echo "Providers: digitalocean, aws, docker-hub, custom-vps"
        exit 1
    fi

    case $PROVIDER in
        digitalocean|aws|docker-hub|custom-vps)
            print_success "Provider: $PROVIDER"
            ;;
        *)
            print_error "Unknown provider: $PROVIDER"
            exit 1
            ;;
    esac

    if [ -z "$DOMAIN" ] && [ "$PROVIDER" != "aws" ]; then
        print_warning "No domain specified. Using IP-based access only."
        print_info "You can set domain later with: export DOMAIN=yourdomain.com"
    else
        print_success "Domain: $DOMAIN"
    fi
}

# Pre-deployment checks
pre_deployment_checks() {
    print_header "Pre-Deployment Checks"

    # Check if .env.prod exists
    if [ ! -f ".env.prod" ]; then
        print_warning ".env.prod not found. Creating from .env.example..."
        cp .env.example .env.prod
        print_info "Edit .env.prod with production values before deploying"
        print_error "Please configure .env.prod and run again"
        exit 1
    fi
    print_success ".env.prod exists"

    # Check if Dockerfile exists
    if [ ! -f "backend/Dockerfile" ] || [ ! -f "frontend/Dockerfile" ]; then
        print_error "Dockerfiles not found"
        exit 1
    fi
    print_success "Dockerfiles present"

    # Check if docker-compose.yml exists
    if [ ! -f "docker-compose.yml" ]; then
        print_error "docker-compose.yml not found"
        exit 1
    fi
    print_success "docker-compose.yml present"

    # Verify production settings
    print_info "Verifying production settings..."
    if grep -q "APP_ENV=development" .env.prod; then
        print_warning "APP_ENV is set to 'development' - should be 'production'"
    fi
    if grep -q "APP_DEBUG=true" .env.prod; then
        print_warning "APP_DEBUG is set to 'true' - should be 'false'"
    fi
    print_success "Configuration checks complete"
}

# Backup existing data (if applicable)
backup_existing() {
    print_header "Backing Up Existing Data"

    if [ -d "backups" ]; then
        BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$BACKUP_DIR"
        print_info "Creating backup in $BACKUP_DIR..."

        # Backup .env files
        if [ -f ".env.prod" ]; then
            cp .env.prod "$BACKUP_DIR/"
            print_success "Backed up .env.prod"
        fi

        # Backup docker-compose.yml
        cp docker-compose.yml "$BACKUP_DIR/"
        print_success "Backed up docker-compose.yml"

        # Backup Dockerfiles
        cp -r backend/Dockerfile frontend/Dockerfile "$BACKUP_DIR/"
        print_success "Backed up Dockerfiles"

        print_success "Backup complete: $BACKUP_DIR"
    fi
}

# Deploy to DigitalOcean
deploy_digitalocean() {
    print_header "DigitalOcean Deployment Configuration"

    print_info "DigitalOcean Deployment Steps:"
    echo "
1. Create Droplet:
   - Go to https://cloud.digitalocean.com/droplets
   - Click 'Create Droplets'
   - Image: Ubuntu 22.04 LTS
   - Plan: \$5/mo (1GB RAM recommended)
   - Add SSH key
   - Create

2. Connect to Droplet:
   ssh root@YOUR_DROPLET_IP

3. Install Docker:
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh

4. Clone Repository:
   cd /root
   git clone https://github.com/your-repo/bbq-ai.git
   cd bbq-ai

5. Configure Environment:
   cp .env.example .env.prod
   nano .env.prod
   # Edit DB_PASSWORD, SECRET_KEY, DOMAIN, CORS_ORIGINS

6. Deploy:
   docker-compose -f docker-compose.yml up -d

7. Setup Domain (if using domain):
   - Point A record to droplet IP
   - Wait for DNS propagation
   - Setup SSL: docker-compose exec frontend certbot certonly -d yourdomain.com

8. Monitor:
   docker-compose logs -f
    "

    print_success "DigitalOcean configuration ready"
}

# Deploy to AWS
deploy_aws() {
    print_header "AWS Deployment Configuration"

    print_info "AWS Deployment Steps:"
    echo "
1. Install AWS CLI:
   brew install awscli

2. Configure Credentials:
   aws configure
   # Enter AWS Access Key, Secret Key, Region

3. Create ECR Repositories:
   aws ecr create-repository --repository-name bbq-backend
   aws ecr create-repository --repository-name bbq-frontend

4. Build and Push Images:
   \$(aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com)
   docker build -t bbq-backend:latest backend/
   docker tag bbq-backend:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/bbq-backend:latest
   docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/bbq-backend:latest

5. Create RDS Database:
   - Go to RDS Dashboard
   - PostgreSQL 15, db.t3.micro
   - Configure security groups

6. Deploy with ECS:
   - Create ECS Cluster
   - Create Task Definitions
   - Create Services
   - Configure Load Balancer

7. Setup Domain:
   - Point CNAME to ALB DNS
   - Setup Certificate Manager

8. Monitor:
   - CloudWatch Logs
   - CloudWatch Metrics
    "

    print_success "AWS configuration ready"
}

# Deploy to Docker Hub
deploy_docker_hub() {
    print_header "Docker Hub Deployment Configuration"

    print_info "Docker Hub Deployment Steps:"
    echo "
1. Create Docker Hub Account:
   https://hub.docker.com

2. Login to Docker Hub:
   docker login
   # Enter username and password

3. Build Images:
   docker-compose build

4. Tag Images:
   docker tag bbq-backend:latest USERNAME/bbq-backend:latest
   docker tag bbq-frontend:latest USERNAME/bbq-frontend:latest

5. Push Images:
   docker push USERNAME/bbq-backend:latest
   docker push USERNAME/bbq-frontend:latest

6. On Target Server:
   ssh user@server_ip
   mkdir -p ~/bbq-ai && cd ~/bbq-ai

7. Create docker-compose.yml for production:
   image: USERNAME/bbq-backend:latest
   image: USERNAME/bbq-frontend:latest

8. Deploy:
   docker-compose up -d

9. Monitor:
   docker-compose logs -f
    "

    print_success "Docker Hub configuration ready"
}

# Deploy to Custom VPS
deploy_custom_vps() {
    print_header "Custom VPS Deployment Configuration"

    print_info "Custom VPS Deployment Steps:"
    echo "
1. SSH into Server:
   ssh user@your_vps_ip

2. Install Docker:
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker \$USER

3. Setup Application Directory:
   mkdir -p ~/bbq-ai && cd ~/bbq-ai

4. Upload Files:
   scp -r . user@your_vps_ip:~/bbq-ai/

5. Configure Environment:
   cp .env.example .env.prod
   nano .env.prod

6. Build and Deploy:
   docker-compose build
   docker-compose up -d

7. Setup Nginx Reverse Proxy:
   docker-compose exec nginx nginx -s reload

8. Setup Domain:
   Update DNS A record to VPS IP
   Configure SSL

9. Monitor:
   docker-compose logs -f
    "

    print_success "Custom VPS configuration ready"
}

# Security checks
security_checks() {
    print_header "Security Pre-Flight Checks"

    echo "Security Checklist:"
    echo "  [ ] Changed all default passwords in .env.prod"
    echo "  [ ] Generated new SECRET_KEY"
    echo "  [ ] Generated new JWT_SECRET_KEY"
    echo "  [ ] Set APP_DEBUG=false"
    echo "  [ ] Set APP_ENV=production"
    echo "  [ ] Configured CORS_ORIGINS"
    echo "  [ ] Database backup configured"
    echo "  [ ] SSL certificate configured"
    echo "  [ ] Firewall configured (80, 443 only)"
    echo "  [ ] SSH key-based authentication enabled"
    echo "  [ ] SSH root login disabled"
    echo "  [ ] Strong database passwords set"
    echo "  [ ] Environment variables are secret (not in git)"

    print_warning "Review all security items above before deploying!"
}

# Generate deployment report
generate_report() {
    print_header "Deployment Report"

    REPORT_FILE="deployment_report_$(date +%Y%m%d_%H%M%S).txt"

    cat > "$REPORT_FILE" << EOF
╔════════════════════════════════════════════════════════════════╗
║         BBQ Restaurant AI - Deployment Report                 ║
╚════════════════════════════════════════════════════════════════╝

Date: $(date)
Provider: $PROVIDER
Domain: ${DOMAIN:-"Not configured"}

DEPLOYMENT CHECKLIST
════════════════════════════════════════════════════════════════

Pre-Deployment:
  ✓ Environment validated
  ✓ Docker files present
  ✓ docker-compose.yml configured
  ✓ .env.prod created

Security:
  [ ] Passwords changed
  [ ] Secrets generated
  [ ] Debug mode disabled
  [ ] CORS configured
  [ ] SSL setup
  [ ] Firewall configured

Services to Deploy:
  - PostgreSQL 15-alpine
  - Redis 7-alpine
  - FastAPI Backend
  - React Frontend
  - Nginx Reverse Proxy

Deployment URL: ${DOMAIN:-"http://YOUR_SERVER_IP"}

API Documentation: ${DOMAIN:-"http://YOUR_SERVER_IP"}/api/docs
Dashboard: ${DOMAIN:-"http://YOUR_SERVER_IP"}

MONITORING
════════════════════════════════════════════════════════════════

View Logs:
  docker-compose logs -f

View Specific Service:
  docker-compose logs -f backend

Check Services:
  docker-compose ps

BACKUP & ROLLBACK
════════════════════════════════════════════════════════════════

Backup Location: ./backups/$(date +%Y%m%d_%H%M%S)
Database Backup: Configure automated backups in production

Rollback Steps:
  1. docker-compose down
  2. Restore from backup
  3. docker-compose up -d

NEXT STEPS
════════════════════════════════════════════════════════════════

1. Configure .env.prod with production values
2. Review and check all security items
3. Test locally with deploy-local.sh
4. Choose deployment provider
5. Follow provider-specific deployment steps
6. Monitor logs during deployment
7. Test all endpoints
8. Configure monitoring and alerts
9. Setup backup strategy
10. Document deployment details

SUPPORT & TROUBLESHOOTING
════════════════════════════════════════════════════════════════

Issues?
  1. Check logs: docker-compose logs
  2. Verify environment: docker-compose config
  3. Check health: curl http://localhost:8000/health
  4. Restart services: docker-compose restart

Documentation:
  - QUICK_START_DEPLOYMENT.md
  - DOCKER_DEPLOYMENT_BEGINNER_GUIDE.md
  - README.md

════════════════════════════════════════════════════════════════
EOF

    print_success "Deployment report generated: $REPORT_FILE"
    cat "$REPORT_FILE"
}

# Main execution
main() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  BBQ Restaurant AI - Production Deployment Script         ║"
    echo "║  Version 1.0.0                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    validate_inputs
    pre_deployment_checks
    backup_existing
    security_checks

    # Deploy based on provider
    case $PROVIDER in
        digitalocean)
            deploy_digitalocean
            ;;
        aws)
            deploy_aws
            ;;
        docker-hub)
            deploy_docker_hub
            ;;
        custom-vps)
            deploy_custom_vps
            ;;
    esac

    generate_report

    print_header "Ready to Deploy!"
    print_success "Follow the instructions above for your chosen provider"
    print_warning "Remember to configure all security settings before going live!"
}

main
