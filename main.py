from fastapi import FastAPI, Form
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from datetime import datetime
import time

app = FastAPI(title="FastAPI Monitoring App", version="1.0.0")

# Metrics
REQUEST_COUNT = Counter("fastapi_requests_total", "Total requests", ["endpoint"])
REQUEST_LATENCY = Histogram("fastapi_request_latency_seconds", "Request latency", ["endpoint"])

# Function to record metrics
def record_metrics(endpoint, latency):
    REQUEST_COUNT.labels(endpoint=endpoint).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)

# Root endpoint
@app.get("/")
def home():
    start = time.time()

    result = {
        "status": "success",
        "service": "fastapi-app",
        "message": "🚀 Welcome to FastAPI Monitoring App!",
        "timestamp": datetime.utcnow().isoformat()
    }

    record_metrics("/", time.time() - start)
    return result


# Submit endpoint
@app.post("/submit")
def submit(name: str = Form(...)):
    start = time.time()

    result = {
        "status": "success",
        "service": "fastapi-app",
        "message": f"👋 Hello, {name}!",
        "timestamp": datetime.utcnow().isoformat()
    }

    record_metrics("/submit", time.time() - start)
    return result


# Prometheus metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
