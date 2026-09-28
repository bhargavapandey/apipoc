# MHRA Export API Service Definition

Service definition for the MHRA data export functionality.

## Overview

- **Application**: halopv
- **Domain**: mhra
- **Service**: export-api
- **Version**: v1
- **Maintained by**: Development + DevOps

## Components

1. **Lambda Function**: `halopv-mhra-export-data-v1-lambda`
2. **API Gateway**: `halopv-mhra-api-v1`
3. **S3 Bucket**: Export storage
4. **IAM Role**: Export permissions

## Integration Points

- Reads from submission database
- Writes to S3 export bucket
- Uses MHRA format layer

## Deployment

Follows same pattern as ICSR Submit API service.
