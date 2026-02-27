from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import projects, todos, status_reports, community, foundry_chat

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="FlowPilot Backend API for project management with Foundry integration"
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router)
app.include_router(todos.router)
app.include_router(status_reports.router)
app.include_router(community.router)
app.include_router(foundry_chat.router)


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/")
def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Welcome to FlowPilot Backend API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }
