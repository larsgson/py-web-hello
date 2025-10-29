# Python Hello World Web App

A minimal Python web application with a single "Update data" button, optimized for Docker deployment.

## Features

- Single-page web application built with Flask
- One interactive button that updates data via AJAX
- Modern, responsive UI with gradient design
- Production-ready Docker configuration
- Runs as non-root user for security
- Built-in health checks
- Minimal dependencies

## Prerequisites

- Docker and Docker Compose installed on your system
- (Optional) Python 3.11+ for local development

## Quick Start with Docker Compose (Recommended)

### Start the application

```bash
# First time: copy environment template (optional, defaults work fine)
cp .env.example .env

# Start the application
docker-compose up -d
```

### Access the application

Open your browser and navigate to:
```
http://localhost:5000
```

### Common Docker Compose Commands

```bash
# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Restart the application
docker-compose restart

# Rebuild and restart
docker-compose up -d --build

# View container stats
docker stats
```

## Alternative: Using Docker Directly

### Build the Docker image

```bash
docker build -t py-hello-app:latest .
```

### Run the container

```bash
docker run -d -p 5000:5000 --name py-hello-container py-hello-app:latest
```

### Docker Commands

```bash
# View logs
docker logs py-hello-container

# Stop the container
docker stop py-hello-container

# Start the container
docker start py-hello-container

# Remove the container
docker rm -f py-hello-container

# View container stats
docker stats py-hello-container
```

## Local Development (without Docker)

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Deployment to Digital Ocean

This application is optimized for deployment to Digital Ocean using Docker. The setup allows you to test everything locally before deploying to minimize cloud debugging.

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete Digital Ocean deployment instructions.

Quick summary:
1. Test locally with `docker-compose up`
2. Create Ubuntu droplet on Digital Ocean
3. Install Docker on droplet
4. Deploy using the same docker-compose.yml
5. Your local environment matches production exactly

## Project Structure

```
.
├── app.py              # Flask application entry point
├── templates/
│   └── index.html      # Single-page application UI
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker build configuration
├── docker-compose.yml  # Docker Compose configuration for local and production
├── .env.example        # Example environment configuration
├── .dockerignore       # Files to exclude from Docker build
├── DEPLOYMENT.md       # Digital Ocean deployment guide
├── LICENSE             # MIT License
└── README.md           # This file
```

## Docker Optimization Features

- **Slim base image**: Uses `python:3.11-slim` for smaller image size
- **Layer caching**: Requirements installed before copying application code
- **Non-root user**: Application runs as user `appuser` (UID 1000)
- **Health checks**: Automated container health monitoring
- **Environment variables**: Optimized Python runtime settings
- **.dockerignore**: Excludes unnecessary files from build context
- **Docker Compose**: Single configuration for local and production environments

## API Endpoints

### `GET /`
Returns the main HTML page with the interactive button.

### `POST /update`
Updates data and returns a JSON response with the current timestamp.

**Response example:**
```json
{
  "status": "success",
  "message": "Data updated at 2025-10-29 09:22:47"
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

larsgson
