# Use an official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application files
COPY . .

# Expose backend port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "-m", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

ENTRYPOINT python -m uvicorn app.main:app --host 0.0.0.0 --port 8000