# Halopv Requests v2 Layer

Shared Lambda layer providing common HTTP request utilities for HaloPV services.

## Overview

- **Purpose**: Common HTTP request utilities
- **Version**: v2
- **Maintained by**: Development Team

## Contents

```
python/
├── requests_utils.py        # HTTP request utilities
├── retry_policies.py        # Retry and backoff strategies
└── monitoring.py            # Request monitoring and metrics
```

## Available Functions

### requests_utils.py

- `make_request()`: Make HTTP requests with built-in retry logic
- `RequestConfig`: Configuration class for HTTP clients
- `Session`: Wrapper around requests.Session with logging

### retry_policies.py

- `ExponentialBackoff`: Exponential backoff strategy
- `CircuitBreaker`: Circuit breaker pattern implementation

### monitoring.py

- `log_request()`: Log request details
- `log_response()`: Log response details
- `emit_metrics()`: Send CloudWatch metrics

## Usage in Lambda

```python
from requests_utils import make_request, RequestConfig

config = RequestConfig(
    timeout=30,
    max_retries=3,
    backoff_factor=2
)

response = make_request('GET', 'https://api.example.com/data', config)
```

## Dependencies

- requests>=2.28.0
- boto3>=1.26.0
