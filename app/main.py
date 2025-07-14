import logging
from fastapi import FastAPI
from pydantic import BaseModel
from app.core.config import get_settings
from app.api.v1.routers import chat_router

# Set up root logger
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for local development if needed
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# Create specific logger
logger = logging.getLogger("chat_app")
logger.info("Logger initialized.")


# Create FastAPI app
app = FastAPI()

# Load settings
settings = get_settings()

# Add routing
app.include_router(chat_router.router)


@app.on_event("startup")
def startup_event():
    print(f"Starting up in {settings.environment} environment")

@app.get("/")
def read_root():
    return {
        "environment": settings.environment,
        "debug": settings.debug,
    }