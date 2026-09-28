"""Retry policies and circuit breaker pattern implementation."""

import logging
import time
from enum import Enum
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """States for circuit breaker."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery


class ExponentialBackoff:
    """Exponential backoff strategy."""
    
    def __init__(self, base: float = 1.0, max_wait: float = 300.0, jitter: bool = True):
        """
        Initialize exponential backoff.
        
        Args:
            base: Base wait time in seconds
            max_wait: Maximum wait time in seconds
            jitter: Add random jitter to wait time
        """
        self.base = base
        self.max_wait = max_wait
        self.jitter = jitter
    
    def wait(self, attempt: int):
        """Calculate and apply wait time for given attempt number."""
        wait_time = min(self.base * (2 ** attempt), self.max_wait)
        
        if self.jitter:
            import random
            wait_time *= random.uniform(0.5, 1.5)
        
        logger.info(f"Waiting {wait_time:.2f}s before retry attempt {attempt + 1}")
        time.sleep(wait_time)


class CircuitBreaker:
    """Circuit breaker pattern for preventing cascading failures."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout: int = 60
    ):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            success_threshold: Number of successes to close circuit
            timeout: Seconds before trying half-open
        """
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
    
    def call(self, func, *args, **kwargs):
        """Execute function through circuit breaker."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker entering HALF_OPEN state")
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
                logger.info("Circuit breaker CLOSED")
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        self.success_count = 0
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.error(f"Circuit breaker OPEN after {self.failure_count} failures")
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if not self.last_failure_time:
            return True
        return datetime.now() >= self.last_failure_time + timedelta(seconds=self.timeout)
