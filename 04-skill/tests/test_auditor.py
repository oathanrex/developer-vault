"""
Unit and Integration Tests for AdSenseReady-AI
"""

import pytest
import json
from pathlib import Path
from src.auditor import AdSenseAuditor
from src.reporter import AuditReporter
from tests.mock_sites.sample_data import READY_SITE_HTML, REJECTED_SITE_HTML

BASE_DIR = Path(__file__).resolve().parent.parent


def test_policy_json_validity():
    """Verify that policies/adsense_rules.json is well-formed and contains all 7 pillars."""
    rules_file = BASE_DIR / "policies" / "adsense_rules.json"
    assert rules_file.exists(), "adsense_rules.json must exist"

    with open(rules_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "pillars" in data
    pillars = data["pillars"]
    assert "legal_trust" in pillars
    assert "content_eeat" in pillars
    assert "technical_seo" in pillars
    assert "site_navigation_ux" in pillars
    assert "google_publisher_policy" in pillars
    assert "ad_layout_readiness" in pillars
    assert "organic_footprint" in pillars


def test_ready_site_approval():
    """Test that a compliant website achieves high score with 0 blockers."""
    auditor = AdSenseAuditor()
    report = auditor.audit_site("https://demotechjournal.com", mock_html=READY_SITE_HTML)

    assert report.total_score > 0
    assert report.normalized_score >= 80.0
    assert len(report.all_blockers) == 0, f"Compliant site should have 0 blockers, found: {[b.name for b in report.all_blockers]}"
    assert report.verdict == "APPROVED_READY"

    # Verify markdown generation
    md = AuditReporter.to_markdown(report)
    assert "# 🎯 Google AdSense Readiness Audit Report" in md
    assert "APPROVED_READY" in md or "READY FOR ADSENSE APPROVAL" in md

    # Verify JSON output
    js = AuditReporter.to_json(report)
    parsed = json.loads(js)
    assert parsed["verdict"] == "APPROVED_READY"


def test_rejected_site_flags_blockers():
    """Test that a non-compliant spam/piracy site triggers multiple critical blockers."""
    auditor = AdSenseAuditor()
    report = auditor.audit_site("https://badspamsite.com", mock_html=REJECTED_SITE_HTML)

    assert len(report.all_blockers) > 0, "Non-compliant site must trigger blockers"
    blocker_ids = [b.id for b in report.all_blockers]

    # Must catch prohibited niche, fake download buttons, noindex, and placeholder text
    assert "banned_niche_detection" in blocker_ids
    assert "deceptive_ui_buttons" in blocker_ids
    assert "search_console_indexing_signals" in blocker_ids
    assert "zero_placeholder_pages" in blocker_ids

    assert report.verdict == "REJECTION_GUARANTEED"
