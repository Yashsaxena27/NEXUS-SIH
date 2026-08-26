import asyncio
import time
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from backend.app.normalization.cisco_adapter import CiscoAdapter
from backend.app.normalization.juniper_adapter import JuniperAdapter
from backend.app.compliance.engine import ComplianceEngine
from backend.app.compliance.loader import load_all_controls

def benchmark_parser(parser_class, config_path, iterations=100):
    with open(config_path, "r") as f:
        config_text = f.read()
    
    parser = parser_class()
    start_time = time.perf_counter()
    for _ in range(iterations):
        parser.normalize(config_text)
    end_time = time.perf_counter()
    
    avg_ms = ((end_time - start_time) / iterations) * 1000
    print(f"{parser_class.__name__} parsing avg time: {avg_ms:.2f} ms")

def benchmark_compliance(config_path, iterations=100):
    with open(config_path, "r") as f:
        config_text = f.read()
        
    parser = CiscoAdapter()
    result = parser.normalize(config_text)
    controls = load_all_controls()
    engine = ComplianceEngine(controls)
    
    start_time = time.perf_counter()
    for _ in range(iterations):
        engine.evaluate(result.config, result.evidence)
    end_time = time.perf_counter()
    
    avg_ms = ((end_time - start_time) / iterations) * 1000
    print(f"Compliance evaluation avg time ({len(controls)} controls): {avg_ms:.2f} ms")

if __name__ == "__main__":
    print("--- NEXUS SIH BENCHMARKS ---")
    cisco_demo = "demo/cisco_compliant.cfg"
    juniper_demo = "demo/juniper_malicious.conf"
    
    if Path(cisco_demo).exists():
        benchmark_parser(CiscoAdapter, cisco_demo)
        benchmark_compliance(cisco_demo)
    else:
        print("Cisco demo config not found.")
        
    if Path(juniper_demo).exists():
        benchmark_parser(JuniperAdapter, juniper_demo)
    else:
        print("Juniper demo config not found.")
