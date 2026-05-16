"""
Health Check and Monitoring Endpoints
Provides detailed system health and metrics
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import psutil
import time
from typing import Dict, Any
from app.database import get_db
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger("health")


@router.get("/health")
async def health_check():
    """
    Basic health check endpoint
    Returns simple status for load balancers
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check with system metrics
    Includes database, memory, CPU, and disk status
    """
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    # Database health check
    try:
        start_time = time.time()
        db.execute(text("SELECT 1"))
        db_duration = (time.time() - start_time) * 1000
        
        health_data["checks"]["database"] = {
            "status": "healthy",
            "response_time_ms": round(db_duration, 2)
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        health_data["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_data["status"] = "unhealthy"
    
    # System metrics
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        
        # Disk usage
        disk = psutil.disk_usage('/')
        
        health_data["checks"]["system"] = {
            "status": "healthy",
            "cpu_percent": cpu_percent,
            "memory": {
                "total_mb": round(memory.total / (1024 * 1024), 2),
                "available_mb": round(memory.available / (1024 * 1024), 2),
                "percent_used": memory.percent
            },
            "disk": {
                "total_gb": round(disk.total / (1024 * 1024 * 1024), 2),
                "free_gb": round(disk.free / (1024 * 1024 * 1024), 2),
                "percent_used": disk.percent
            }
        }
        
        # Mark as unhealthy if resources are critically low
        if memory.percent > 90 or disk.percent > 90 or cpu_percent > 90:
            health_data["checks"]["system"]["status"] = "warning"
            health_data["status"] = "degraded"
            
    except Exception as e:
        logger.error(f"System metrics check failed: {str(e)}")
        health_data["checks"]["system"] = {
            "status": "unknown",
            "error": str(e)
        }
    
    return health_data


@router.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness probe for Kubernetes
    Checks if application is ready to serve traffic
    """
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Service not ready"
        )


@router.get("/health/live")
async def liveness_check():
    """
    Liveness probe for Kubernetes
    Checks if application is alive
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    """
    Prometheus-style metrics endpoint
    Returns application metrics in a structured format
    """
    metrics = {
        "timestamp": datetime.utcnow().isoformat(),
        "application": {
            "name": "task-management-system",
            "version": "1.0.0"
        },
        "metrics": {}
    }
    
    # Database metrics
    try:
        # Count total users
        result = db.execute(text("SELECT COUNT(*) FROM users"))
        total_users = result.scalar()
        
        # Count total tasks
        result = db.execute(text("SELECT COUNT(*) FROM tasks"))
        total_tasks = result.scalar()
        
        # Count total teams
        result = db.execute(text("SELECT COUNT(*) FROM teams"))
        total_teams = result.scalar()
        
        metrics["metrics"]["database"] = {
            "total_users": total_users,
            "total_tasks": total_tasks,
            "total_teams": total_teams
        }
    except Exception as e:
        logger.error(f"Failed to fetch database metrics: {str(e)}")
        metrics["metrics"]["database"] = {"error": str(e)}
    
    # System metrics
    try:
        metrics["metrics"]["system"] = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }
    except Exception as e:
        logger.error(f"Failed to fetch system metrics: {str(e)}")
        metrics["metrics"]["system"] = {"error": str(e)}
    
    return metrics

# Made with Bob
