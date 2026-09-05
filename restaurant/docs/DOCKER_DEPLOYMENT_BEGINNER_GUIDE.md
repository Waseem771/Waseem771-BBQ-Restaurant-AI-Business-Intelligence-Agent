# 🐳 Docker Deployment Guide - Complete Beginner Tutorial

**Date:** 2026-08-31  
**Level:** Beginner-Friendly  
**Goal:** Deploy BBQ AI to production using Docker

---

## 📚 What is Docker?

Think of Docker as a **shipping container for your application**:
- 📦 Packages your app + all dependencies
- 🚀 Runs the same everywhere (your PC, server, cloud)
- 🔒 Isolated and secure
- ⚡ Easy to deploy and scale

---

## 🛠️ Prerequisites (Install These First)

### For Windows/Mac
1. **Docker Desktop**
   - Download: https://www.docker.com/products/docker-desktop
   - Install it (follow wizard)
   - Takes 5-10 minutes

2. **Git** (probably already have)
   - Or use PowerShell/Terminal directly

### Verify Installation
```bash
# Open Terminal/PowerShell and type:
docker --version
# Should show: Docker version XX.XX.XX

docker-compose --version
# Should show: Docker Compose version XX.XX.XX
```

---

## 📁 Project Structure

Your project should have:
```
bbq-ai-business-intelligence/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── Dockerfile
│   └── vite.config.js
└── docker-compose.yml (main orchestration)
```

---

## 🐳 Step 1: Create Backend Dockerfile

Create file: `backend/Dockerfile`

```dockerfile
# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (FastAPI default)
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**What this does:**
- Uses Python 3.11 as base
- Installs dependencies
- Runs FastAPI server on port 8000

---

## 🐳 Step 2: Create Frontend Dockerfile

Create file: `frontend/Dockerfile`

```dockerfile
# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build production bundle
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files to nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 3000

# Run nginx
CMD ["nginx", "-g", "daemon off;"]
```

**What this does:**
- Stage 1: Build the app
- Stage 2: Serve with Nginx (lightweight web server)
- Result: Small, optimized container

---

## 🔧 Step 3: Create Nginx Config for Frontend

Create file: `frontend/nginx.conf`

```nginx
server {
    listen 3000;
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }
    location /api {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**What this does:**
- Serves frontend on port 3000
- Routes `/api` to backend
- Handles Vue/React routing

---

## 🐳 Step 4: Create Main docker-compose.yml

Create file: `docker-compose.yml` (in project root)

```yaml
version: '3.8'

services:
  # Backend Service
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: bbq-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/bbq_db
      - REDIS_URL=redis://redis:6379
      - APP_ENV=production
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
    restart: unless-stopped
    networks:
      - bbq-network

  # Frontend Service
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: bbq-frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - bbq-network

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: bbq-postgres
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=bbq_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - bbq-network

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: bbq-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - bbq-network

  # Nginx Reverse Proxy (Optional, for production)
  nginx:
    image: nginx:alpine
    container_name: bbq-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
    networks:
      - bbq-network

volumes:
  postgres_data:
  redis_data:

networks:
  bbq-network:
    driver: bridge
```

**What this does:**
- Defines all services (Backend, Frontend, Database, Cache, Nginx)
- Sets up networking between containers
- Manages volumes for persistent data
- Configures ports and environment variables

---

## 🚀 Step 5: Build and Run Locally

### Option A: Build Everything

```bash
# Navigate to project root
cd path/to/bbq-ai-business-intelligence

# Build all containers
docker-compose build

# Run all services
docker-compose up -d

# Check status
docker-compose ps
```

### Option B: Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove everything (careful!)
docker-compose down -v
```

### Check if Running

```bash
# List running containers
docker ps

# Frontend should be at: http://localhost:3000
# Backend at: http://localhost:8000
# Database at: localhost:5432
```

---

## ✅ Testing Locally

### 1. Check Frontend
```bash
# Open browser
http://localhost:3000

# Should see dashboard
```

### 2. Check Backend API
```bash
# Open browser
http://localhost:8000/docs

# Should see FastAPI docs
```

### 3. Check Database
```bash
# Connect to PostgreSQL
psql -h localhost -U user -d bbq_db

# List tables
\dt
```

---

## 🌐 Deploy to Production

### Option 1: AWS (Recommended for Beginners)

#### Step 1: Create AWS Account
- Go to https://aws.amazon.com
- Sign up (free tier available)

#### Step 2: Use ECS (Elastic Container Service)
```bash
# Install AWS CLI
# Windows: choco install awscli
# Mac: brew install awscli

# Configure credentials
aws configure

# Enter:
# AWS Access Key ID: [from your AWS account]
# AWS Secret Access Key: [from your AWS account]
# Default region: us-east-1
# Default output format: json
```

#### Step 3: Push to ECR (Elastic Container Registry)
```bash
# Create ECR repository
aws ecr create-repository --repository-name bbq-backend
aws ecr create-repository --repository-name bbq-frontend

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [YOUR_AWS_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com

# Tag images
docker tag bbq-backend:latest [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/bbq-backend:latest
docker tag bbq-frontend:latest [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/bbq-frontend:latest

# Push images
docker push [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/bbq-backend:latest
docker push [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/bbq-frontend:latest
```

#### Step 4: Deploy on ECS
- Go to AWS Console → ECS
- Create Cluster
- Create Task Definition
- Create Service
- Configure Load Balancer

### Option 2: DigitalOcean (Simpler)

#### Step 1: Create Account
- Go to https://www.digitalocean.com
- Sign up

#### Step 2: Create Droplet
```bash
# 1. Click "Create" → "Droplets"
# 2. Choose image: Ubuntu 22.04
# 3. Choose size: $6/month minimum
# 4. Choose region: Closest to you
# 5. Add SSH key
# 6. Click "Create Droplet"
```

#### Step 3: Install Docker on Droplet
```bash
# SSH into your droplet
ssh root@your_droplet_ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

#### Step 4: Upload Your Code
```bash
# From your local machine
git clone your-repo-url
cd your-repo
docker-compose up -d
```

### Option 3: Docker Hub + Any Server

#### Step 1: Create Docker Hub Account
- Go to https://hub.docker.com
- Sign up (free)

#### Step 2: Push Images
```bash
# Login
docker login

# Tag images
docker tag bbq-backend:latest yourusername/bbq-backend:latest
docker tag bbq-frontend:latest yourusername/bbq-frontend:latest

# Push
docker push yourusername/bbq-backend:latest
docker push yourusername/bbq-frontend:latest
```

#### Step 3: Pull and Run on Server
```bash
# On your production server
docker pull yourusername/bbq-backend:latest
docker pull yourusername/bbq-frontend:latest
docker-compose up -d
```

---

## 🔒 Production Best Practices

### 1. Environment Variables
Create `.env` file:
```env
# Backend
DATABASE_URL=postgresql://user:secure_password@postgres:5432/bbq_db
REDIS_URL=redis://redis:6379
API_SECRET_KEY=your_secret_key_here
APP_ENV=production

# Frontend
VITE_API_URL=https://your-domain.com/api
```

### 2. Security
```yaml
# In docker-compose.yml
services:
  backend:
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_SECRET_KEY=${API_SECRET_KEY}
    # Don't expose ports directly in production
    # Use nginx reverse proxy instead
```

### 3. SSL Certificate (HTTPS)
```bash
# Use Let's Encrypt with Certbot
docker run -it --rm \
  -v /etc/letsencrypt:/etc/letsencrypt \
  certbot/certbot certonly --standalone \
  -d yourdomain.com
```

### 4. Monitoring & Logs
```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Use tools like ELK Stack or Datadog
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find what's using port 8000
netstat -tulpn | grep 8000

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
# ports:
#   - "8001:8000"  # Use 8001 instead
```

### Container Won't Start
```bash
# Check logs
docker-compose logs backend

# Rebuild without cache
docker-compose build --no-cache

# Run with verbose output
docker-compose up (without -d flag)
```

### Database Connection Error
```bash
# Verify postgres is running
docker-compose ps

# Check environment variables
docker exec bbq-backend env

# Verify connection string
# Should be: postgresql://user:password@postgres:5432/dbname
```

### Frontend Can't Connect to Backend
```bash
# Check nginx proxy settings
# Edit frontend/nginx.conf

location /api {
    proxy_pass http://backend:8000;  # backend is container name
}
```

---

## ✅ Production Deployment Checklist

- [ ] Docker installed locally
- [ ] Docker Compose installed
- [ ] Project has all Dockerfiles
- [ ] docker-compose.yml created
- [ ] Environment variables configured
- [ ] Tested locally (docker-compose up -d)
- [ ] SSL certificate obtained
- [ ] Server/hosting account created
- [ ] Docker installed on server
- [ ] Code pushed to repository
- [ ] Images built and pushed to Docker Hub/ECR
- [ ] Services running on production server
- [ ] Domain configured
- [ ] Monitoring set up
- [ ] Backups configured

---

## 🎯 Quick Start Commands

```bash
# Local Development
docker-compose up -d              # Start all services
docker-compose ps                 # Check status
docker-compose logs -f            # View logs
docker-compose down               # Stop all services

# Production on Server
docker pull yourusername/bbq-backend:latest
docker pull yourusername/bbq-frontend:latest
docker-compose up -d              # Start in background

# Maintenance
docker-compose exec backend bash  # Access backend container
docker-compose exec postgres psql # Access database
docker system prune -a            # Clean up unused images/containers
```

---

## 📞 Getting Help

### Common Issues
1. **Port already in use** → Change port in docker-compose.yml
2. **Container won't start** → Check logs with `docker-compose logs`
3. **Database connection failed** → Verify DATABASE_URL environment variable
4. **Frontend can't reach API** → Check nginx proxy settings

### Resources
- Docker Docs: https://docs.docker.com
- Docker Compose: https://docs.docker.com/compose
- AWS ECS: https://aws.amazon.com/ecs
- DigitalOcean: https://digitalocean.com/docs

---

## 🎉 You're Ready!

This guide covers everything a beginner needs to deploy production Docker.

**Next Steps:**
1. ✅ Read this guide completely
2. ✅ Install Docker Desktop
3. ✅ Create Dockerfile for backend
4. ✅ Create Dockerfile for frontend
5. ✅ Test locally with docker-compose
6. ✅ Choose hosting provider
7. ✅ Deploy!

**Questions?** Each section has troubleshooting and common issues.

---

**Generated:** 2026-08-31 13:46 UTC  
**Level:** Beginner-Friendly ✅  
**Completeness:** Comprehensive ✅  
**Ready to Deploy:** Yes ✅

