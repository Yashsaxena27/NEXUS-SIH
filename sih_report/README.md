# SIH 26155 — NEXUS Master Technical Research Report Generator

## What This Is

A PDF generator that produces a comprehensive **100+ page** technical research report about SIH 2026 Problem Statement 26155 — "AI-Driven Multi-Vendor Network Security Compliance Auditor".

This project does **NOT** implement the NEXUS application. It generates a professional PDF report from pre-researched content.

## Quick Start

```bash
# 1. Install dependencies
cd sih_report
pip install -r requirements.txt

# 2. Generate the report
python generate_report.py

# 3. Find your PDF
# Output: output/SIH_26155_NEXUS_Master_Report.pdf
```

## Project Structure

```
sih_report/
├── generate_report.py           # Main entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── content/
│   ├── __init__.py              # Content assembly
│   ├── part1.py                 # Sections 1–13
│   ├── part2.py                 # Sections 14–26
│   └── part3.py                 # Sections 27–39
│
├── diagrams/
│   └── generate_diagrams.py     # Programmatic diagram generation
│
├── styles/
│   └── report.css               # Professional CSS stylesheet
│
└── output/
    └── SIH_26155_NEXUS_Master_Report.pdf  (generated)
```

## Requirements

- Python 3.10+
- WeasyPrint system dependencies (see [WeasyPrint docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html))

### Windows

WeasyPrint requires GTK libraries. Install via:

```bash
pip install weasyprint
```

If you encounter issues, install GTK3 runtime from https://github.com/nickvdp/gtk3-install or use MSYS2.

## Output

- **File:** `SIH_26155_NEXUS_Master_Report.pdf`
- **Pages:** 120–150 (all content preserved from both research documents)
- **Diagrams:** 12 programmatic architecture/flow diagrams
- **Sections:** 39 major sections covering problem analysis, architecture, compliance, AI/ML, datasets, and SIH strategy
