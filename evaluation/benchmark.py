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

            if actual_status == "UNKNOWN":
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


def run_benchmark() -> dict:
    """Run the full evaluation benchmark."""
    gt_dir = PROJECT_ROOT / "dataset" / "ground_truth"
    samples_dir = PROJECT_ROOT / "dataset" / "samples"

    if not gt_dir.exists():
        print(f"ERROR: Ground truth directory not found: {gt_dir}")
        return {}

    # Load ground truth
    samples = load_ground_truth(gt_dir)
    print(f"Loaded {len(samples)} ground truth samples")

    # Import pipeline components
    try:
        from backend.app.normalization import normalize_config
        from backend.app.vendors.detector import VendorDetector
        from backend.app.compliance.engine import ComplianceEngine
        from backend.app.compliance.loader import load_all_controls
    except ImportError as e:
        print(f"ERROR: Could not import pipeline components: {e}")
        print("Make sure all modules are implemented.")
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
        print(f"  OK: {filename} ({detected_vendor}, {len(findings_dict)} checks)")

    # Evaluate
    vendor_metrics = evaluate_vendor_detection(samples, results)
    norm_metrics = evaluate_normalization(samples, results)
    compliance_metrics = evaluate_compliance(samples, results)

    report = {
        "total_samples": len(samples),
        "processed": len(results),
        "vendor_detection": vendor_metrics,
        "normalization": norm_metrics,
        "compliance": compliance_metrics,
    }

    # Print summary
    print("\n" + "=" * 60)
    print("NEXUS EVALUATION BENCHMARK RESULTS")
    print("=" * 60)
    print(f"\nSamples: {report['total_samples']} | Processed: {report['processed']}")
    print(f"\nVendor Detection:")
    print(f"  Accuracy: {vendor_metrics['accuracy']:.1%} ({vendor_metrics['correct']}/{vendor_metrics['total']})")
    print(f"\nNormalization:")
    print(f"  Accuracy: {norm_metrics['accuracy']:.1%} ({norm_metrics['correct']}/{norm_metrics['total']})")
    print(f"\nCompliance:")
    print(f"  Accuracy:  {compliance_metrics['accuracy']:.1%}")
    print(f"  Precision: {compliance_metrics['precision']:.1%}")
    print(f"  Recall:    {compliance_metrics['recall']:.1%}")
    print(f"  F1 Score:  {compliance_metrics['f1_score']:.1%}")
    print(f"  FP Rate:   {compliance_metrics['false_positive_rate']:.1%}")
    print(f"  FN Rate:   {compliance_metrics['false_negative_rate']:.1%}")
    print(f"  Unknown:   {compliance_metrics['unknown_rate']:.1%}")
    print(f"\n  TP={compliance_metrics['true_positives']} TN={compliance_metrics['true_negatives']} FP={compliance_metrics['false_positives']} FN={compliance_metrics['false_negatives']} UNK={compliance_metrics['unknowns']}")

    # Save results
    results_path = PROJECT_ROOT / "evaluation" / "results.json"
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with open(results_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nResults saved to: {results_path}")

    return report


if __name__ == "__main__":
    run_benchmark()
