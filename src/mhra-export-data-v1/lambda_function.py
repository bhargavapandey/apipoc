import json
import logging
import os
from datetime import datetime

# Layer dependencies
try:
    from requests_utils import Session, RequestConfig
    from mhra_format import convert_to_mhra_csv, convert_to_mhra_json
except ImportError:
    logging.warning("Layer dependencies not available - running in local mode")

logger = logging.getLogger()
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))

EXPORT_BUCKET = os.getenv('EXPORT_BUCKET', 'halopv-exports-dev')
EXPORT_FORMAT = os.getenv('EXPORT_FORMAT', 'csv')


def lambda_handler(event, context):
    """
    Lambda handler for MHRA data export.
    
    Expected event structure:
    {
        "query_start_date": "2024-01-01",
        "query_end_date": "2024-01-31",
        "format": "csv"  # optional: csv, json, xml
    }
    """
    logger.info(f"Received export request: {json.dumps(event)}")
    
    try:
        query_start = event.get('query_start_date')
        query_end = event.get('query_end_date')
        export_format = event.get('format', EXPORT_FORMAT)
        
        # Validate dates
        if not query_start or not query_end:
            return error_response(400, "Missing query_start_date or query_end_date")
        
        # Fetch submissions
        logger.info(f"Fetching submissions from {query_start} to {query_end}")
        submissions = fetch_submissions(query_start, query_end)
        
        # Convert to MHRA format
        if export_format == 'json':
            export_data = convert_to_mhra_json(submissions)
            file_extension = 'json'
        else:  # default to CSV
            export_data = convert_to_mhra_csv(submissions)
            file_extension = 'csv'
        
        # Upload to S3
        s3_key = upload_to_s3(export_data, export_format, query_start, query_end)
        
        logger.info(f"Successfully created export: {s3_key}")
        return success_response({
            "export_id": s3_key,
            "format": export_format,
            "submission_count": len(submissions),
            "location": f"s3://{EXPORT_BUCKET}/{s3_key}",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Export failed: {str(e)}", exc_info=True)
        return error_response(500, "Export process failed")


def fetch_submissions(start_date, end_date):
    """
    Fetch ICSR submissions for the date range.
    This would typically query a database or API.
    """
    logger.info(f"Fetching submissions for period {start_date} to {end_date}")
    # TODO: Implement actual data retrieval
    return []


def upload_to_s3(data, format_type, start_date, end_date):
    """
    Upload export file to S3.
    """
    import boto3
    s3_client = boto3.client('s3')
    
    # Generate S3 key
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    s3_key = f"exports/mhra/{start_date}/{timestamp}_mhra_export.{format_type}"
    
    try:
        s3_client.put_object(
            Bucket=EXPORT_BUCKET,
            Key=s3_key,
            Body=data,
            ContentType='application/octet-stream',
            ServerSideEncryption='AES256'
        )
        logger.info(f"Uploaded export to S3: {s3_key}")
        return s3_key
    except Exception as e:
        logger.error(f"S3 upload failed: {str(e)}")
        raise


def success_response(data, status_code=200):
    """Format successful response."""
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(data)
    }


def error_response(status_code, message):
    """Format error response."""
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "error": message,
            "timestamp": datetime.utcnow().isoformat()
        })
    }
