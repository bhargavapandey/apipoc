"""E2B and MHRA schema definitions."""

E2B_SCHEMA_V2 = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "E2B Submission Schema v2.0",
    "type": "object",
    "required": ["patient", "adverse_event"],
    "properties": {
        "patient": {
            "type": "object",
            "required": ["initials", "date_of_birth"],
            "properties": {
                "initials": {
                    "type": "string",
                    "pattern": "^[A-Z]{2}$"
                },
                "date_of_birth": {
                    "type": "string",
                    "format": "date"
                },
                "age": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 150
                },
                "weight_kg": {
                    "type": "number",
                    "minimum": 0.5,
                    "maximum": 300
                }
            }
        },
        "adverse_event": {
            "type": "object",
            "required": ["description", "date_started"],
            "properties": {
                "description": {
                    "type": "string",
                    "minLength": 1
                },
                "date_started": {
                    "type": "string",
                    "format": "date"
                },
                "date_ended": {
                    "type": "string",
                    "format": "date"
                },
                "serious": {
                    "type": "boolean"
                },
                "outcome": {
                    "type": "string",
                    "enum": ["recovered", "recovering", "not_recovered", "fatal", "unknown"]
                }
            }
        },
        "medication": {
            "type": "object",
            "required": ["name", "route"],
            "properties": {
                "name": {"type": "string"},
                "route": {"type": "string"},
                "dose": {"type": "string"},
                "frequency": {"type": "string"}
            }
        }
    }
}

MHRA_EXPORT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "MHRA Export Schema v1.0",
    "type": "object",
    "required": ["submission_id", "submission_date", "patient_initials"],
    "properties": {
        "submission_id": {"type": "string"},
        "submission_date": {"type": "string", "format": "date-time"},
        "patient_initials": {"type": "string", "pattern": "^[A-Z]{2}$"},
        "patient_dob": {"type": "string", "format": "date"},
        "adverse_event_description": {"type": "string"},
        "serious": {"type": "boolean"},
        "outcome": {
            "type": "string",
            "enum": ["recovered", "recovering", "not_recovered", "fatal", "unknown"]
        }
    }
}


def get_e2b_schema(version: str = "2.0"):
    """
    Get E2B schema by version.
    
    Args:
        version: Schema version
    
    Returns:
        Schema dictionary
    """
    if version == "2.0":
        return E2B_SCHEMA_V2
    else:
        raise ValueError(f"Unknown E2B schema version: {version}")


def get_mhra_schema():
    """
    Get MHRA export schema.
    
    Returns:
        Schema dictionary
    """
    return MHRA_EXPORT_SCHEMA
