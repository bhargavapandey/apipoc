import json
import pytest
from unittest.mock import patch, MagicMock
import sys

sys.modules['requests_utils'] = MagicMock()
sys.modules['mhra_format'] = MagicMock()

from lambda_function import lambda_handler, fetch_submissions, upload_to_s3


def test_lambda_handler_success():
    """Test successful MHRA export."""
    event = {
        "query_start_date": "2024-01-01",
        "query_end_date": "2024-01-31",
        "format": "csv"
    }
    
    context = MagicMock()
    
    with patch('lambda_function.fetch_submissions') as mock_fetch, \
         patch('lambda_function.upload_to_s3') as mock_upload:
        mock_fetch.return_value = [{"id": "1", "data": "test"}]
        mock_upload.return_value = "exports/mhra/2024-01-01/20240115_120000_mhra_export.csv"
        
        response = lambda_handler(event, context)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['format'] == 'csv'
    assert body['submission_count'] == 1


def test_lambda_handler_missing_dates():
    """Test export with missing dates."""
    event = {"format": "csv"}
    context = MagicMock()
    
    response = lambda_handler(event, context)
    
    assert response['statusCode'] == 400
    body = json.loads(response['body'])
    assert 'error' in body
