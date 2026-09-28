"""Common HTTP request utilities for Lambda functions."""

import logging
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass
import requests
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


@dataclass
class RequestConfig:
    """Configuration for HTTP requests."""
    timeout: int = 30
    max_retries: int = 3
    backoff_factor: float = 2.0
    

class Session:
    """Wrapper around requests.Session with logging and monitoring."""
    
    def __init__(self, config: RequestConfig = None):
        """Initialize session with configuration."""
        self.config = config or RequestConfig()
        self.session = requests.Session()
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """Make GET request with retry logic."""
        return self.make_request('GET', url, **kwargs)
    
    def post(self, url: str, **kwargs) -> requests.Response:
        """Make POST request with retry logic."""
        return self.make_request('POST', url, **kwargs)
    
    def put(self, url: str, **kwargs) -> requests.Response:
        """Make PUT request with retry logic."""
        return self.make_request('PUT', url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> requests.Response:
        """Make DELETE request with retry logic."""
        return self.make_request('DELETE', url, **kwargs)
    
    def make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with automatic retry logic."""
        kwargs['timeout'] = kwargs.get('timeout', self.config.timeout)
        
        for attempt in range(self.config.max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{self.config.max_retries}: {method} {url}")
                response = self.session.request(method, url, **kwargs)
                
                # Log response
                logger.info(f"Response status: {response.status_code}")
                
                # Retry on 5xx errors
                if response.status_code >= 500 and attempt < self.config.max_retries - 1:
                    wait_time = self.config.backoff_factor ** attempt
                    logger.warning(f"Server error {response.status_code}, retrying in {wait_time}s")
                    time.sleep(wait_time)
                    continue
                
                return response
            
            except requests.exceptions.Timeout as e:
                logger.error(f"Request timeout on attempt {attempt + 1}")
                if attempt == self.config.max_retries - 1:
                    raise
                wait_time = self.config.backoff_factor ** attempt
                time.sleep(wait_time)
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Request exception: {str(e)}")
                if attempt == self.config.max_retries - 1:
                    raise
                wait_time = self.config.backoff_factor ** attempt
                time.sleep(wait_time)
        
        raise Exception(f"Failed to make request after {self.config.max_retries} attempts")


def make_request(
    method: str,
    url: str,
    config: Optional[RequestConfig] = None,
    **kwargs
) -> requests.Response:
    """Convenience function to make a single HTTP request."""
    session = Session(config)
    return session.make_request(method, url, **kwargs)
