"""Request monitoring and metrics utilities."""

import json
import logging
import time
from datetime import datetime
from typing import Optional
import boto3

logger = logging.getLogger(__name__)
cloudwatch = boto3.client('cloudwatch')


def log_request(method: str, url: str, headers: dict = None, body: str = None):
    """Log HTTP request details."""
    log_data = {
        "type": "http_request",
        "timestamp": datetime.utcnow().isoformat(),
        "method": method,
        "url": url,
        "headers": headers or {}
    }
    if body:
        try:
            log_data["body"] = json.loads(body)
        except:
            log_data["body"] = body
    
    logger.info(json.dumps(log_data))


def log_response(status_code: int, headers: dict = None, body: str = None, elapsed: float = 0):
    """Log HTTP response details."""
    log_data = {
        "type": "http_response",
        "timestamp": datetime.utcnow().isoformat(),
        "status_code": status_code,
        "elapsed_ms": int(elapsed * 1000),
        "headers": headers or {}
    }
    if body:
        try:
            log_data["body"] = json.loads(body)
        except:
            log_data["body"] = body[:200]  # Truncate large responses
    
    logger.info(json.dumps(log_data))


def emit_metrics(namespace: str, metric_name: str, value: float, unit: str = 'Count'):
    """Emit CloudWatch metric."""
    try:
        cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Value': value,
                    'Unit': unit,
                    'Timestamp': datetime.utcnow()
                }
            ]
        )
        logger.debug(f"Emitted metric {namespace}/{metric_name}")
    except Exception as e:
        logger.error(f"Failed to emit metric: {str(e)}")
