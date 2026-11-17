# CLAUDE.md - AdSenseReady-AI Guidelines for Claude Code

## Project Overview
AdSenseReady-AI is an open-source 360-degree audit engine and universal AI skill designed to evaluate websites against Google AdSense publisher approval criteria with 10/10 precision.

## Core Commands
- Audit a website: `python -m src.cli <url>`
- Export markdown audit report: `python -m src.cli <url> --format markdown --output report.md`
- Export JSON audit report: `python -m src.cli <url> --format json --output report.json`
- Sync with live Google policies: `python scripts/sync_policies.py`
- Run test suite: `python -m pytest tests/`
- Run demo benchmark: `python -m src.cli --demo`

## Architecture & Code Standards
- **Python Version**: Python 3.8+ compatible, robust fallback when optional packages are absent.
- **7-Pillar Modular Design**: Each evaluation pillar resides in `src/checkers/<pillar>.py`.
- **Policy Storage**: All criteria are versioned and stored in `policies/adsense_rules.json`.
- **Severity Levels**:
  - `BLOCKER`: Guaranteed instant rejection by Google. Must be fixed first.
  - `HIGH`: Substantial negative impact; likely rejection.
  - `MEDIUM`: Quality penalty.
  - `LOW`: Best practice.

## When Responding to User Inquiries
- Always cite the relevant official Google policy source when explaining rejections.
- Prioritize fixes in order of impact (Blockers first, then High-priority fixes).
- Maintain an encouraging, top-tier engineering tone.
