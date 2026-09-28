# Validation Utilities Layer

Shared Lambda layer providing E2B and MHRA validation utilities.

## Overview

- **Purpose**: Data validation and schema compliance checking
- **Version**: v2
- **Maintained by**: Development Team

## Contents

```
python/
├── validation_utils.py       # Main validation functions
├── e2b_schema.py            # E2B schema definitions
└── validators.py            # Custom validators
```

## Functions

- `validate_e2b_schema()`: Validate E2B submission format
- `validate_mhra_format()`: Validate MHRA export format
- `ValidationError`: Exception class for validation errors

## Usage

```python
from validation_utils import validate_e2b_schema, ValidationError

try:
    validate_e2b_schema(submission_data, schema_version="2.0")
except ValidationError as e:
    print(f"Validation failed: {e}")
```
