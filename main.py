from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import logging

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    logger.info("Home page accessed")
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit")
def submit(name: str = Form(...)):
    logger.info(f"Form submitted with name: {name}")
    return {"message": f"Hello, {name}!"}

@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "healthy"})