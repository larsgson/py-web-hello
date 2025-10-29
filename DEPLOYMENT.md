# Digital Ocean Deployment Guide

This guide explains how to deploy the Python Hello World app to Digital Ocean using Docker, with maximum local testing capability.

## Strategy: Identical Local and Production Environments

The deployment uses Docker Compose to ensure your local environment matches production exactly, minimizing cloud debugging needs.

## Prerequisites

- Digital Ocean account
- A Digital Ocean Droplet (Ubuntu 22.04 or later recommended)
- SSH access to your droplet
- Domain name (optional, but recommended)

## Local Testing (Before Deployment)

### 1. Test with Docker Compose locally

```bash
# Build and run
docker-compose up --build

# Access at http://localhost:5000
```

### 2. Test production port configuration

```bash
# Create .env file for port 80 (production-like)
echo "PORT=80" > .env

# Run with elevated privileges (port 80)
sudo docker-compose up --build

# Access at http://localhost
```

If everything works locally on port 80, it will work on Digital Ocean.

## Digital Ocean Deployment

### Step 1: Create a Droplet

1. Log into Digital Ocean
2. Create a new Droplet:
   - **OS**: Ubuntu 22.04 LTS
   - **Plan**: Basic ($6/month is sufficient for this app)
   - **Region**: Choose closest to your users
   - **Authentication**: SSH key (recommended)

### Step 2: Install Docker on Droplet

SSH into your droplet:

```bash
ssh root@your_droplet_ip
```

Install Docker and Docker Compose:

```bash
# Update package index
apt update

# Install prerequisites
apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

### Step 3: Deploy Application

```bash
# Create application directory
mkdir -p /opt/py-web-hello
cd /opt/py-web-hello

# Clone your repository (or use scp/rsync to copy files)
# Option A: Using git
git clone https://github.com/yourusername/py-web-hello.git .

# Option B: Using rsync from local machine (run from your local machine)
# rsync -avz --exclude '.git' --exclude '__pycache__' /home/lgunnars/dev/bw/py-web-hello/ root@your_droplet_ip:/opt/py-web-hello/
```

### Step 4: Configure for Production

```bash
# Create .env file for production
echo "PORT=80" > .env

# Build and start the application
docker compose up -d --build

# Verify it's running
docker compose ps
docker compose logs
```

### Step 5: Verify Deployment

```bash
# Check if container is running
docker compose ps

# View logs
docker compose logs -f

# Test locally on droplet
curl http://localhost

# Test from your machine
curl http://your_droplet_ip
```

## Updates and Redeployment

When you make changes locally and test them:

```bash
# On your local machine: Test thoroughly
docker-compose up --build

# Once verified, push to git or sync files
git push origin main

# On Digital Ocean droplet
cd /opt/py-web-hello
git pull origin main  # or rsync from local

# Rebuild and restart (zero-downtime with proper setup)
docker compose up -d --build

# Verify
docker compose logs -f
```

## Useful Commands on Digital Ocean

### View logs
```bash
docker compose logs -f web
```

### Restart application
```bash
docker compose restart
```

### Stop application
```bash
docker compose down
```

### Rebuild and restart
```bash
docker compose up -d --build
```

### View resource usage
```bash
docker stats
```

### Clean up old images
```bash
docker system prune -a
```

## Firewall Configuration

Configure UFW firewall on Digital Ocean:

```bash
# Allow SSH (important!)
ufw allow 22/tcp

# Allow HTTP
ufw allow 80/tcp

# Allow HTTPS (for future SSL setup)
ufw allow 443/tcp

# Enable firewall
ufw enable

# Check status
ufw status
```

## Optional: Set Up Domain Name

### Configure DNS
1. Add an A record pointing to your droplet IP
   - Host: `@` (or subdomain like `www`)
   - Value: `your_droplet_ip`

### Set Up Reverse Proxy with Nginx (Recommended)

For production with SSL/HTTPS, add Nginx reverse proxy:

```bash
# Install nginx
apt install -y nginx

# Create nginx config
cat > /etc/nginx/sites-available/py-hello <<'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/py-hello /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

# Test and reload
nginx -t
systemctl reload nginx

# Update .env to use port 5000 (behind nginx)
echo "PORT=5000" > /opt/py-web-hello/.env
cd /opt/py-web-hello
docker compose up -d
```

### Add SSL with Let's Encrypt

```bash
# Install certbot
apt install -y certbot python3-certbot-nginx

# Get certificate
certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal is configured automatically
```

## Monitoring and Maintenance

### Set up automatic restarts
The `restart: unless-stopped` policy in docker-compose.yml ensures the container restarts automatically after:
- Container crashes
- Droplet reboots
- Docker daemon restarts

### Monitor logs
```bash
# Follow logs
docker compose logs -f

# Last 100 lines
docker compose logs --tail=100
```

### Health checks
The application includes built-in health checks. Monitor with:
```bash
docker inspect py-hello-app | grep -A 10 Health
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker compose logs

# Rebuild from scratch
docker compose down
docker compose up --build
```

### Port already in use
```bash
# Find what's using the port
lsof -i :80

# Kill the process or change PORT in .env
```

### Can't connect from browser
```bash
# Check firewall
ufw status

# Check container is running
docker compose ps

# Check nginx (if using)
systemctl status nginx
nginx -t
```

## Best Practices

1. **Always test locally first** with the same Docker Compose setup
2. **Use version control** (git) to track all changes
3. **Test with production port** (80) locally before deploying
4. **Keep backups** of your .env and any data
5. **Monitor logs** regularly after deployment
6. **Update dependencies** periodically for security

## Cost Optimization

- **Basic Droplet ($6/month)** is sufficient for this application
- **Enable monitoring** in Digital Ocean dashboard (free)
- **Set up billing alerts** to avoid surprises
- **Use floating IPs** if you need to migrate droplets without DNS changes

## Next Steps

1. Test thoroughly locally with `docker-compose up`
2. Create Digital Ocean droplet
3. Deploy using the steps above
4. Set up domain and SSL (optional but recommended)
5. Configure monitoring and backups
6. Document any custom configurations in this file
