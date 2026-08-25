import yaml
from pathlib import Path
from pydantic import ValidationError
from typing import List, Union

from backend.app.compliance.models import ComplianceControl

def validate_policy(file_path: Union[str, Path]) -> List[ComplianceControl]:
    """Validates a YAML policy file against the ComplianceControl schema."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Policy file not found: {path}")
        
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    if not isinstance(data, dict) or "controls" not in data:
        raise ValueError("Invalid policy format. Expected top-level 'controls' list.")
        
    controls = []
    for raw_control in data["controls"]:
        try:
            control = ComplianceControl(**raw_control)
            controls.append(control)
        except ValidationError as e:
            # Re-raise with context
            raise ValueError(f"Validation failed for control '{raw_control.get('id', 'Unknown')}': {e}")
            
    return controls
