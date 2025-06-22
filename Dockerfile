FROM python:3.10-slim-bookworm

# Security updates
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies without caching
RUN pip install --no-cache-dir -r requirements.txt

# Set default port (can be overridden at runtime)
ENV PORT=8000
EXPOSE $PORT

# (Optional) Create and switch to a non-root user
RUN useradd -m appuser
USER appuser

# Start the application
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:$PORT", "app:app"]
