"""Validation utilities for E2B and MHRA formats."""

import logging
from typing import Any, Dict, Optional
import jsonschema

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class Validator:
    """Base validator class."""
    
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
        self.validator = jsonschema.Draft7Validator(schema)
    
    def validate(self, data: Any) -> bool:
        """
        Validate data against schema.
        
        Args:
            data: Data to validate
        
        Returns:
            True if valid, raises ValidationError otherwise
        
        Raises:
            ValidationError: If validation fails
        """
        errors = list(self.validator.iter_errors(data))
        if errors:
            error_messages = [error.message for error in errors]
            raise ValidationError(f"Validation failed: {', '.join(error_messages)}")
        return True


def validate_e2b_schema(data: Dict[str, Any], schema_version: str = "2.0") -> bool:
    """
    Validate E2B submission format.
    
    Args:
        data: Submission data
        schema_version: E2B schema version
    
    Returns:
        True if valid
    
    Raises:
        ValidationError: If validation fails
    """
    from e2b_schema import get_e2b_schema
    
    schema = get_e2b_schema(schema_version)
    validator = Validator(schema)
    
    logger.info(f"Validating E2B submission against schema {schema_version}")
    return validator.validate(data)


def validate_mhra_format(data: Dict[str, Any]) -> bool:
    """
    Validate MHRA export format.
    
    Args:
        data: Export record
    
    Returns:
        True if valid
    
    Raises:
        ValidationError: If validation fails
    """
    from e2b_schema import get_mhra_schema
    
    schema = get_mhra_schema()
    validator = Validator(schema)
    
    logger.info("Validating MHRA export format")
    return validator.validate(data)


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_date_range(start_date: str, end_date: str) -> bool:
    """
    Validate date range is valid.
    
    Args:
        start_date: Start date (ISO format)
        end_date: End date (ISO format)
    
    Returns:
        True if valid
    """
    from datetime import datetime
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        if start > end:
            raise ValidationError("Start date must be before end date")
        return True
    except ValueError as e:
        raise ValidationError(f"Invalid date format: {str(e)}")
