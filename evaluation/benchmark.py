"""
NEXUS Evaluation Benchmark

Evaluates the full pipeline:
    vendor detection → normalization → compliance → evidence

Against ground truth data in dataset/ground_truth/

Usage:
    cd <project_root>
    python -m evaluation.benchmark

Output:
    - Console summary
    - evaluation/results.json (machine-readable)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# Ensure project root is on path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.schemas.security_ir import NormalizationResult
from backend.app.compliance.models import ComplianceStatus


def load_ground_truth(gt_dir: Path) -> list[dict]:
    """Load all ground truth JSON files."""
    samples = []
    for gt_file in sorted(gt_dir.glob("*_ground_truth.json")):
        with open(gt_file) as f:
            data = json.load(f)
        for sample in data.get("samples", []):
            sample["_vendor"] = data["vendor"]
            sample["_gt_file"] = gt_file.name
            samples.append(sample)
    return samples


def evaluate_vendor_detection(samples: list[dict], results: dict[str, dict]) -> dict:
    """Evaluate vendor detection accuracy."""
    correct = 0
    total = 0
    errors = []

    for sample in samples:
        filename = sample["filename"]
        expected_vendor = sample.get("expected_vendor_detection", sample["_vendor"])
        if filename in results:
            actual_vendor = results[filename].get("detected_vendor", "")
            total += 1
            if actual_vendor.lower() == expected_vendor.lower():
                correct += 1
            else:
                errors.append({
                    "file": filename,
                    "expected": expected_vendor,
                    "actual": actual_vendor,
                })

    accuracy = correct / total if total > 0 else 0.0
    return {
        "accuracy": round(accuracy, 4),
        "correct": correct,
        "total": total,
        "errors": errors,
    }


def evaluate_normalization(samples: list[dict], results: dict[str, dict]) -> dict:
    """Evaluate normalization accuracy against expected values."""
    correct = 0
    total = 0
    errors = []

    for sample in samples:
        filename = sample["filename"]
        expected = sample.get("expected_normalized", {})
        if filename not in results or not expected:
            continue

        actual_config = results[filename].get("normalized_config", {})

        for field_path, expected_value in expected.items():
            total += 1
            actual_value = _resolve_dotpath(actual_config, field_path)

            if actual_value == expected_value:
                correct += 1
            else:
                errors.append({
                    "file": filename,
                    "field": field_path,
                    "expected": expected_value,
                    "actual": actual_value,
                })

    accuracy = correct / total if total > 0 else 0.0
    return {
        "accuracy": round(accuracy, 4),
        "correct": correct,
        "total": total,
        "errors": errors[:20],  # Limit error output
    }


def evaluate_compliance(samples: list[dict], results: dict[str, dict]) -> dict:
    """Evaluate compliance detection accuracy (PASS/FAIL/UNKNOWN)."""
    tp = 0  # True positive: correctly detected FAIL
    tn = 0  # True negative: correctly detected PASS
    fp = 0  # False positive: said FAIL when should be PASS
    fn = 0  # False negative: said PASS when should be FAIL
    unknowns = 0
    total = 0
    errors = []

    for sample in samples:
        filename = sample["filename"]
        expected_compliance = sample.get("expected_compliance", {})
        if filename not in results or not expected_compliance:
            continue

        actual_findings = results[filename].get("findings", {})

        for control_id, expected_status in expected_compliance.items():
            total += 1
            actual_status = actual_findings.get(control_id, "UNKNOWN")

            if actual_status in ["UNKNOWN", "UNKNOWN_ABSENT", "UNKNOWN_PARSE_ERROR"]:
                unknowns += 1
                continue

            if expected_status == "FAIL" and actual_status == "FAIL":
                tp += 1
            elif expected_status == "PASS" and actual_status == "PASS":
                tn += 1
            elif expected_status == "PASS" and actual_status == "FAIL":
                fp += 1
                errors.append({
                    "file": filename,
                    "control": control_id,
                    "expected": expected_status,
                    "actual": actual_status,
                    "type": "false_positive",
                })
            elif expected_status == "FAIL" and actual_status == "PASS":
                fn += 1
                errors.append({
                    "file": filename,
                    "control": control_id,
                    "expected": expected_status,
                    "actual": actual_status,
                    "type": "false_negative",
                })

    evaluated = tp + tn + fp + fn
    accuracy = (tp + tn) / evaluated if evaluated > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "false_positive_rate": round(fpr, 4),
        "false_negative_rate": round(fnr, 4),
        "unknown_rate": round(unknowns / total, 4) if total > 0 else 0.0,
        "true_positives": tp,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "unknowns": unknowns,
        "total_checks": total,
        "errors": errors[:20],
    }


def _resolve_dotpath(obj: dict, path: str) -> Any:
    """Navigate a dot-separated path through nested dicts/objects."""
    parts = path.split(".")
    current = obj
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        elif hasattr(current, part):
            current = getattr(current, part)
        else:
            return None
        if current is None:
            return None
    return current


def run_benchmark(dataset_name: str = "benchmark_a_synthetic") -> dict:
    """Run the full evaluation benchmark on a specific dataset."""
    dataset_dir = PROJECT_ROOT / "dataset" / dataset_name
    gt_dir = dataset_dir / "ground_truth"
    samples_dir = dataset_dir / "samples"

    if not gt_dir.exists():
        print(f"  No ground truth for {dataset_name}. Skipping.")
        return {}

    # Load ground truth
    samples = load_ground_truth(gt_dir)
    print(f"Loaded {len(samples)} ground truth samples from {dataset_name}")

    if not samples:
        return {}

    # Import pipeline components
    try:
        from backend.app.normalization import normalize_config
        from backend.app.vendors.detector import VendorDetector
        from backend.app.compliance.engine import ComplianceEngine
        from backend.app.compliance.loader import load_all_controls
    except ImportError as e:
        print(f"ERROR: Could not import pipeline components: {e}")
        return {}

    # Load compliance controls
    controls_dir = PROJECT_ROOT / "compliance" / "controls"
    controls = load_all_controls(controls_dir) if controls_dir.exists() else []
    engine = ComplianceEngine(controls)
    detector = VendorDetector()

    # Process each sample
    results: dict[str, dict] = {}
    for sample in samples:
        filename = sample["filename"]
        vendor = sample["_vendor"]

        # Find config file
        config_path = samples_dir / vendor / filename
        if not config_path.exists():
            print(f"  SKIP: {filename} (file not found)")
            continue

        raw_config = config_path.read_text(encoding="utf-8", errors="replace")

        # Vendor detection
        detection = detector.detect_vendor(raw_config)
        detected_vendor = detection.vendor if detection else "unknown"

        # Normalization
        try:
            norm_result = normalize_config(raw_config, vendor_hint=vendor)
            normalized_dict = norm_result.config.model_dump()
        except Exception as e:
            print(f"  ERROR normalizing {filename}: {e}")
            normalized_dict = {}
            norm_result = None

        # Compliance evaluation
        findings_dict = {}
        if norm_result:
            try:
                report = engine.evaluate(norm_result.config, norm_result.evidence)
                for finding in report.findings:
                    findings_dict[finding.control_id] = finding.status.value
            except Exception as e:
                print(f"  ERROR evaluating {filename}: {e}")

        results[filename] = {
            "detected_vendor": detected_vendor,
            "normalized_config": normalized_dict,
            "findings": findings_dict,
        }

    # Evaluate
    vendor_metrics = evaluate_vendor_detection(samples, results)
    norm_metrics = evaluate_normalization(samples, results)
    compliance_metrics = evaluate_compliance(samples, results)

    return {
        "dataset": dataset_name,
        "total_samples": len(samples),
        "processed": len(results),
        "vendor_detection": vendor_metrics,
        "normalization": norm_metrics,
        "compliance": compliance_metrics,
    }


def run_all_benchmarks():
    """Run all benchmarks and save results."""
    datasets = [
        "benchmark_a_synthetic",
        "benchmark_b_unseen",
        "benchmark_c_real_world",
        "benchmark_d_edge"
    ]
    
    all_reports = {}
    
    print("\n" + "=" * 60)
    print("NEXUS EVALUATION BENCHMARK SUITE")
    print("=" * 60)

    for ds in datasets:
        print(f"\n--- Running {ds} ---")
        report = run_benchmark(ds)
        if report:
            all_reports[ds] = report
            
            nm = report["normalization"]
            cm = report["compliance"]
            
            print(f"  Norm Accuracy: {nm['accuracy']:.1%} | Unknown Rate: {cm.get('unknown_rate', 0):.1%}")
            print(f"  Comp Precision: {cm.get('precision', 0):.1%} | Comp Recall: {cm.get('recall', 0):.1%}")

    # Save results
    results_path = PROJECT_ROOT / "evaluation" / "results.json"
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with open(results_path, "w") as f:
        json.dump(all_reports, f, indent=2)
    print(f"\nAll results saved to: {results_path}")


if __name__ == "__main__":
    run_all_benchmarks()
