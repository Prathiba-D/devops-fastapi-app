# Use official Python base image (slim version to keep image small)
FROM python:3.11-slim
# FROM python:3.11
# FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the entire application (including main.py and templates)
COPY . .

# Expose port that FastAPI runs on
EXPOSE 8000

# Command to run the app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
