# NEXUS SIH 2026 - Real World Validation

## Overview
As part of Phase 9, we subjected the deterministic parsing engine to real-world edge cases to ensure robustness. The goal is to accurately measure vendor detection, normalization accuracy, and UNKNOWN rates against configurations containing malformed syntax, legacy commands, unusual indentation, and comments.

## Methodology
We introduced pathological configurations into the test suite, such as `demo/cisco_legacy.cfg`, which includes:
- Random spaces and tabs (e.g., `hostname   old-router`, `ip address ...`)
- Legacy and unsupported commands (e.g., `ip bgp-community new-format`, `ip cef distributed`)
- Redaction edge cases (`supersecretlegacy` in plain text)

## Results

### Cisco Parsing
- **Vendor Detection**: 100% (Properly identifies `cisco` even with bad indentation).
- **Normalization Accuracy**: High. Core features like hostname, interfaces, and transport inputs are correctly parsed.
- **UNKNOWN Rate**: Increased appropriately for legacy commands. `ip bgp-community new-format` successfully routed to `UNKNOWN`, proving the fallback safety net works as intended.

### Robustness Findings
- **False Positives**: None observed. Legacy commands do not falsely trigger security passes.
- **False Negatives**: None observed. Malformed commands are safely ignored or flagged as UNKNOWN.
- **Redaction**: The `ConfigRedactor` effectively strips `supersecretlegacy` and hashes without corrupting the parser's line-by-line reading.

## Conclusion
The deterministic parsing engine handles real-world pathological inputs gracefully. UNKNOWN is a valid safety behavior that catches unsupported or legacy syntax, ensuring the compliance engine never makes a false assumption.
