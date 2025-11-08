from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routes.auth import router as auth_router
from core.config import settings
from routes import ask, diagnose, prices, fertilizer, policy, dashboard

import logging
import time

# ===========================
# FastAPI App Initialization
# ===========================
app = FastAPI(
    title="AI Agri Assistant API",
    description="Backend API for AI-powered agriculture assistant using Gemini",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ✅ (REMOVED) SQLAlchemy DB Table Creation — Not needed for MongoDB

# ===========================
# Logging Configuration
# ===========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ===========================
# CORS Middleware
# ===========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# Request Logging Middleware
# ===========================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} ({process_time:.2f}ms)"
    )
    return response

# ===========================
# Global Exception Handler
# ===========================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

# ===========================
# Include Routers
# ===========================
app.include_router(auth_router)
app.include_router(ask.router)
app.include_router(diagnose.router)
app.include_router(prices.router)
app.include_router(fertilizer.router)
app.include_router(policy.router)
app.include_router(dashboard.router)

# ===========================
# Root and Health Endpoints
# ===========================
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the AI Agri Assistant API!"}

@app.get("/health", tags=["Root"])
async def health():
    return {"status": "ok"}
