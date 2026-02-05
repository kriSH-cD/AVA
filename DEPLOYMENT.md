# Deployment Guide for College Domain

This guide explains how to deploy the AVA ML API Docker image on your college domain.

## 🎯 Overview

**Image Location**: `ghcr.io/zaheer-zee/ava-ml-api:latest`
**Platforms**: linux/amd64, linux/arm64
**Port**: 8000
**Requirements**: Docker, Internet connection

---

## 📦 Option 1: Docker Run (Simple)

### On College Server

```bash
# 1. Pull the image
docker pull ghcr.io/zaheer-zee/ava-ml-api:latest

# 2. Create environment file
cat > .env << EOF
API_KEY=AVA-2026-910728
HOST=0.0.0.0
PORT=8000
EOF

# 3. Run the container
docker run -d \
  --name ava-ml-api \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  ghcr.io/zaheer-zee/ava-ml-api:latest

# 4. Check status
docker ps
docker logs ava-ml-api

# 5. Test
curl http://localhost:8000/health
```

### Access via Domain

If your college domain is `ml.college.edu`:
- Configure reverse proxy (nginx/Apache) to forward to port 8000
- Or use Docker port mapping: `-p 80:8000`

---

## 📦 Option 2: Docker Compose (Recommended)

### Create `docker-compose.yml` on Server

```yaml
version: '3.8'

services:
  ava-ml-api:
    image: ghcr.io/zaheer-zee/ava-ml-api:latest
    container_name: ava-ml-api
    ports:
      - "8000:8000"
    environment:
      - API_KEY=AVA-2026-910728
      - HOST=0.0.0.0
      - PORT=8000
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Deploy

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 📦 Option 3: Kubernetes (Advanced)

### Create `deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ava-ml-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ava-ml-api
  template:
    metadata:
      labels:
        app: ava-ml-api
    spec:
      containers:
      - name: ava-ml-api
        image: ghcr.io/zaheer-zee/ava-ml-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: API_KEY
          value: "AVA-2026-910728"
        - name: HOST
          value: "0.0.0.0"
        - name: PORT
          value: "8000"
---
apiVersion: v1
kind: Service
metadata:
  name: ava-ml-api
spec:
  selector:
    app: ava-ml-api
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Deploy

```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl get services
```

---

## 🌐 Nginx Reverse Proxy Setup

If deploying on `ml.college.edu`:

### Nginx Config

```nginx
server {
    listen 80;
    server_name ml.college.edu;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Enable and Restart

```bash
sudo ln -s /etc/nginx/sites-available/ava-ml-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 HTTPS Setup (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d ml.college.edu

# Auto-renewal is configured automatically
```

---

## 📊 Monitoring

### Check Container Health

```bash
# Container status
docker ps

# Logs
docker logs -f ava-ml-api

# Resource usage
docker stats ava-ml-api

# Health endpoint
curl http://localhost:8000/health
```

### Expected Response

```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_trained": true
}
```

---

## 🔄 Updates

### Pull Latest Version

```bash
# Stop current container
docker stop ava-ml-api
docker rm ava-ml-api

# Pull latest image
docker pull ghcr.io/zaheer-zee/ava-ml-api:latest

# Restart
docker run -d \
  --name ava-ml-api \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  ghcr.io/zaheer-zee/ava-ml-api:latest
```

### With Docker Compose

```bash
docker-compose pull
docker-compose up -d
```

---

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs ava-ml-api

# Common issues:
# - Port 8000 already in use
# - Missing .env file
# - Insufficient memory
```

### Can't Pull Image

```bash
# Make package public on GitHub
# Or login to GHCR:
docker login ghcr.io -u zaheer-zee
```

### API Not Responding

```bash
# Check if container is running
docker ps

# Check port mapping
docker port ava-ml-api

# Test locally first
curl http://localhost:8000/health
```

---

## 📋 Checklist for College IT Team

- [ ] Docker installed on server
- [ ] Port 8000 available (or configure different port)
- [ ] Internet access (for language detection)
- [ ] Domain configured (ml.college.edu)
- [ ] Nginx/reverse proxy configured
- [ ] SSL certificate (optional but recommended)
- [ ] Firewall rules allow port 80/443
- [ ] Environment variables set
- [ ] Health check endpoint accessible

---

## 📞 Support Information

**Image**: `ghcr.io/zaheer-zee/ava-ml-api:latest`
**Documentation**: https://github.com/zaheer-zee/AVA
**Health Check**: `GET /health`
**API Endpoint**: `POST /api/voice-detection`

**Required Environment Variables**:
- `API_KEY` - Authentication key
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)

**System Requirements**:
- CPU: 2+ cores
- RAM: 2GB minimum, 4GB recommended
- Disk: 2GB for image
- Network: Internet access for language detection
