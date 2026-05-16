"""
Enhanced Logging System
Provides structured logging with request tracking and performance monitoring
"""

import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict
from contextvars import ContextVar
import uuid

# Context variable for request ID tracking
request_id_var: ContextVar[str] = ContextVar('request_id', default='')


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add request ID if available
        request_id = request_id_var.get()
        if request_id:
            log_data['request_id'] = request_id
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data
        
        return json.dumps(log_data)


class RequestLogger:
    """Logger for HTTP request/response tracking"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_request(
        self,
        method: str,
        path: str,
        client_ip: str,
        user_id: str = None
    ):
        """Log incoming HTTP request"""
        extra_data = {
            'method': method,
            'path': path,
            'client_ip': client_ip,
            'user_id': user_id,
            'type': 'request'
        }
        self.logger.info(
            f"Request: {method} {path}",
            extra={'extra_data': extra_data}
        )
    
    def log_response(
        self,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float
    ):
        """Log HTTP response with performance metrics"""
        extra_data = {
            'method': method,
            'path': path,
            'status_code': status_code,
            'duration_ms': round(duration_ms, 2),
            'type': 'response'
        }
        
        level = logging.INFO
        if status_code >= 500:
            level = logging.ERROR
        elif status_code >= 400:
            level = logging.WARNING
        
        self.logger.log(
            level,
            f"Response: {method} {path} - {status_code} ({duration_ms:.2f}ms)",
            extra={'extra_data': extra_data}
        )
    
    def log_error(
        self,
        error: Exception,
        context: Dict[str, Any] = None
    ):
        """Log application error with context"""
        extra_data = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'type': 'error'
        }
        if context:
            extra_data['context'] = context
        
        self.logger.error(
            f"Error: {type(error).__name__} - {str(error)}",
            exc_info=True,
            extra={'extra_data': extra_data}
        )


class SecurityLogger:
    """Logger for security-related events"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_auth_attempt(
        self,
        email: str,
        success: bool,
        client_ip: str,
        reason: str = None
    ):
        """Log authentication attempt"""
        extra_data = {
            'email': email,
            'success': success,
            'client_ip': client_ip,
            'type': 'auth_attempt'
        }
        if reason:
            extra_data['reason'] = reason
        
        level = logging.INFO if success else logging.WARNING
        message = f"Auth {'success' if success else 'failed'}: {email}"
        
        self.logger.log(
            level,
            message,
            extra={'extra_data': extra_data}
        )
    
    def log_permission_denied(
        self,
        user_id: str,
        resource: str,
        action: str
    ):
        """Log permission denied event"""
        extra_data = {
            'user_id': user_id,
            'resource': resource,
            'action': action,
            'type': 'permission_denied'
        }
        self.logger.warning(
            f"Permission denied: User {user_id} - {action} on {resource}",
            extra={'extra_data': extra_data}
        )
    
    def log_suspicious_activity(
        self,
        activity_type: str,
        details: Dict[str, Any],
        client_ip: str
    ):
        """Log suspicious activity"""
        extra_data = {
            'activity_type': activity_type,
            'details': details,
            'client_ip': client_ip,
            'type': 'suspicious_activity'
        }
        self.logger.warning(
            f"Suspicious activity: {activity_type}",
            extra={'extra_data': extra_data}
        )


class PerformanceLogger:
    """Logger for performance metrics"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_query_performance(
        self,
        query_type: str,
        duration_ms: float,
        rows_affected: int = None
    ):
        """Log database query performance"""
        extra_data = {
            'query_type': query_type,
            'duration_ms': round(duration_ms, 2),
            'type': 'db_query'
        }
        if rows_affected is not None:
            extra_data['rows_affected'] = rows_affected
        
        level = logging.WARNING if duration_ms > 1000 else logging.DEBUG
        
        self.logger.log(
            level,
            f"Query: {query_type} ({duration_ms:.2f}ms)",
            extra={'extra_data': extra_data}
        )
    
    def log_cache_operation(
        self,
        operation: str,
        key: str,
        hit: bool = None
    ):
        """Log cache operation"""
        extra_data = {
            'operation': operation,
            'key': key,
            'type': 'cache'
        }
        if hit is not None:
            extra_data['hit'] = hit
        
        self.logger.debug(
            f"Cache {operation}: {key}",
            extra={'extra_data': extra_data}
        )


def setup_logging(log_level: str = "INFO", json_logs: bool = True) -> logging.Logger:
    """
    Setup application logging with structured format
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_logs: Whether to use JSON formatting
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("task_management")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, log_level.upper()))
    
    # Set formatter
    if json_logs:
        formatter = StructuredFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """Get logger instance"""
    if name:
        return logging.getLogger(f"task_management.{name}")
    return logging.getLogger("task_management")


def generate_request_id() -> str:
    """Generate unique request ID"""
    return str(uuid.uuid4())


def set_request_id(request_id: str):
    """Set request ID in context"""
    request_id_var.set(request_id)


def get_request_id() -> str:
    """Get current request ID"""
    return request_id_var.get()


# Create specialized loggers
def get_request_logger() -> RequestLogger:
    """Get request logger instance"""
    return RequestLogger(get_logger("request"))


def get_security_logger() -> SecurityLogger:
    """Get security logger instance"""
    return SecurityLogger(get_logger("security"))


def get_performance_logger() -> PerformanceLogger:
    """Get performance logger instance"""
    return PerformanceLogger(get_logger("performance"))