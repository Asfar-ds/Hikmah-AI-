# =========================
# # 1️⃣ Frontend Build Stage
# # =========================
# FROM node:18 AS builder
# WORKDIR /app

# # Copy frontend dependencies and install
# COPY frontend/package*.json ./
# RUN npm install

# # Copy all source files and build
# COPY frontend/ ./
# RUN npm run build

# # =========================
# # 2️⃣ Backend + Nginx Stage
# # =========================
# FROM python:3.11-slim

# # Install Python + system dependencies
# RUN apt-get update && apt-get install -y nginx && apt-get clean

# WORKDIR /app

# # Copy backend
# COPY backend/ ./backend/
# COPY backend/requirements.txt .
# ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# # Install backend dependencies
# RUN pip install --no-cache-dir -r backend/requirements.txt

# # Copy built frontend from builder
# COPY --from=builder /app/dist /var/www/html

# # Copy Nginx configuration (you can customize this file)
# # If you don’t have a custom config, comment this out
# COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# # Expose both frontend (80) and backend (8000) ports
# EXPOSE 80
# EXPOSE 8000

# # Start both Nginx and Uvicorn in the same container
# CMD service nginx start && uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
