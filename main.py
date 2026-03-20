from fastapi import FastAPI, Form
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

app = FastAPI()

# Metrics
REQUEST_COUNT = Counter("fastapi_requests_total", "Total requests", ["endpoint"])
REQUEST_LATENCY = Histogram("fastapi_request_latency_seconds", "Request latency", ["endpoint"])

# Helper function to record metrics
def record_metrics(endpoint, latency):
    REQUEST_COUNT.labels(endpoint=endpoint).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)

# Application endpoints
@app.get("/")
def home():
    start = time.time()
    result = {"message": "Hello"}
    record_metrics("/", time.time() - start)
    return result

@app.post("/submit")
def submit(name: str = Form(...)):
    start = time.time()
    result = {"message": f"Hello, {name}!"}
    record_metrics("/submit", time.time() - start)
    return result

# Prometheus metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
