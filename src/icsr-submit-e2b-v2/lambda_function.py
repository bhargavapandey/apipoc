import json
import logging
import os
from datetime import datetime

# These utilities are provided by Lambda layers
try:
    from requests_utils import make_request, RequestConfig
    from validation_utils import validate_e2b_schema, ValidationError
except ImportError:
    # Fallback for local testing
    logging.warning("Layer dependencies not available - running in local mode")

logger = logging.getLogger()
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))

API_ENDPOINT = os.getenv('API_ENDPOINT', 'https://api.example.com')
VALIDATION_SCHEMA_VERSION = os.getenv('VALIDATION_SCHEMA_VERSION', '2.0')


def lambda_handler(event, context):
    """
    Main Lambda handler for ICSR E2B submission.
    
    Expected event structure:
    {
        "body": "<json-encoded ICSR submission>",
        "headers": {...},
        "httpMethod": "POST",
        "path": "/icsr/submit"
    }
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Parse request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        # Validate E2B schema
        logger.info(f"Validating against schema version {VALIDATION_SCHEMA_VERSION}")
        try:
            validate_e2b_schema(body, VALIDATION_SCHEMA_VERSION)
        except ValidationError as e:
            logger.error(f"Validation failed: {str(e)}")
            return error_response(400, f"Invalid E2B submission: {str(e)}")
        
        # Process submission
        submission_id = process_icsr_submission(body)
        
        logger.info(f"Successfully processed submission {submission_id}")
        return success_response({
            "submission_id": submission_id,
            "status": "accepted",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return error_response(500, "Internal server error")


def process_icsr_submission(submission_data):
    """
    Process the ICSR submission.
    This could involve:
    - Persisting to database
    - Sending to downstream systems
    - Triggering additional workflows
    """
    # Generate submission ID
    submission_id = f"ICSR-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{hash(json.dumps(submission_data, sort_keys=True)) % 10000:04d}"
    
    logger.info(f"Processing ICSR submission {submission_id}")
    # TODO: Implement actual processing logic
    
    return submission_id


def success_response(data, status_code=200):
    """Format successful response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "X-Submission-Time": datetime.utcnow().isoformat()
        },
        "body": json.dumps(data)
    }


def error_response(status_code, message):
    """Format error response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "error": message,
            "timestamp": datetime.utcnow().isoformat()
        })
    }
