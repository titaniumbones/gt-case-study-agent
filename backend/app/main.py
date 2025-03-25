from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import logging

from app.api.routes import api_router
from app.core.config import settings
from app.core.logging import setup_logging

app = FastAPI(title="GivingTuesday Campaign Advisor API")

# Configure CORS with more permissive settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# Include API routes
app.include_router(api_router, prefix="/api")

# Serve static files if in production mode
if settings.ENVIRONMENT == "production":
    # Mount the React build directory
    app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")
    
    # Serve React app for all other routes
    @app.get("/{full_path:path}")
    async def serve_react_app(request: Request, full_path: str):
        # Serve index.html for all routes (React will handle routing)
        if not (full_path.startswith("api/") or full_path.startswith("static/")):
            logger.info(f"Serving frontend for path: {full_path}")
            return FileResponse("../frontend/build/index.html")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting GivingTuesday Campaign Advisor API")
    
    # Ensure required directories exist
    os.makedirs("vectordb", exist_ok=True)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down GivingTuesday Campaign Advisor API")