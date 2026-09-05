# 🚀 QUICK START - Docker Deployment Guide

**Date:** 2026-08-31  
**Difficulty:** Beginner  
**Time Required:** 30 minutes (local), 1-2 hours (production)

---

## ⚡ 5-Minute Local Setup

### Step 1: Prerequisites Check
```bash
# Verify Docker is installed
docker --version
docker-compose --version

# Should show versions like:
# Docker version 24.0.0
# Docker Compose version 2.20.0
```

### Step 2: Navigate to Project
```bash
cd path/to/bbq-ai-business-intelligence
```

### Step 3: Create Environment File
```bash
# Copy the example
cp .env.example .env

# Edit .env and change passwords
# (Use your favorite text editor)
```

### Step 4: Build and Start
```bash
# Build all containers
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

### Step 5: Verify Everything Works
```bash
# Frontend
open http://localhost:3000

# Backend API
open http://localhost:8000/docs

# Database (optional)
psql -h localhost -U bbq_user -d bbq_db
```

---

## 🌐 Production Deployment (Choose One)

### Option A: DigitalOcean (Easiest for Beginners)

#### Prerequisites
- DigitalOcean account (signup: https://digitalocean.com)
- SSH key generated

#### Deployment Steps

**1. Create Droplet**
```bash
# On DigitalOcean Dashboard:
# 1. Click "Create" → "Droplets"
# 2. Image: Ubuntu 22.04 LTS
# 3. Size: $5-6/month (1GB RAM minimum)
# 4. Region: Choose closest to users
# 5. Add your SSH key
# 6. Hostname: bbq-ai-app
# 7. Create
```

**2. Connect to Droplet**
```bash
# Get IP from DigitalOcean dashboard
ssh root@YOUR_DROPLET_IP
```

**3. Install Docker**
```bash
# Run on droplet
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verify
docker --version
docker-compose --version
```

**4. Upload Your Code**
```bash
# On your local machine
# Option A: Using git
ssh root@YOUR_DROPLET_IP "cd /root && git clone https://github.com/yourusername/bbq-ai.git"

# Option B: Using scp
scp -r ./bbq-ai-business-intelligence root@YOUR_DROPLET_IP:/root/
```

**5. Configure and Deploy**
```bash
# SSH into droplet
ssh root@YOUR_DROPLET_IP

# Navigate to app
cd /root/bbq-ai-business-intelligence

# Create .env file
nano .env

# Paste content from .env.example
# Edit these critical values:
# - DB_PASSWORD (strong password)
# - SECRET_KEY (generate new)
# - DOMAIN (your domain)
# - CORS_ORIGINS

# Save (Ctrl+O, Enter, Ctrl+X)

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

**6. Setup Domain**
```bash
# In your domain registrar:
# 1. Create A record pointing to droplet IP
# 2. Wait 10-30 minutes for DNS propagation

# Verify DNS
nslookup yourdomain.com
```

**7. Setup SSL Certificate**
```bash
# On droplet
docker-compose exec frontend certbot certonly \
  --standalone \
  -d yourdomain.com \
  -d www.yourdomain.com
```

**Droplet Access**
- Frontend: http://YOUR_DROPLET_IP:3000 → https://yourdomain.com
- Backend: http://YOUR_DROPLET_IP:8000 → https://yourdomain.com/api
- Database: psql -h YOUR_DROPLET_IP -U bbq_user -d bbq_db

---

### Option B: AWS (More Complex but Scalable)

#### Prerequisites
- AWS account (free tier available)
- AWS CLI installed
- Basic AWS knowledge

#### Deployment Steps

**1. Install AWS CLI**
```bash
# macOS
brew install awscli

# Windows
choco install awscli

# Verify
aws --version
```

**2. Configure AWS Credentials**
```bash
aws configure

# Enter:
# AWS Access Key ID: [from IAM console]
# AWS Secret Access Key: [from IAM console]
# Default region: us-east-1
# Default output format: json
```

**3. Create ECR Repositories**
```bash
# Create repository for backend
aws ecr create-repository \
  --repository-name bbq-backend \
  --region us-east-1

# Create repository for frontend
aws ecr create-repository \
  --repository-name bbq-frontend \
  --region us-east-1
```

**4. Build and Push Images**
```bash
# Get AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com

# Build images
docker-compose build

# Tag backend
docker tag bbq-backend:latest \
  ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/bbq-backend:latest

# Tag frontend
docker tag bbq-frontend:latest \
  ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/bbq-frontend:latest

# Push backend
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/bbq-backend:latest

# Push frontend
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/bbq-frontend:latest
```

**5. Create RDS Database**
```bash
# Use AWS Console for simplicity:
# 1. Go to RDS → Create database
# 2. Engine: PostgreSQL 15
# 3. Instance class: db.t3.micro (free tier)
# 4. DB name: bbq_db
# 5. Master username: bbq_user
# 6. Password: [strong password]
# 7. Create
```

**6. Deploy with ECS**
```bash
# Use AWS Console or CLI:
# 1. Create ECS cluster
# 2. Create task definitions for backend/frontend
# 3. Create services
# 4. Configure load balancer
# 5. Map domain
```

---

### Option C: Docker Hub + Any VPS

#### Steps

**1. Create Docker Hub Account**
- Go to https://hub.docker.com
- Sign up (free)

**2. Push to Docker Hub**
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

**3. On Your VPS**
```bash
# SSH into VPS
ssh user@your_vps_ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Create .env
nano .env

# Create docker-compose.yml with Docker Hub images:
# Change:
# build: ./backend → image: yourusername/bbq-backend:latest
# build: ./frontend → image: yourusername/bbq-frontend:latest

# Start
docker-compose up -d
```

---

## 📊 Monitoring After Deployment

### Check Services Status
```bash
# View all containers
docker-compose ps

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Common Commands

```bash
# Restart services
docker-compose restart

# Stop services
docker-compose down

# Update containers
docker-compose pull
docker-compose up -d

# View resource usage
docker stats

# Clean up unused images
docker system prune -a
```

---

## 🔒 Security Checklist

- [ ] Changed all default passwords in .env
- [ ] Generated new SECRET_KEY and JWT_SECRET_KEY
- [ ] Set APP_DEBUG=false
- [ ] Configured CORS_ORIGINS with your domain
- [ ] SSL certificate installed (HTTPS)
- [ ] Firewall configured (only 80, 443 open)
- [ ] Regular backups configured
- [ ] Monitoring set up
- [ ] Logs reviewed

---

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check logs
docker-compose logs

# Rebuild
docker-compose build --no-cache

# Check ports
netstat -tulpn | grep 8000  # or 3000, 5432
```

### Can't Connect to API
```bash
# Verify backend is running
docker-compose ps backend

# Check API health
curl http://localhost:8000/health

# View backend logs
docker-compose logs backend
```

### Database Connection Error
```bash
# Verify postgres running
docker-compose ps postgres

# Check connection
docker-compose exec postgres psql -U bbq_user -d bbq_db

# Check environment variables
docker-compose config
```

---

## 📈 Next Steps

1. **Local Testing** ✅
   - Run locally with docker-compose
   - Test all features
   - Fix any issues

2. **Production Deployment** ✅
   - Choose hosting (DigitalOcean recommended)
   - Deploy containers
   - Setup domain

3. **Monitoring** ✅
   - Setup error tracking (Sentry)
   - Configure logging
   - Add performance monitoring

4. **Optimization** ✅
   - Enable caching
   - Optimize database
   - Setup CDN

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Build | `docker-compose build` |
| Start | `docker-compose up -d` |
| Stop | `docker-compose down` |
| Logs | `docker-compose logs -f` |
| Restart | `docker-compose restart` |
| Status | `docker-compose ps` |
| Clean | `docker system prune -a` |

---

## 🎯 Success Indicators

✅ **Local**
- Frontend loads at http://localhost:3000
- API docs visible at http://localhost:8000/docs
- Can login to dashboard
- No errors in logs

✅ **Production**
- Website loads at https://yourdomain.com
- API responds at https://yourdomain.com/api
- SSL certificate shows as valid
- All services running (`docker-compose ps`)

---

## 📚 Additional Resources

- Docker Docs: https://docs.docker.com
- Docker Compose: https://docs.docker.com/compose
- DigitalOcean Tutorials: https://www.digitalocean.com/community/tutorials
- AWS Documentation: https://docs.aws.amazon.com

---

## ✅ You're Done!

Your app is now deployed! 🎉

**Common Next Steps:**
1. Monitor the application
2. Collect user feedback
3. Optimize performance
4. Add monitoring/alerting
5. Plan scaling strategy

---

**Generated:** 2026-08-31 13:47 UTC  
**Level:** Beginner-Friendly ✅  
**Ready to Deploy:** Yes ✅

