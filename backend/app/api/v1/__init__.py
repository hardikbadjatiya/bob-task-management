"""
API Version 1
Main API router for version 1 endpoints
"""

from fastapi import APIRouter
from app.api.v1 import auth, tasks, users, teams

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(teams.router, prefix="/teams", tags=["Teams"])

# Made with Bob
