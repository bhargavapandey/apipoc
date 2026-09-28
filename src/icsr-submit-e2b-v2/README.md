# ICSR Submit E2B v2 Lambda Function

This Lambda function handles ICSR (Individual Case Safety Report) submission with E2B format validation.

## Overview

- **Domain**: icsr
- **Function**: submit-e2b
- **Version**: v2
- **Maintained by**: Development Team

## Dependencies

- `halopv-requests-v2-layer`: Common HTTP request utilities
- `halopv-validation-v2-layer`: Data validation and E2B schema validation

## Environment Variables

The following environment variables should be set by the deployment configuration:

- `API_ENDPOINT`: Base API endpoint URL
- `VALIDATION_SCHEMA_VERSION`: E2B schema version to use
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run locally with SAM
sam local start-api
```

## Deployment

This function is deployed via CI/CD pipeline. The infrastructure definition is maintained in `infrastructure/services/icsr-submit-api-v2/`.
