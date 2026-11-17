"""
Comprehensive Tests for AdSenseReady-AI: Top 1% Standards
"""

import pytest
import json
from pathlib import Path

from src.auditor import AdSenseAuditor
from src.reporter import AuditReporter
from src.checkers.cms_detector import CMSDetector
from src.checkers.content_eeat import ContentEEATChecker
from src.mcp_server import handle_call_tool
from tests.mock_sites.sample_data import READY_SITE_HTML, REJECTED_SITE_HTML


def test_cms_detection():
    wp_html = "<html><head><meta name='generator' content='WordPress 6.4'></head><body><script src='/wp-includes/js/wp.js'></script></body></html>"
    result = CMSDetector.detect(wp_html)
    assert result["cms"] == "WordPress"
    assert any("Site Kit" in tip for tip in result["customized_tips"])

    ghost_html = "<html><head><meta name='generator' content='Ghost 5.0'></head><body></body></html>"
    ghost_res = CMSDetector.detect(ghost_html)
    assert ghost_res["cms"] == "Ghost"

    custom_html = "<html><head><title>My Handcrafted HTML</title></head><body></body></html>"
    custom_res = CMSDetector.detect(custom_html)
    assert custom_res["cms"] == "Custom / Static HTML"


def test_readability_calculation():
    checker = ContentEEATChecker({})
    text = (
        "Designing modern microservices requires strict boundary enforcement and clear domain separation. "
        "Engineers must ensure that independent services communicate asynchronously to handle high transaction volumes. "
        "By utilizing message brokers and automated caching layers, platform stability is maintained seamlessly."
    )
    score, rating = checker.calculate_readability(text)
    assert 0.0 <= score <= 100.0
    assert len(rating) > 0


def test_html_report_generation():
    auditor = AdSenseAuditor()
    report = auditor.audit_site("https://demotechjournal.com", mock_html=READY_SITE_HTML)
    html_output = AuditReporter.to_html(report)

    assert "<!DOCTYPE html>" in html_output
    assert "demotechjournal.com" in html_output
    assert "7-Pillar Detailed Evaluation" in html_output
    assert "score-number" in html_output
    assert "Prioritized Remediation Action Plan" in html_output


def test_mcp_explain_rejection_reason():
    res = handle_call_tool("explain_rejection_reason", {"reason": "Low Value Content"})
    assert "content" in res
    assert len(res["content"]) > 0
    text = res["content"][0]["text"]
    assert "How to Fix Google AdSense \"Low Value Content\"" in text
    assert "Article Count" in text
