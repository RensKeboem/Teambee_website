# Build stage for CSS
FROM node:18-slim as css-builder
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
RUN npm run build:css

# Build stage for Python
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

    # Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the built CSS and other files
COPY --from=css-builder /app/public/app.css public/app.css
COPY . .

# Set environment variables
ENV PORT=8000
ENV HOST=0.0.0.0

# Expose the port
EXPOSE 8000

# Run the app
CMD uvicorn main:app --host 0.0.0.0 --port $PORT