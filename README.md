# Booking App

## Overview
Booking App is a robust and scalable application designed for managing reservations. Built with FastAPI, it leverages modern tools like Docker, Redis, Celery, and PostgreSQ.

## Features
- **FastAPI** for high-performance backend
- **PostgreSQL** for database storage
- **Redis** for caching and task queue management
- **Celery** for background task execution
- **Flower** for monitoring Celery tasks
- **Prometheus & Grafana** for metrics and monitoring
- **Sentry** for error tracking
- **Versioning** to maintain API stability
- **Docker & Docker Compose** for containerized deployment

## Tech Stack
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **Cache & Queue:** Redis
- **Task Management:** Celery, Flower
- **Monitoring & Logging:** Prometheus, Grafana, Sentry
- **Containerization:** Docker, Docker Compose

## Installation
### Prerequisites
Ensure you have the following installed:
- Docker & Docker Compose

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/venia-min/booking-app.git
   cd booking-app
   ```
2. Create an `.env` file from the sample and configure the required environment variables:
   ```bash
   cp .env-sample .env
   ```
4. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Usage
- The API documentation is available at `http://localhost:8000/docs`.
- Monitor background tasks via Flower at `http://localhost:5555`.
- Check metrics on Prometheus at `http://localhost:9090`.
- View monitoring dashboards in Grafana at `http://localhost:3000`.
