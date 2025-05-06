# Project Energy

## Description
This is a Python-based project that uses a PostgreSQL database called `project-energy`.

## Requirements
- Docker
- Python 3.9+

## Setup Instructions
1. Build the Docker image:
   ```sh
   docker build -t project-energy .
   docker run -p 8000:8000 project-energy
   ```

Ensure PostgreSQL is running and accessible.