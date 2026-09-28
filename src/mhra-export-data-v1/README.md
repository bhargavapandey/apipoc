# MHRA Data Export Lambda Function

Lambda function for exporting ICSR submission data in MHRA format.

## Overview

- **Domain**: mhra
- **Function**: export-data
- **Version**: v1
- **Maintained by**: Development Team

## Dependencies

- `halopv-requests-v2-layer`: HTTP request utilities
- `halopv-mhra-format-v1-layer`: MHRA format conversion utilities

## Environment Variables

- `EXPORT_BUCKET`: S3 bucket for export files
- `MHRA_API_KEY`: API key for MHRA submission
- `EXPORT_FORMAT`: Export format (CSV, JSON, XML)

## Functionality

- Retrieves submission data from database
- Converts to MHRA format
- Generates export files
- Uploads to S3
- Sends notifications

## Local Development

```bash
pip install -r requirements.txt
python -m pytest tests/
```
