# Use lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask requests python-dotenv

# Expose port for Flask app
EXPOSE 8080

# Set environment variable for Flask to production
ENV FLASK_ENV=production

# Command to run Flask app
CMD ["python", "app.py"]
