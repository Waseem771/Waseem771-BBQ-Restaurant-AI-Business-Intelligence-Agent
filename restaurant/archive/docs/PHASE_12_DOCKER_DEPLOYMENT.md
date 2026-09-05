# Phase 12: Docker & Production Deployment

**BBQ Restaurant AI Business Intelligence Agent**  
**Phase 12: Docker & Production Deployment**  
**Date: 2026-08-31**  
**Status: Ready for Implementation**

---

## Table of Contents

1. [Overview](#overview)
2. [What is Docker](#what-is-docker)
3. [Architecture](#architecture)
4. [Files to Create](#files-to-create)
5. [File-by-File Instructions](#file-by-file-instructions)
6. [Deployment Steps](#deployment-steps)
7. [Commands Reference](#commands-reference)
8. [Troubleshooting](#troubleshooting)
9. [Future Changes Guide](#future-changes-guide)

---

## Overview

### What Phase 12 Does

Phase 12 containerizes your BBQ Restaurant AI BI application using Docker and Docker Compose for production deployment.

**Before Phase 12:**
- Run app locally: `python -m uvicorn app.main:app --port 8000`
- Manual setup on each server
- Different behavior on different machines

**After Phase 12:**
- Run app anywhere: `docker-compose up`
- Same behavior everywhere
- Easy deployment and scaling

### Key Components

1. **Dockerfile** - Instructions to build container image
2. **docker-compose.yml** - Defines all services (API, Nginx, etc.)
3. **nginx.conf** - Web server configuration
4. **.dockerignore** - Files to exclude from container
5. **.env.production** - Production environment variables

---

## What is Docker

### Simple Explanation

Docker is like a **complete package** containing:
- Your Python code
- Python 3.11
- All libraries (FastAPI, requests, etc.)
- Configuration files
- Everything needed to run

### Without Docker (Problem)

```
Your computer → Works perfectly
Colleague's computer → Missing library X → Breaks
Production server → Different Python version → Breaks
```

### With Docker (Solution)

```
Your computer → Docker container → Works
Colleague's computer → Same Docker container → Works
Production server → Same Docker container → Works
```

### Container vs Virtual Machine

**Container:** Lightweight, shares OS kernel, starts in seconds
**Virtual Machine:** Heavy, separate OS, takes minutes

Docker uses containers (much better for this).

---

## Architecture

### Services Overview

```
┌─────────────────────────────────────────────┐
│         Internet (Port 80/443)              │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│   Nginx Container (Reverse Proxy)           │
│   - Handles HTTP requests                   │
│   - Routes to FastAPI                       │
│   - Logs access                             │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│   FastAPI Container (Application)           │
│   - Your BBQ AI BI application              │
│   - All Phase 1-11 code                     │
│   - Port 8000 (internal)                    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│   SQLite Database (Shared Volume)           │
│   - data/bbq.db                             │
│   - Persists between restarts               │
└─────────────────────────────────────────────┘
```

### How It Works

1. User accesses: `http://example.com`
2. Nginx receives request on port 80
3. Nginx forwards to FastAPI on port 8000
4. FastAPI processes request, accesses SQLite
5. Response sent back through Nginx to user

---

## Files to Create

### File Structure

```
project-root/
├── Dockerfile                 ← NEW
├── docker-compose.yml         ← NEW
├── nginx.conf                 ← NEW
├── .dockerignore              ← NEW
├── .env.production            ← NEW
├── .env.example               ← EXISTING
├── requirements.txt           ← EXISTING
├── app/                       ← EXISTING
│   ├── main.py
│   ├── ml/
│   │   ├── models.py
│   │   ├── registry.py
│   │   └── loader.py
│   └── api/
│       └── routes/
│           ├── models.py
│           └── ...
├── data/                      ← CREATED BY DOCKER
│   └── bbq.db
└── logs/                      ← CREATED BY DOCKER
    └── (log files)
```

---

## File-by-File Instructions

### 1. Dockerfile

**Purpose:** Instructions to build the container image

**Location:** `Dockerfile` (no extension, in project root)

**Content:**

```dockerfile
# Stage 1: Builder
# Compiles dependencies to reduce final image size
FROM python:3.11-slim as builder

WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
# Final container with only what's needed
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Create required directories
RUN mkdir -p /app/data /app/logs

# Set environment variables
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production

# Health check - container is considered healthy if this passes
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port 8000
EXPOSE 8000

# Command to run when container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
```

**How to use:**
- Already configured for your project
- Builds in 2 stages to reduce image size
- Installs requirements automatically
- Runs health check every 30 seconds

**When to modify:**
- Add system dependencies: Edit `apt-get install` line in Stage 2
- Change Python version: Change `3.11` to desired version
- Change startup command: Modify the `CMD` line at end

---

### 2. docker-compose.yml

**Purpose:** Define and run multiple containers

**Location:** `docker-compose.yml` (in project root)

**Content:**

```yaml
version: '3.8'

services:
  # FastAPI Application
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: bbq_api
    image: bbq-api:latest
    ports:
      - "8000:8000"  # External port : Internal port
    environment:
      # Environment variables inside container
      APP_ENV: production
      DATABASE_URL: sqlite:///./data/bbq.db
      LOG_LEVEL: info
    volumes:
      # Share folders between host and container
      - ./data:/app/data           # Database folder
      - ./logs:/app/logs           # Log folder
    restart: unless-stopped        # Restart if crashes
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - bbq_network                # Connect to network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: bbq_nginx
    ports:
      - "80:80"                    # HTTP
      - "443:443"                  # HTTPS (setup later)
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro  # Config file (read-only)
      - ./logs/nginx:/var/log/nginx             # Nginx logs
    depends_on:
      - api                        # Start api first
    restart: unless-stopped
    networks:
      - bbq_network

# Network for containers to communicate
networks:
  bbq_network:
    driver: bridge
```

**How to use:**
- Run: `docker-compose up`
- Start in background: `docker-compose up -d`
- Stop: `docker-compose down`

**When to modify:**
- Add new service: Copy `api` section, rename, configure
- Change ports: Modify `ports:` values
- Add volumes: Add line under `volumes:`
- Change image version: Modify `image:` line

---

### 3. nginx.conf

**Purpose:** Configure web server to route traffic

**Location:** `nginx.conf` (in project root)

**Content:**

```nginx
# Nginx configuration for BBQ AI BI

# Worker processes
events {
    worker_connections 1024;  # Max connections per worker
}

# HTTP server
http {
    # Define upstream server (FastAPI)
    upstream api {
        server api:8000;  # Container name : Port
    }

    # HTTP server block
    server {
        # Listen on port 80
        listen 80;
        server_name _;              # Accept all domain names
        client_max_body_size 10M;   # Max upload size

        # Logging
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        # Main API routes
        location / {
            # Forward all requests to FastAPI
            proxy_pass http://api;
            
            # Set headers so FastAPI knows real client info
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # WebSocket support (for real-time updates)
        location /ws {
            proxy_pass http://api;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Health check endpoint
        location /health {
            proxy_pass http://api;
            access_log off;           # Don't log health checks
        }
    }
}
```

**How to use:**
- Already configured for your project
- Handles HTTP on port 80
- Supports WebSockets
- Logs all requests

**When to modify:**
- Add HTTPS (SSL): Add second `server` block on port 443
- Change port: Modify `listen 80` line
- Change timeouts: Modify `proxy_*_timeout` values
- Add new route: Add `location /path { ... }` block

---

### 4. .dockerignore

**Purpose:** Exclude files from Docker build (keeps image small)

**Location:** `.dockerignore` (in project root)

**Content:**

```
# Python cache
__pycache__
*.pyc
*.pyo
*.pyd
.Python

# Virtual environments
env/
venv/
.venv
ENV/

# Environment files
.env
.env.local
.env.*.local

# Git
.git
.gitignore
.gitattributes

# OS
.DS_Store
Thumbs.db

# Database (local, will be created)
*.db
data/

# Logs
logs/

# Testing
.pytest_cache
.coverage
htmlcov/
.tox/

# Build
*.egg-info
dist/
build/

# IDE
.vscode
.idea
*.swp
*.swo

# Documentation
README.md
docs/

# CI/CD
.github/
.gitlab-ci.yml
```

**How to use:**
- Already complete for your project
- Automatically used by Docker

**When to modify:**
- Add files to ignore: Add new line with pattern
- Example: Add `__pycache__/` if not already present

---

### 5. .env.production

**Purpose:** Production environment variables (secrets and configuration)

**Location:** `.env.production` (in project root)

**Content:**

```env
# Application Settings
APP_ENV=production
DEBUG=false
LOG_LEVEL=info

# Database
DATABASE_URL=sqlite:///./data/bbq.db

# Security (CHANGE THESE IN PRODUCTION!)
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here-change-in-production

# LLM Configuration (if using)
LLM_API_KEY=your-api-key-here
LLM_PROVIDER=anthropic

# Monitoring
ENABLE_MONITORING=true
METRICS_PORT=9090

# Email (for alerts)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL=admin@example.com
```

**How to use:**
- Load: `docker-compose` automatically uses this file
- Don't commit to git: Add to `.gitignore`

**When to modify:**
- Change database path: Update `DATABASE_URL`
- Change log level: Update `LOG_LEVEL` (debug, info, warning, error)
- Add API keys: Add new lines as needed
- Change secrets: Update `SECRET_KEY` and `JWT_SECRET_KEY`

---

## Deployment Steps

### Step 1: Prepare Files

Create all 5 files in project root:
- [ ] `Dockerfile`
- [ ] `docker-compose.yml`
- [ ] `nginx.conf`
- [ ] `.dockerignore`
- [ ] `.env.production`

### Step 2: Test Locally

**Build image:**
```bash
docker build -t bbq-api:latest .
```

**Start services:**
```bash
docker-compose up
```

**Test in another terminal:**
```bash
curl http://localhost/health
```

**Expected response:**
```json
{"status": "healthy", "database": "connected"}
```

### Step 3: Deploy to Production Server

**SSH into server:**
```bash
ssh user@your-server.com
```

**Clone repository:**
```bash
git clone <your-repo-url>
cd bbq-ai-business-intelligence
```

**Copy production env file:**
```bash
cp .env.example .env.production
# Edit with production values
nano .env.production
```

**Start services:**
```bash
docker-compose up -d
```

**Check status:**
```bash
docker-compose ps
```

### Step 4: Monitor

**View logs:**
```bash
docker-compose logs -f api
```

**Check health:**
```bash
curl http://your-server.com/health
```

---

## Commands Reference

### Building

```bash
# Build image
docker build -t bbq-api:latest .

# Build without cache
docker build --no-cache -t bbq-api:latest .
```

### Running

```bash
# Start all services in foreground (see logs)
docker-compose up

# Start all services in background
docker-compose up -d

# Start specific service
docker-compose up api

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Monitoring

```bash
# View logs from all services
docker-compose logs

# Follow logs (live)
docker-compose logs -f

# Logs from specific service
docker-compose logs -f api

# Last 100 lines
docker-compose logs -f api --tail=100

# View running containers
docker-compose ps

# View container stats
docker stats
```

### Debugging

```bash
# Execute command in running container
docker-compose exec api bash

# View events
docker-compose events

# Validate compose file
docker-compose config

# Check service status
docker-compose ps api
```

### Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a
```

---

## Troubleshooting

### Issue 1: Port Already in Use

**Error:** `Error response from daemon: driver failed programming external connectivity`

**Solution:**
```bash
# Find what's using port 80
lsof -i :80
# Or on Windows
netstat -ano | findstr :80

# Kill the process or use different port
# Change in docker-compose.yml:
# ports:
#   - "8080:80"  # Use 8080 instead
```

### Issue 2: Container Won't Start

**Error:** `Container exited with code 1`

**Solution:**
```bash
# Check logs
docker-compose logs api

# Rebuild image
docker-compose build --no-cache

# Start fresh
docker-compose down -v
docker-compose up
```

### Issue 3: Database Connection Error

**Error:** `No such file or directory: /app/data/bbq.db`

**Solution:**
```bash
# Check volumes are mounted
docker-compose exec api ls -la /app/data/

# If missing, create directory
mkdir -p data/

# Restart services
docker-compose restart
```

### Issue 4: Nginx 502 Bad Gateway

**Error:** `502 Bad Gateway` when accessing http://localhost

**Solution:**
```bash
# Check if api container is running
docker-compose ps

# Check api logs
docker-compose logs api

# Check nginx logs
docker-compose logs nginx

# Restart api
docker-compose restart api
```

### Issue 5: Health Check Failing

**Error:** `unhealthy` status in `docker-compose ps`

**Solution:**
```bash
# Check if API is responding
docker-compose exec api curl http://localhost:8000/health

# Check logs
docker-compose logs api

# Increase health check timeout
# Edit docker-compose.yml:
# healthcheck:
#   start_period: 60s  # Increase from 40s
```

---

## Future Changes Guide

### Scenario 1: Add a New Service (e.g., Redis Cache)

**Step 1: Add to docker-compose.yml**
```yaml
services:
  redis:
    image: redis:latest
    container_name: bbq_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - bbq_network

volumes:
  redis_data:
```

**Step 2: Connect from API**
```python
# In your code
import redis
r = redis.Redis(host='redis', port=6379, db=0)
```

**Step 3: Restart**
```bash
docker-compose up -d
```

---

### Scenario 2: Update Python Dependencies

**Step 1: Update requirements.txt**
```bash
pip freeze > requirements.txt
```

**Step 2: Rebuild image**
```bash
docker-compose build --no-cache
```

**Step 3: Restart services**
```bash
docker-compose up -d
```

---

### Scenario 3: Change Environment Variable

**Step 1: Edit .env.production**
```env
LOG_LEVEL=debug  # Changed from info
```

**Step 2: Restart services**
```bash
docker-compose up -d
```

**Step 3: Verify**
```bash
docker-compose logs -f api | grep "level"
```

---

### Scenario 4: Enable HTTPS (SSL/TLS)

**Step 1: Add SSL certificate**
```bash
mkdir -p certs
# Copy your certificate and key files
cp /path/to/cert.pem certs/
cp /path/to/key.pem certs/
```

**Step 2: Update nginx.conf**
```nginx
server {
    listen 443 ssl;
    ssl_certificate /etc/nginx/certs/cert.pem;
    ssl_certificate_key /etc/nginx/certs/key.pem;
    # ... rest of config
}
```

**Step 3: Update docker-compose.yml**
```yaml
nginx:
  volumes:
    - ./certs:/etc/nginx/certs:ro
```

**Step 4: Restart**
```bash
docker-compose up -d
```

---

### Scenario 5: Increase Resource Limits

**Edit docker-compose.yml:**
```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

---

### Scenario 6: Add Database Backup

**Step 1: Create backup script**
```bash
#!/bin/bash
mkdir -p backups
cp data/bbq.db backups/bbq.db.$(date +%Y%m%d_%H%M%S)
```

**Step 2: Schedule with cron**
```bash
0 2 * * * /path/to/backup.sh  # Daily at 2 AM
```

---

### Scenario 7: Add Monitoring (Prometheus)

**Add to docker-compose.yml:**
```yaml
prometheus:
  image: prom/prometheus:latest
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
  networks:
    - bbq_network
```

---

## Production Checklist

- [ ] All 5 files created
- [ ] .env.production configured with real values
- [ ] SECRET_KEY changed to unique value
- [ ] Database directory created: `mkdir -p data`
- [ ] Logs directory created: `mkdir -p logs`
- [ ] Tested locally: `docker-compose up`
- [ ] Health check passes: `curl http://localhost/health`
- [ ] API responds: `curl http://localhost/api/v1/dashboard/kpis`
- [ ] Nginx forwards correctly
- [ ] WebSocket works: Can connect to `/ws` endpoints
- [ ] Logs are written to `logs/` directory
- [ ] Database persists after restart
- [ ] All services restart on failure
- [ ] Documentation updated for team
- [ ] Backups configured
- [ ] Monitoring setup (optional)
- [ ] HTTPS enabled (optional but recommended)

---

## Summary

**Phase 12 provides:**
- Complete containerization ✓
- Production-ready configuration ✓
- Easy deployment anywhere ✓
- Simple monitoring and logging ✓
- Web server (Nginx) ✓
- Health checks ✓
- Auto-restart on failure ✓

**After Phase 12, you can:**
- Deploy with: `docker-compose up -d`
- Monitor with: `docker-compose logs -f`
- Manage easily: Simple commands
- Scale easily: Add more services as needed

---

## Files Checklist

- [ ] Dockerfile
- [ ] docker-compose.yml
- [ ] nginx.conf
- [ ] .dockerignore
- [ ] .env.production

**Status: Ready for Production Deployment**

---

*Phase 12: Docker & Production Deployment*  
**Date:** 2026-08-31  
**Version:** 1.0  
**Status:** Complete  
**Next Phase:** Phase 13 (Monitoring & Logging - Future)
