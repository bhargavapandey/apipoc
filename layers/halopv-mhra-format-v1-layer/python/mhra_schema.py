"""MHRA schema definitions."""

MHRA_SUBMISSION_SCHEMA = {
    "type": "object",
    "required": ["submission_id", "submission_date", "patient_initials", "adverse_event_description"],
    "properties": {
        "submission_id": {
            "type": "string",
            "description": "Unique submission identifier"
        },
        "submission_date": {
            "type": "string",
            "format": "date-time",
            "description": "Date and time of submission"
        },
        "patient_initials": {
            "type": "string",
            "pattern": "^[A-Z]{2}$",
            "description": "Patient initials (2 letters)"
        },
        "patient_dob": {
            "type": "string",
            "format": "date",
            "description": "Patient date of birth"
        },
        "adverse_event_description": {
            "type": "string",
            "minLength": 1,
            "description": "Description of adverse event"
        },
        "adverse_event_date": {
            "type": "string",
            "format": "date",
            "description": "Date of adverse event"
        },
        "serious": {
            "type": "boolean",
            "description": "Whether the event is serious"
        },
        "outcome": {
            "type": "string",
            "enum": ["recovered", "recovering", "not_recovered", "fatal", "unknown"],
            "description": "Outcome of the adverse event"
        }
    }
}

MHRA_EXPORT_FORMATS = {
    "csv": {
        "content_type": "text/csv",
        "extension": "csv"
    },
    "json": {
        "content_type": "application/json",
        "extension": "json"
    },
    "xml": {
        "content_type": "application/xml",
        "extension": "xml"
    }
}
