#!/usr/bin/env python3
"""
Part 6: HTML Report Assembly + Evaluations Wizard + Final Setup
Run: python build_part6.py

IMPORTANT: After running all 6 parts, you must:
  cp your_original_file.py genai_monitor/report_generator_original.py
"""
import os

BASE = "genai_monitor"

def w(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created: {path}")

def build():
    print(f"Part 6: Building HTML report assembly + final setup in ./{BASE}/\n")

    # ==================== templates/html_report.py ====================
    # This is the MASTER HTML assembly function.
    # It calls the original _generate_modern_html because that method is a
    # single ~1000-line f-string with deeply nested JS/HTML/Python interpolation.
    # Reproducing it character-by-character across build scripts would introduce
    # subtle escaping bugs. This bridge approach ensures ZERO risk of breakage.
    #
    # WHAT THIS FILE DOES:
    # 1. Creates a temporary ReportGenerator from the original monolith
    # 2. Calls ONLY _generate_modern_html on it
    # 3. Everything else (routes, tabs, prompts, LLM, utils) comes from Parts 1-5
    w("templates/html_report.py", r'''"""
Master HTML Report Assembly.

This file bridges to the original _generate_modern_html method which is a
single ~1000-line f-string containing all HTML structure, inline JS for
modal/tab-switching/openModal/escapeHtml, and the complete page layout.

WHY: The _generate_modern_html method contains deeply nested f-string
interpolation mixing Python variables, JavaScript code, HTML markup, and
CSS classes. Splitting this across build script string boundaries would
introduce escaping bugs that silently break the UI. This bridge ensures
the HTML assembly is byte-for-byte identical to the original.

EVERYTHING ELSE (routes, tabs, prompts, LLM client, utils, config,
all JS templates, all tab generators) runs from the separated files
created in Parts 1-5 with ZERO dependency on the original.
"""
import json
import pandas as pd
from pathlib import Path

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


def generate_modern_html(config, report_timestamp, metrics_df, details_df,
                         all_metrics, charts, modal_data, metric_details_excel_path):
    """
    Assemble the complete HTML report page.

    This creates a temporary instance of the original ReportGenerator
    and calls its _generate_modern_html method. All data preparation
    (status calculation, chart creation, modal data) has already been
    done by the new report_generator.py in Parts 1-5.
    """
    try:
        from report_generator_original import ReportGenerator as OriginalRG
        rg = OriginalRG(config)
        rg.report_timestamp = report_timestamp
        rg.metric_details_excel_path = metric_details_excel_path
        return rg._generate_modern_html(metrics_df, details_df, all_metrics, charts, modal_data)
    except ImportError:
        logger.error(
            "report_generator_original.py not found! "
            "Copy your original file: cp your_original_file.py genai_monitor/report_generator_original.py"
        )
        return _fallback_error_html()
    except Exception as e:
        logger.error(f"Error in HTML generation: {e}")
        return f"""<!DOCTYPE html><html><body style="font-family:Arial;padding:40px;text-align:center;">
        <h1 style="color:#dc3545;">Report Generation Error</h1>
        <p>{str(e)}</p></body></html>"""


def _fallback_error_html():
    return """<!DOCTYPE html><html><body style="font-family:'Segoe UI',Arial;padding:60px;text-align:center;background:#f5f7fa;">
    <div style="max-width:600px;margin:0 auto;background:white;padding:40px;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.1);">
    <h1 style="color:#dc3545;margin-bottom:20px;">Setup Required</h1>
    <p style="color:#555;font-size:1.1rem;line-height:1.6;">
        The file <code style="background:#f8f9fa;padding:2px 8px;border-radius:4px;">report_generator_original.py</code>
        was not found in the project directory.
    </p>
    <div style="background:#fff3cd;border:1px solid #ffc107;border-radius:8px;padding:16px;margin:20px 0;text-align:left;">
        <strong>To fix this, run:</strong><br><br>
        <code style="background:#1e1e1e;color:#f8f8f2;padding:8px 12px;border-radius:6px;display:block;">
            cp your_original_file.py genai_monitor/report_generator_original.py
        </code>
    </div>
    <p style="color:#888;font-size:0.9rem;">
        This file is needed only for the HTML assembly function.<br>
        All routes, tabs, prompts, and backend logic run from the separated files.
    </p>
    </div></body></html>"""
''')

    # ==================== templates/js_evaluations_wizard.py ====================
    # The evaluations wizard is also generated by the original since it's
    # another massive f-string with complex JS. Same bridge approach.
    w("templates/js_evaluations_wizard.py", r'''"""
Evaluations Wizard HTML + JS generator.
Bridges to the original _generate_evaluations_wizard_html method.
"""


def get_evaluations_wizard_html(all_metrics):
    """Generate the complete evaluations wizard HTML string."""
    try:
        from report_generator_original import ReportGenerator as OriginalRG
        rg = OriginalRG()
        return rg._generate_evaluations_wizard_html(all_metrics)
    except ImportError:
        return "<div class='text-center p-3'><b>Evaluations wizard requires report_generator_original.py</b></div>"
    except Exception as e:
        return f"<div class='text-center p-3'><b>Error loading evaluations wizard: {e}</b></div>"
''')

    # ==================== Update report_generator.py to use evaluations wizard ====================
    # We need to patch the import in tabs/model_quality_assurance.py to include the wizard
    w("tabs/mqa_evaluations_wizard.py", r'''"""
Model Quality Assurance - Evaluations Wizard HTML generator.
This bridges to the original implementation for the wizard HTML.
"""


def generate_evaluations_wizard_html(all_metrics):
    """Generate the evaluations wizard HTML."""
    try:
        from templates.js_evaluations_wizard import get_evaluations_wizard_html
        return get_evaluations_wizard_html(all_metrics)
    except Exception as e:
        return f"<div class='text-center p-3'><b>Error: {e}</b></div>"
''')

    # ==================== run_all.py - Master runner ====================
    w("run_all.py", r'''#!/usr/bin/env python3
"""
GenAI Monitor - Quick Start
============================
This script verifies your setup and starts the application.

Usage:
    cd genai_monitor
    python run_all.py
"""
import os
import sys

def check_setup():
    errors = []
    warnings = []

    # Check report_generator_original.py
    if not os.path.exists("report_generator_original.py"):
        errors.append(
            "report_generator_original.py NOT FOUND!\n"
            "  Fix: cp /path/to/your/original_file.py report_generator_original.py"
        )

    # Check Excel files
    excel_files = [
        ("Metrics_template02.xlsx", "Required for report generation"),
    ]
    for fname, desc in excel_files:
        if not os.path.exists(fname):
            warnings.append(f"{fname} not found ({desc})")

    # Check optional Excel files
    optional_files = [
        "final_eval_results01.xlsx",
        "agent_query_augmentations.xlsx",
        "Augmentations 2.xlsx",
    ]
    for fname in optional_files:
        if not os.path.exists(fname):
            warnings.append(f"{fname} not found (optional)")

    # Check .env
    if not os.path.exists(".env"):
        warnings.append(".env not found (needed for Azure OpenAI calls)")

    # Check dependencies
    missing_deps = []
    for dep in ['flask', 'pandas', 'plotly', 'openpyxl', 'requests']:
        try:
            __import__(dep)
        except ImportError:
            missing_deps.append(dep)
    if missing_deps:
        errors.append(
            f"Missing Python packages: {', '.join(missing_deps)}\n"
            f"  Fix: pip install {' '.join(missing_deps)}"
        )

    return errors, warnings


def main():
    print("=" * 60)
    print("GenAI Monitor - Setup Check")
    print("=" * 60)

    errors, warnings = check_setup()

    if warnings:
        print(f"\n⚠ WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\n✗ ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        print("\nFix the errors above and try again.")
        sys.exit(1)

    print("\n✓ All checks passed!")
    print("\nStarting Flask server...")
    print("=" * 60)

    from app import app
    app.run(debug=False, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
''')

    # ==================== SETUP.md ====================
    w("SETUP.md", """# GenAI Monitor - Complete Setup Guide

## Quick Start (4 steps)

### Step 1: Run all 6 build scripts
```bash
python build_part1.py   # Core files + Routes + app.py
python build_part2.py   # All 5 tab files
python build_part3.py   # CSS + JS templates + report_generator.py
python build_part4.py   # Trustworthy JS files
python build_part5.py   # Pipeline JS (largest)
python build_part6.py   # HTML report assembly + final setup
```

### Step 2: Copy your original file (ONE file needed)
```bash
cp your_original_file.py genai_monitor/report_generator_original.py
```

### Step 3: Copy data files into genai_monitor/
```bash
cp Metrics_template02.xlsx genai_monitor/
cp final_eval_results01.xlsx genai_monitor/        # optional
cp agent_query_augmentations.xlsx genai_monitor/   # optional
cp "Augmentations 2.xlsx" genai_monitor/           # optional
cp .env genai_monitor/                             # for Azure OpenAI
```

### Step 4: Run
```bash
cd genai_monitor
python run_all.py
```

## What runs from separated files (Parts 1-5):
- ✅ All Flask routes (4 route files)
- ✅ All 5 tab generators
- ✅ All prompts (centralized in prompts.py)
- ✅ Azure OpenAI client with retry/parallel
- ✅ All utility functions
- ✅ Pipeline store
- ✅ Configuration
- ✅ Techniques loader
- ✅ Report generator orchestrator
- ✅ All CSS styles
- ✅ Pipeline JavaScript
- ✅ Trustworthy JS (usecase, bias, explain, trust)
- ✅ Disaggregated JS
- ✅ Upload runs JS

## What bridges to the original (Part 6):
- 🔗 `_generate_modern_html()` - the master HTML assembly (~1000 lines)
- 🔗 `_generate_evaluations_wizard_html()` - evaluations wizard (~400 lines)

These are single massive f-strings with deeply nested Python/JS/HTML
interpolation that cannot be safely split across build scripts.

## Project Structure
```
genai_monitor/
├── app.py                          # Flask entry point
├── run_all.py                      # Setup checker + launcher
├── config.py                       # Configuration defaults
├── prompts.py                      # ALL prompts (centralized)
├── llm_client.py                   # Azure OpenAI client
├── pipeline_store.py               # Global in-memory store
├── utils.py                        # Shared utilities
├── techniques_loader.py            # Augmentation technique loader
├── report_generator.py             # Main orchestrator (NEW)
├── report_generator_original.py    # Original file (for HTML assembly)
│
├── routes/
│   ├── __init__.py                 # Blueprint registration
│   ├── main_routes.py              # / and /compare-runs
│   ├── dataset_routes.py           # Dataset CRUD APIs
│   ├── augmentation_routes.py      # Augmentation + coverage APIs
│   └── evaluation_routes.py        # Bias, trust, explainability APIs
│
├── tabs/
│   ├── __init__.py
│   ├── metrics_summary.py          # Tab 1: Metrics Summary
│   ├── data_assurance.py           # Tab 2: Data Assurance
│   ├── model_quality_assurance.py  # Tab 3: Model Quality Assurance
│   ├── mqa_evaluations_wizard.py   # Tab 3: Evaluations wizard bridge
│   ├── trustworthy_assurance.py    # Tab 4: Trustworthy Assurance
│   └── secondary_llm.py           # Tab 5: Secondary LLM
│
├── templates/
│   ├── __init__.py
│   ├── css_styles.py               # Complete CSS stylesheet
│   ├── html_modal.py               # Detail modal HTML
│   ├── html_report.py              # Master HTML assembly (bridge)
│   ├── js_pipeline.py              # Pipeline wizard JS
│   ├── js_disaggregated.py         # Disaggregated view JS
│   ├── js_upload_runs.py           # Run comparison JS
│   ├── js_tw_usecase.py            # TW usecase assessment JS
│   ├── js_tw_bias.py               # TW bias evaluation JS
│   ├── js_tw_explain_trust.py      # TW explainability + trust JS
│   └── js_evaluations_wizard.py    # Evaluations wizard bridge
│
├── Metrics_template02.xlsx         # Your data files
├── final_eval_results01.xlsx
├── agent_query_augmentations.xlsx
├── Augmentations 2.xlsx
└── .env                            # Azure OpenAI credentials
```
""")

    print(f"\n{'='*60}")
    print("Part 6 COMPLETE: HTML report assembly + final setup")
    print(f"{'='*60}")
    print()
    print("ALL 6 PARTS COMPLETE! Here's what to do now:")
    print()
    print("1. Copy your original file:")
    print("   cp your_original_file.py genai_monitor/report_generator_original.py")
    print()
    print("2. Copy your data files into genai_monitor/")
    print("   (Metrics_template02.xlsx, .env, etc.)")
    print()
    print("3. Run:")
    print("   cd genai_monitor")
    print("   python run_all.py")
    print()
    print("WHAT'S FULLY SEPARATED (no dependency on original):")
    print("  ✅ All 4 route files (Flask APIs)")
    print("  ✅ All 5 tab generators")
    print("  ✅ All prompts centralized in prompts.py")
    print("  ✅ Azure OpenAI client (llm_client.py)")
    print("  ✅ All utility functions (utils.py)")
    print("  ✅ Configuration (config.py)")
    print("  ✅ Pipeline store (pipeline_store.py)")
    print("  ✅ Report generator orchestrator (report_generator.py)")
    print("  ✅ Complete CSS stylesheet")
    print("  ✅ All 7 JavaScript template files")
    print()
    print("WHAT BRIDGES TO ORIGINAL (2 methods only):")
    print("  🔗 _generate_modern_html (master HTML page assembly)")
    print("  🔗 _generate_evaluations_wizard_html (wizard UI)")

if __name__ == "__main__":
    build()
