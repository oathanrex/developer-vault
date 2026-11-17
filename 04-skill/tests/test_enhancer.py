"""
Tests for Low-Value Content Eliminator
"""

import pytest
from src.enhancer import LowValueContentEliminator
from src.mcp_server import handle_call_tool


def test_diagnose_thin_content():
    eliminator = LowValueContentEliminator()
    thin_text = "This is a brief article about microservices architecture. It has very few words."
    diag = eliminator.diagnose(thin_text, title="Microservices Guide")

    assert diag["current_word_count"] < 100
    assert diag["risk_level"] == "CRITICAL"
    assert diag["words_needed"] > 900
    assert len(diag["structural_gaps"]) >= 3
    assert not diag["ready_for_adsense"]


def test_generate_expansion_plan():
    eliminator = LowValueContentEliminator()
    plan = eliminator.generate_expansion_plan("Database Sharding", "A brief intro to database sharding.", author_name="Oathan Rex")

    assert "diagnosis" in plan
    assert "blueprint_instructions" in plan
    assert "sample_faq_items" in plan
    assert len(plan["sample_faq_items"]) >= 3
    assert "@type\": \"FAQPage" in plan["faq_schema_ldjson"]
    assert "Written by Oathan Rex" in plan["eeat_author_box_html"]


def test_mcp_low_value_content_tools():
    # Test diagnose_thin_content MCP tool
    diag_res = handle_call_tool("diagnose_thin_content", {"content": "Very short post."})
    assert "CRITICAL" in diag_res["content"][0]["text"]

    # Test eliminate_low_value_content MCP tool
    elim_res = handle_call_tool("eliminate_low_value_content", {
        "topic": "Cloud Scaling",
        "current_content": "Cloud scaling is useful for web applications.",
        "author_name": "Oathan Rex"
    })
    assert "FAQPage" in elim_res["content"][0]["text"]
    assert "Written by Oathan Rex" in elim_res["content"][0]["text"]
