from prometheus_client import Counter, Histogram, start_http_server
from fastapi import FastAPI, Request, Form

app = FastAPI()

# Start Prometheus metrics server (different port, e.g., 8001)
start_http_server(8001)

# Metrics
REQUEST_COUNT = Counter("fastapi_requests_total", "Total requests", ["endpoint"])
REQUEST_LATENCY = Histogram("fastapi_request_latency_seconds", "Request latency", ["endpoint"])

@app.get("/")
def home():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return {"message": "Hello"}

@app.post("/submit")
def submit(name: str = Form(...)):
    REQUEST_COUNT.labels(endpoint="/submit").inc()
    return {"message": f"Hello, {name}!"}
