"""
Top 1% Standards Verification Test Suite:
Tests Article Generator, Web App Evaluator, Lexical Uniqueness, and SVG Badges.
"""

import pytest
from src.generator import ArticleGenerator
from src.checkers.app_evaluator import WebAppAdSenseEvaluator
from src.checkers.uniqueness import UniquenessAnalyzer
from src.badge import generate_svg_badge
from src.mcp_server import handle_call_tool


def test_article_generator_completeness():
    topic = "Cognitive Perspective Architecture"
    article_md = ArticleGenerator.generate(topic, author_name="Oathan Rex")

    words = len(article_md.split())
    assert words >= 800, f"Generated article must be substantive, got {words} words"
    assert "Executive Summary & Key Takeaways" in article_md
    assert "Comparative Analysis Matrix" in article_md
    assert "Frequently Asked Questions" in article_md
    assert "FAQPage" in article_md
    assert "Oathan Rex" in article_md
    assert "The Comprehensive Guide to Cognitive Perspective Architecture" in article_md


def test_web_app_evaluator():
    app_html = """
    <html>
    <head><title>Online Audio Compressor Tool</title></head>
    <body>
        <div id="tool-container">
            <canvas id="audio-visualizer"></canvas>
            <input type="file" id="audio-input">
            <button id="compress-btn">Compress Audio Now</button>
        </div>
        <footer>
            <a href="/privacy">Privacy</a>
            <a href="/guide">Usage Guide & Theory</a>
        </footer>
    </body>
    </html>
    """
    is_app = WebAppAdSenseEvaluator.is_interactive_app(app_html, 45)
    assert is_app is True

    eval_res = WebAppAdSenseEvaluator.evaluate_app("https://audiotool.io", app_html, ["https://audiotool.io/guide"])
    assert eval_res["is_web_app"] is True
    assert "app_score" in eval_res
    assert len(eval_res["approval_roadmap"]) >= 3


def test_uniqueness_lexical_analyzer():
    dense_text = (
        "Architecting resilient distributed microservices demands deterministic boundary enforcement, "
        "comprehensive telemetry aggregation, asynchronous event queues, and rigorous fault isolation. "
        "Engineers must implement idempotent consumers alongside circuit breakers to neutralize cascading degradation."
    )
    res = UniquenessAnalyzer.evaluate(dense_text)
    assert res["total_tokens"] > 25
    assert res["raw_ttr"] > 0.6
    assert res["composite_lexical_score"] > 60.0
    assert not res["is_repetitive_or_spun"]


def test_svg_badge_generation():
    svg_passing = generate_svg_badge(95.0, "Ready")
    assert "<svg" in svg_passing
    assert "95/100" in svg_passing
    assert "#10b981" in svg_passing

    svg_failing = generate_svg_badge(45.0, "High Risk")
    assert "45/100" in svg_failing
    assert "#ef4444" in svg_failing


def test_mcp_generate_full_article_tool():
    res = handle_call_tool("generate_full_article", {"topic": "Zero-Trust Service Meshes"})
    assert "content" in res
    text = res["content"][0]["text"]
    assert "Zero-Trust Service Meshes" in text
    assert len(text.split()) >= 800
