# 🔍 Docker Deployment - Monitoring & Troubleshooting Guide

**Date:** 2026-08-31  
**Level:** Beginner-Friendly  
**Last Updated:** 2026-08-31

---

## Table of Contents

1. [Monitoring Overview](#monitoring-overview)
2. [Real-Time Monitoring](#real-time-monitoring)
3. [Log Management](#log-management)
4. [Performance Metrics](#performance-metrics)
5. [Troubleshooting Common Issues](#troubleshooting-common-issues)
6. [Health Checks](#health-checks)
7. [Alerts & Notifications](#alerts--notifications)
8. [Production Monitoring](#production-monitoring)

---

## Monitoring Overview

Monitoring your deployed application ensures:
- Early problem detection
- Performance optimization
- Resource management
- Security compliance
- User experience quality

### Key Metrics to Monitor

```
CPU Usage
Memory Usage
Disk Space
Network I/O
Database Connections
API Response Time
Error Rates
Container Status
```

---

## Real-Time Monitoring

### 1. View All Running Containers

```bash
# Status of all services
docker-compose ps

# Output example:
# NAME           COMMAND              STATE                PORTS
# bbq-postgres   postgres             Up 2 hours           5432/tcp
# bbq-redis      redis-server         Up 2 hours           6379/tcp
# bbq-backend    uvicorn app.main     Up 2 hours           8000/tcp
# bbq-frontend   nginx                Up 2 hours           3000/tcp
```

### 2. Live Resource Usage

```bash
# Real-time container metrics
docker stats

# Output shows:
# CONTAINER ID  NAME         CPU %   MEM USAGE / LIMIT
# abc123def456  bbq-backend  0.15%   145MiB / 2GiB
# def456abc123  bbq-frontend 0.05%   32MiB / 2GiB
# 789ghi012jkl  bbq-postgres 0.20%   256MiB / 2GiB
# 012jkl345mno  bbq-redis    0.10%   8MiB / 2GiB

# Non-streaming version (single snapshot)
docker stats --no-stream
```

### 3. Detailed Container Information

```bash
# Inspect a specific container
docker-compose exec backend env

# View container details
docker inspect bbq-backend

# Get container IP address
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' bbq-backend
```

---

## Log Management

### 1. View Logs

```bash
# All services logs
docker-compose logs

# Follow logs (live)
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
docker-compose logs -f redis

# Logs from last 10 minutes
docker-compose logs --since 10m

# Logs until specific time
docker-compose logs --until 5m
```

### 2. Log Storage

```bash
# Check log file location
docker inspect --format='{{.LogPath}}' bbq-backend

# View raw log file
cat /var/lib/docker/containers/[CONTAINER_ID]/[CONTAINER_ID]-json.log

# Follow in real time
tail -f /var/lib/docker/containers/[CONTAINER_ID]/[CONTAINER_ID]-json.log
```

### 3. Log Rotation Configuration

```yaml
# In docker-compose.yml (already configured)
logging:
  driver: "json-file"
  options:
    max-size: "10m"      # Max log size before rotation
    max-file: "3"        # Keep max 3 log files
```

---

## Performance Metrics

### 1. API Response Times

```bash
# Test API response time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# Custom format file (curl-format.txt):
# time_namelookup:  %{time_namelookup}\n
# time_connect:     %{time_connect}\n
# time_appconnect:  %{time_appconnect}\n
# time_pretransfer: %{time_pretransfer}\n
# time_redirect:    %{time_redirect}\n
# time_starttransfer: %{time_starttransfer}\n
# ─────────────────────────────
# time_total:       %{time_total}\n
```

### 2. Database Performance

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U bbq_user -d bbq_db

# Inside psql:
# Show current connections
SELECT * FROM pg_stat_activity;

# Show slow queries
SELECT query, calls, mean_time FROM pg_stat_statements ORDER BY mean_time DESC;

# Check database size
SELECT pg_database.datname, 
       pg_size_pretty(pg_database_size(pg_database.datname)) 
FROM pg_database;

# List all tables and their sizes
SELECT tablename, pg_size_pretty(pg_total_relation_size(tablename::regclass))
FROM pg_tables
WHERE schemaname='public'
ORDER BY pg_total_relation_size(tablename::regclass) DESC;
```

### 3. Redis Performance

```bash
# Connect to Redis
docker-compose exec redis redis-cli

# Inside redis-cli:
# Get stats
INFO stats

# Check memory usage
INFO memory

# List all keys
KEYS *

# Get key count
DBSIZE

# Monitor Redis commands in real time
MONITOR
```

### 4. Nginx Performance

```bash
# Check Nginx status
docker-compose exec frontend nginx -s reload

# View Nginx access logs
docker-compose logs frontend | grep "GET\|POST"

# Check Nginx configuration
docker-compose exec frontend nginx -t
```

---

## Troubleshooting Common Issues

### Issue 1: Services Won't Start

**Symptoms:**
- `docker-compose ps` shows containers exiting
- Logs show error messages

**Diagnosis:**
```bash
# Check specific service logs
docker-compose logs backend

# Rebuild container
docker-compose build --no-cache backend

# Check for port conflicts
netstat -tulpn | grep 8000
```

**Solution:**
```bash
# Stop all services
docker-compose down

# Remove volumes to start fresh (caution: loses data)
docker-compose down -v

# Rebuild and start
docker-compose build
docker-compose up -d

# Check status
docker-compose ps
```

---

### Issue 2: Database Connection Error

**Symptoms:**
```
ERROR: could not connect to server: Connection refused
```

**Diagnosis:**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Test connection manually
docker-compose exec postgres pg_isready -U bbq_user

# Check network connectivity
docker-compose exec backend ping postgres
```

**Solution:**
```bash
# Verify PostgreSQL environment variables
docker-compose config | grep -A 10 "postgres:"

# Restart PostgreSQL
docker-compose restart postgres

# Check if port 5432 is in use
sudo lsof -i :5432

# Kill process using port if necessary
kill -9 <PID>
```

---

### Issue 3: Memory Leak / High Memory Usage

**Symptoms:**
- `docker stats` shows increasing memory usage
- Application slows down over time
- Out of memory errors

**Diagnosis:**
```bash
# Check memory usage trend
watch -n 5 'docker stats --no-stream | grep backend'

# Check container memory limit
docker inspect backend | grep -i memory

# Check for memory leaks in application
docker-compose exec backend ps aux
```

**Solution:**
```bash
# Restart container
docker-compose restart backend

# Increase memory limit in docker-compose.yml:
services:
  backend:
    mem_limit: 2g
    memswap_limit: 2g

# Rebuild and restart
docker-compose up -d backend

# Monitor after restart
docker stats --no-stream
```

---

### Issue 4: API Not Responding

**Symptoms:**
- `curl http://localhost:8000/health` times out
- Frontend can't reach backend

**Diagnosis:**
```bash
# Check if backend container is running
docker-compose ps backend

# Check backend logs for errors
docker-compose logs backend --tail=50

# Test backend from frontend container
docker-compose exec frontend curl http://backend:8000/health

# Check network connectivity
docker-compose exec backend ping postgres
docker-compose exec backend ping redis

# Check if port 8000 is listening
docker-compose exec backend netstat -tulpn | grep 8000
```

**Solution:**
```bash
# Restart backend
docker-compose restart backend

# Check for dependency issues
docker-compose logs backend

# Verify environment variables
docker-compose exec backend env | grep DATABASE_URL

# Rebuild if configuration changed
docker-compose build backend
docker-compose up -d backend
```

---

### Issue 5: Disk Space Issues

**Symptoms:**
- Docker build fails with "no space left on device"
- Services crash unexpectedly

**Diagnosis:**
```bash
# Check available disk space
df -h

# Check Docker storage usage
docker system df

# Find large images
docker images --format "{{.Repository}}:{{.Tag}}\t{{.Size}}" | sort -k2 -hr

# Find large containers
docker ps -as --format "table {{.Names}}\t{{.Size}}\t{{.SizeRw}}"
```

**Solution:**
```bash
# Remove unused images
docker image prune -a

# Remove unused containers
docker container prune

# Remove unused volumes
docker volume prune

# Remove all unused Docker resources
docker system prune -a

# Check cleanup results
docker system df
```

---

### Issue 6: SSL/HTTPS Certificate Issues

**Symptoms:**
- Browser warning about invalid certificate
- Mixed content warnings
- SSL_CERTIFICATE_VERIFY_FAILED errors

**Diagnosis:**
```bash
# Check certificate expiry
echo | openssl s_client -servername yourdomain.com -connect yourdomain.com:443 2>/dev/null | grep "Issuer\|Expiration"

# Verify certificate
openssl verify /etc/nginx/ssl/cert.pem

# Check certificate files exist
docker-compose exec frontend ls -la /etc/nginx/ssl/
```

**Solution:**
```bash
# Renew certificate with certbot
docker-compose exec frontend certbot renew

# For new certificate
docker-compose exec frontend certbot certonly \
  --standalone \
  -d yourdomain.com \
  -d www.yourdomain.com

# Verify renewal
docker-compose restart frontend
```

---

## Health Checks

### 1. Manual Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "database": "connected", "redis": "connected"}

# Frontend health
curl http://localhost:3000/health

# Database health
docker-compose exec postgres pg_isready -U bbq_user -h postgres

# Redis health
docker-compose exec redis redis-cli ping
# Expected: PONG
```

### 2. Automated Health Checks (already configured)

Health checks are configured in `docker-compose.yml`:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

**Check health status:**
```bash
# View health status
docker-compose ps

# Detailed health info
docker inspect --format='{{json .State.Health}}' bbq-backend | jq '.'
```

### 3. Creating Custom Health Checks

```bash
# Test complete flow
./scripts/test-deployment.sh local

# Run specific tests
docker-compose exec backend curl http://localhost:8000/api/v1/dashboard
docker-compose exec postgres psql -U bbq_user -d bbq_db -c "SELECT COUNT(*) FROM users;"
```

---

## Alerts & Notifications

### 1. Set Up Log Alerts

```bash
# Monitor for errors
docker-compose logs -f | grep -i "error\|warning\|fatal"

# Save errors to file
docker-compose logs -f 2>&1 | tee deployment.log | grep -i "error"

# Check error rate
docker-compose logs | grep -i "error" | wc -l
```

### 2. Alert Rules

Create a monitoring script `scripts/monitor-alerts.sh`:

```bash
#!/bin/bash

# Alert on high memory usage
MEMORY_THRESHOLD=80
USAGE=$(docker stats --no-stream backend --format '{{.MemPerc}}' | sed 's/%//')
if (( $(echo "$USAGE > $MEMORY_THRESHOLD" | bc -l) )); then
    echo "ALERT: Backend memory usage at $USAGE%"
fi

# Alert on failed container
if ! docker-compose ps backend | grep -q "Up"; then
    echo "ALERT: Backend container is not running"
fi

# Alert on low disk space
AVAILABLE=$(df / | tail -1 | awk '{print $4}')
if [ $AVAILABLE -lt 1000000 ]; then
    echo "ALERT: Low disk space: $((AVAILABLE / 1000))MB available"
fi
```

### 3. Run Monitoring in Background

```bash
# Run monitoring script every 5 minutes
*/5 * * * * /path/to/scripts/monitor-alerts.sh >> /var/log/bbq-monitoring.log

# View monitoring logs
tail -f /var/log/bbq-monitoring.log
```

---

## Production Monitoring

### 1. Advanced Monitoring Stack

Install and configure additional tools:

```bash
# Option 1: Prometheus + Grafana
docker run -d --name prometheus prom/prometheus

# Option 2: ELK Stack (Elasticsearch, Logstash, Kibana)
docker run -d --name elasticsearch docker.elastic.co/elasticsearch/elasticsearch:7.14.0

# Option 3: Sentry (Error Tracking)
docker run -d --name sentry getsentry/sentry:latest
```

### 2. Production Checklist

```
□ Monitoring system installed (Prometheus, Datadog, etc.)
□ Log aggregation configured (ELK, Splunk, etc.)
□ Error tracking enabled (Sentry, Rollbar, etc.)
□ Alerts configured for critical metrics
□ Backup strategy implemented
□ Database replication configured
□ CDN configured for static assets
□ SSL certificate auto-renewal set up
□ Rate limiting configured
□ CORS properly configured
□ Database connection pooling optimized
□ Cache hit rate monitored
□ API rate limiting tested
```

### 3. Uptime Monitoring

```bash
# Set up uptime monitoring service
curl -X POST https://uptime-service.com/api/checks \
  -H "Content-Type: application/json" \
  -d '{
    "name": "BBQ AI Dashboard",
    "url": "https://yourdomain.com",
    "interval": 300,
    "alert_threshold": 3
  }'
```

---

## Quick Reference Commands

| Task | Command |
|------|---------|
| **Status** | `docker-compose ps` |
| **Logs** | `docker-compose logs -f` |
| **Metrics** | `docker stats --no-stream` |
| **Restart** | `docker-compose restart` |
| **Rebuild** | `docker-compose build --no-cache` |
| **Clean** | `docker system prune -a` |
| **DB Shell** | `docker-compose exec postgres psql -U bbq_user -d bbq_db` |
| **Redis Shell** | `docker-compose exec redis redis-cli` |
| **Health** | `curl http://localhost:8000/health` |
| **API Docs** | `open http://localhost:8000/docs` |
| **Test** | `./scripts/test-deployment.sh local` |

---

## Summary

**Key Points:**
- Monitor services regularly with `docker stats` and `docker-compose logs`
- Set up automated alerts for critical metrics
- Maintain logs for troubleshooting and auditing
- Test health checks periodically
- Keep backups current
- Plan for scaling as usage grows

**Next Steps:**
1. Set up monitoring for your environment
2. Configure alerts for your team
3. Test disaster recovery procedures
4. Document your monitoring setup
5. Train team on troubleshooting

---

**Generated:** 2026-08-31 13:49 UTC  
**Version:** 1.0.0  
**Status:** Production Ready ✅

