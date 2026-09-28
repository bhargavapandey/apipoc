"""MHRA format conversion utilities."""

import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def convert_to_mhra_csv(submissions: List[Dict[str, Any]]) -> str:
    """
    Convert submissions to MHRA CSV format.
    
    Args:
        submissions: List of submission dictionaries
    
    Returns:
        CSV formatted string
    """
    try:
        import pandas as pd
        
        # Flatten submission data
        flattened = []
        for sub in submissions:
            flat_record = flatten_submission(sub)
            flattened.append(flat_record)
        
        # Convert to CSV
        df = pd.DataFrame(flattened)
        csv_data = df.to_csv(index=False)
        
        logger.info(f"Converted {len(submissions)} submissions to CSV")
        return csv_data
    
    except Exception as e:
        logger.error(f"CSV conversion failed: {str(e)}")
        raise


def convert_to_mhra_json(submissions: List[Dict[str, Any]]) -> str:
    """
    Convert submissions to MHRA JSON format.
    
    Args:
        submissions: List of submission dictionaries
    
    Returns:
        JSON formatted string
    """
    try:
        mhra_records = []
        for sub in submissions:
            mhra_record = map_to_mhra_schema(sub)
            mhra_records.append(mhra_record)
        
        json_data = json.dumps({
            "metadata": {
                "export_format": "MHRA-v1",
                "record_count": len(mhra_records)
            },
            "records": mhra_records
        }, indent=2)
        
        logger.info(f"Converted {len(submissions)} submissions to JSON")
        return json_data
    
    except Exception as e:
        logger.error(f"JSON conversion failed: {str(e)}")
        raise


def convert_to_mhra_xml(submissions: List[Dict[str, Any]]) -> str:
    """
    Convert submissions to MHRA XML format.
    
    Args:
        submissions: List of submission dictionaries
    
    Returns:
        XML formatted string
    """
    try:
        from lxml import etree
        
        root = etree.Element("mhra_export")
        root.set("version", "1.0")
        root.set("record_count", str(len(submissions)))
        
        for sub in submissions:
            record_elem = etree.SubElement(root, "record")
            mhra_record = map_to_mhra_schema(sub)
            dict_to_xml(mhra_record, record_elem)
        
        xml_data = etree.tostring(root, pretty_print=True, encoding='unicode')
        logger.info(f"Converted {len(submissions)} submissions to XML")
        return xml_data
    
    except Exception as e:
        logger.error(f"XML conversion failed: {str(e)}")
        raise


def flatten_submission(submission: Dict[str, Any]) -> Dict[str, Any]:
    """
    Flatten nested submission structure for CSV export.
    """
    flat = {}
    
    def flatten_dict(d, parent_key=''):
        for k, v in d.items():
            new_key = f"{parent_key}_{k}" if parent_key else k
            if isinstance(v, dict):
                flatten_dict(v, new_key)
            elif isinstance(v, list):
                flat[new_key] = json.dumps(v)
            else:
                flat[new_key] = v
    
    flatten_dict(submission)
    return flat


def map_to_mhra_schema(submission: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map submission data to MHRA schema.
    """
    return {
        "submission_id": submission.get("id"),
        "submission_date": submission.get("created_at"),
        "patient_initials": submission.get("patient", {}).get("initials"),
        "patient_dob": submission.get("patient", {}).get("date_of_birth"),
        "adverse_event_description": submission.get("adverse_event", {}).get("description"),
        "adverse_event_date": submission.get("adverse_event", {}).get("date_started"),
        "serious": submission.get("serious", False),
        "outcome": submission.get("outcome"),
    }


def dict_to_xml(data: Dict[str, Any], parent_elem):
    """
    Recursively convert dictionary to XML elements.
    """
    from lxml import etree
    
    for key, value in data.items():
        if isinstance(value, dict):
            child = etree.SubElement(parent_elem, key)
            dict_to_xml(value, child)
        elif isinstance(value, list):
            for item in value:
                child = etree.SubElement(parent_elem, key)
                if isinstance(item, dict):
                    dict_to_xml(item, child)
                else:
                    child.text = str(item)
        else:
            child = etree.SubElement(parent_elem, key)
            child.text = str(value) if value is not None else ""
