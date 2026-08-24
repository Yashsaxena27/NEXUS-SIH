import yaml
from pathlib import Path
from backend.app.compliance.models import ComplianceControl, ControlRequirement, ControlSeverity, ControlOperator

def load_controls(yaml_path: str | Path) -> list[ComplianceControl]:
    '''Load compliance controls from a YAML file.'''
    path = Path(yaml_path)
    if not path.is_file():
        return []
    
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
        
    controls = []
    if not data or 'controls' not in data:
        return controls
        
    for ctrl_data in data['controls']:
        controls.append(ComplianceControl(**ctrl_data))
        
    return controls

def load_all_controls(controls_dir: str | Path = None) -> list[ComplianceControl]:
    '''Load all YAML control files from a directory.'''
    if controls_dir is None:
        controls_dir = Path(__file__).parent.parent.parent.parent / "compliance" / "controls"
    
    dir_path = Path(controls_dir)
    controls = []
    
    if not dir_path.is_dir():
        return controls
        
    for yaml_file in dir_path.rglob('*.yaml'):
        controls.extend(load_controls(yaml_file))
        
    return controls
