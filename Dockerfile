FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "scripts/run.py"]

# Make the application accessible to other containers or the host
# CMD ["python", "-m", "http.server", "8000", "--bind", "0.0.0.0"]