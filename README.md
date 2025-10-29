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

- Docker installed on your system
- (Optional) Python 3.11+ for local development

## Quick Start with Docker

### Build the Docker image

```bash
docker build -t py-hello-app:latest .
```

### Run the container

```bash
docker run -d -p 5000:5000 --name py-hello-container py-hello-app:latest
```

### Access the application

Open your browser and navigate to:
```
http://localhost:5000
```

## Docker Commands

### View logs
```bash
docker logs py-hello-container
```

### Stop the container
```bash
docker stop py-hello-container
```

### Start the container
```bash
docker start py-hello-container
```

### Remove the container
```bash
docker rm -f py-hello-container
```

### View container stats
```bash
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

## Project Structure

```
.
├── app.py              # Flask application entry point
├── templates/
│   └── index.html      # Single-page application UI
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker build configuration
├── .dockerignore       # Files to exclude from Docker build
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
