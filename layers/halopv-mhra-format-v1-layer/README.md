# MHRA Format Conversion v1 Layer

Shared Lambda layer providing MHRA format conversion utilities.

## Overview

- **Purpose**: MHRA format conversion and validation
- **Version**: v1
- **Maintained by**: Development Team

## Contents

```
python/
├── mhra_format.py           # Format conversion functions
├── mhra_schema.py           # MHRA schema definitions
└── mhra_validators.py       # Format validation
```

## Functions

- `convert_to_mhra_csv()`: Convert submissions to CSV format
- `convert_to_mhra_json()`: Convert submissions to JSON format
- `convert_to_mhra_xml()`: Convert submissions to XML format
- `validate_mhra_record()`: Validate MHRA format compliance

## Dependencies

- pandas>=1.5.0
- lxml>=4.9.0
