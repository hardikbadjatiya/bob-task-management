"""
Custom Middleware for Request Tracking and Security
"""

import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from typing import Callable
from app.core.logging import (
    get_request_logger,
    get_security_logger,
    generate_request_id,
    set_request_id
)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging all HTTP requests and responses"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.request_logger = get_request_logger()
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate and set request ID
        request_id = generate_request_id()
        set_request_id(request_id)
        
        # Add request ID to request state
        request.state.request_id = request_id
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Log incoming request
        self.request_logger.log_request(
            method=request.method,
            path=request.url.path,
            client_ip=client_ip,
            user_id=getattr(request.state, 'user_id', None)
        )
        
        # Track request duration
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            # Log response
            self.request_logger.log_response(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms
            )
            
            return response
            
        except Exception as e:
            # Log error
            duration_ms = (time.time() - start_time) * 1000
            self.request_logger.log_error(
                error=e,
                context={
                    'method': request.method,
                    'path': request.url.path,
                    'duration_ms': duration_ms
                }
            )
            raise


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware for adding security headers to responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting middleware"""
    
    def __init__(self, app: ASGIApp, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_counts = {}
        self.security_logger = get_security_logger()
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client identifier
        client_ip = request.client.host if request.client else "unknown"
        current_time = int(time.time() / 60)  # Current minute
        
        # Create key for this client and minute
        key = f"{client_ip}:{current_time}"
        
        # Clean old entries
        self._cleanup_old_entries(current_time)
        
        # Check rate limit
        if key in self.request_counts:
            self.request_counts[key] += 1
            if self.request_counts[key] > self.requests_per_minute:
                # Log suspicious activity
                self.security_logger.log_suspicious_activity(
                    activity_type="rate_limit_exceeded",
                    details={
                        'requests': self.request_counts[key],
                        'limit': self.requests_per_minute,
                        'path': request.url.path
                    },
                    client_ip=client_ip
                )
                
                return Response(
                    content="Rate limit exceeded",
                    status_code=429,
                    headers={"Retry-After": "60"}
                )
        else:
            self.request_counts[key] = 1
        
        return await call_next(request)
    
    def _cleanup_old_entries(self, current_minute: int):
        """Remove entries older than 2 minutes"""
        keys_to_delete = [
            key for key in self.request_counts.keys()
            if int(key.split(':')[1]) < current_minute - 2
        ]
        for key in keys_to_delete:
            del self.request_counts[key]


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware for monitoring application performance"""
    
    def __init__(self, app: ASGIApp, slow_request_threshold_ms: float = 1000):
        super().__init__(app)
        self.slow_request_threshold_ms = slow_request_threshold_ms
        self.request_logger = get_request_logger()
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        response = await call_next(request)
        
        duration_ms = (time.time() - start_time) * 1000
        
        # Log slow requests
        if duration_ms > self.slow_request_threshold_ms:
            self.request_logger.logger.warning(
                f"Slow request detected: {request.method} {request.url.path} ({duration_ms:.2f}ms)",
                extra={
                    'extra_data': {
                        'method': request.method,
                        'path': request.url.path,
                        'duration_ms': round(duration_ms, 2),
                        'threshold_ms': self.slow_request_threshold_ms,
                        'type': 'slow_request'
                    }
                }
            )
        
        # Add performance header
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
        
        return response

# Made with Bob
