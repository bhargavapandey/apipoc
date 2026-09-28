import json
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Mock the layers for testing
sys.modules['requests_utils'] = MagicMock()
sys.modules['validation_utils'] = MagicMock()

from lambda_function import lambda_handler, process_icsr_submission, success_response, error_response


def test_lambda_handler_success():
    """Test successful ICSR submission."""
    event = {
        "body": json.dumps({
            "patient": {
                "initials": "JD",
                "date_of_birth": "1980-01-01"
            },
            "adverse_event": {
                "description": "Severe headache",
                "date_started": "2024-01-15"
            }
        }),
        "httpMethod": "POST",
        "headers": {"Content-Type": "application/json"}
    }
    
    context = MagicMock()
    
    with patch('lambda_function.validate_e2b_schema'):
        response = lambda_handler(event, context)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['status'] == 'accepted'
    assert 'submission_id' in body


def test_lambda_handler_validation_error():
    """Test ICSR submission with validation error."""
    from validation_utils import ValidationError
    
    event = {
        "body": json.dumps({"invalid": "data"}),
        "httpMethod": "POST",
        "headers": {"Content-Type": "application/json"}
    }
    
    context = MagicMock()
    
    with patch('lambda_function.validate_e2b_schema') as mock_validate:
        mock_validate.side_effect = ValidationError("Missing required fields")
        response = lambda_handler(event, context)
    
    assert response['statusCode'] == 400
    body = json.loads(response['body'])
    assert 'error' in body


def test_success_response():
    """Test success response formatting."""
    data = {"submission_id": "TEST-001", "status": "accepted"}
    response = success_response(data)
    
    assert response['statusCode'] == 200
    assert response['headers']['Content-Type'] == 'application/json'
    body = json.loads(response['body'])
    assert body['submission_id'] == 'TEST-001'


def test_error_response():
    """Test error response formatting."""
    response = error_response(400, "Bad request")
    
    assert response['statusCode'] == 400
    assert response['headers']['Content-Type'] == 'application/json'
    body = json.loads(response['body'])
    assert body['error'] == 'Bad request'
