from fastapi import FastAPI, Request, Form
from prometheus_client import Counter, Histogram, start_http_server
import threading

app = FastAPI()

# Metrics
REQUEST_COUNT = Counter("fastapi_requests_total", "HTTP requests", ["endpoint", "method"])
REQUEST_LATENCY = Histogram("fastapi_request_latency_seconds", "Request latency", ["endpoint"])

# Start metrics server
threading.Thread(target=lambda: start_http_server(8000), daemon=True).start()

@app.get("/")
def home():
    REQUEST_COUNT.labels(endpoint="/", method="GET").inc()
    return {"message": "Home"}

@app.post("/submit")
def submit(name: str = Form(...)):
    REQUEST_COUNT.labels(endpoint="/submit", method="POST").inc()
    with REQUEST_LATENCY.labels(endpoint="/submit").time():
        return {"message": f"Hello, {name}!"}
