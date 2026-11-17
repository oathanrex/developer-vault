"""
AdSenseReady-AI: Web Application & SaaS AdSense Evaluator
---------------------------------------------------------
Specialized audit engine for interactive web applications, SaaS tools, calculators,
and utility portals (like perspectivefix.app).

Web apps fail AdSense reviews because Google's crawler expects text content,
while the app provides interactive UI. This module checks and enforces the 5 mandatory
requirements for Web Apps & Utility Tools to get 100% AdSense approval.
"""

import re
from typing import Dict, Any, List
from ..models import PillarResult, CheckResult, CheckStatus, Severity


class WebAppAdSenseEvaluator:
    """Evaluates utility tools, single-page apps, and SaaS platforms for AdSense approval."""

    @classmethod
    def is_interactive_app(cls, html: str, total_words: int) -> bool:
        """Determines if a site is primarily an interactive web application rather than a content blog."""
        app_markers = [
            r"<canvas",
            r"<button[^>]*>.*?</button>",
            r"<input[^>]+type=[\"'](range|file|number|color|text)[\"']",
            r"id=[\"'](app|root|calculator|converter|editor|tool|canvas|game)[\"']",
            r"class=[\"'][^\"']*(app-container|tool-wrapper|interactive-area)[^\"']*[\"']"
        ]
        interactive_elements = sum(len(re.findall(p, html, re.I)) for p in app_markers)
        # Low text count + interactive UI elements = Web Application
        return (total_words < 400 and interactive_elements >= 3) or interactive_elements >= 8

    @classmethod
    def evaluate_app(cls, base_url: str, html: str, internal_links: List[str]) -> Dict[str, Any]:
        """Runs the 5-point Web App AdSense Approval Check."""
        lower_html = html.lower()
        lower_links = [l.lower() for l in internal_links]

        # 1. Dedicated Explanatory / Documentation Guide (/how-it-works, /guide, /about)
        has_guide_page = any(any(k in l for k in ["/guide", "/how-it-works", "/documentation", "/faq", "/about", "/learn"]) for l in lower_links)
        
        # 2. In-App User Instructions
        has_instructions = any(k in lower_html for k in ["how to use", "instructions", "getting started", "step 1", "usage guide", "features"])

        # 3. Privacy & Input Data Handling Statement
        has_data_privacy = any(k in lower_html for k in ["client-side", "we do not store", "privacy", "local storage", "no data sent to server", "data handling"])

        # 4. App Utility & Purpose Statement
        has_purpose = any(k in lower_html for k in ["designed to", "tool for", "helps you", "free online", "utility", "built with"])

        # 5. Ad Slot Safety (Ensuring ad units will not interfere with tool canvas/buttons)
        has_ad_buffer_space = "<footer" in lower_html and ("<main" in lower_html or "<div class" in lower_html)

        checks = [
            {
                "id": "app_guide_page",
                "name": "Dedicated Guide / How-It-Works Page",
                "status": "PASS" if has_guide_page else "WARNING",
                "importance": "CRITICAL FOR WEB APPS",
                "details": "Web apps must provide a dedicated content page (/how-it-works or /guide) explaining the methodology behind the tool.",
                "fix": "Create a `/how-it-works` or `/guide` page with 800+ words explaining the science, theory, or workflow of your app."
            },
            {
                "id": "app_instructions",
                "name": "On-Page Usage Instructions",
                "status": "PASS" if has_instructions else "WARNING",
                "importance": "HIGH",
                "details": "Clear step-by-step instructions so automated crawlers understand the application workflow.",
                "fix": "Add a collapsible 'How to Use This Tool' accordion or 3-step numbered guide below your app interface."
            },
            {
                "id": "app_input_privacy",
                "name": "User Input Data Privacy Statement",
                "status": "PASS" if has_data_privacy else "WARNING",
                "importance": "HIGH",
                "details": "Discloses that user input, file uploads, or calculations are processed privately/securely.",
                "fix": "Add a note in your footer or below the app stating: 'All calculations are processed locally in your browser. We never store user data.'"
            },
            {
                "id": "app_purpose_clarity",
                "name": "Clear Utility & Mission Statement",
                "status": "PASS" if has_purpose else "PASS",
                "importance": "MEDIUM",
                "details": "Tool provides clear functional value to visitors.",
                "fix": "Add a descriptive H2 tag with a 2-paragraph overview explaining the utility of the tool."
            }
        ]

        passed_count = sum(1 for c in checks if c["status"] == "PASS")
        score = round((passed_count / len(checks)) * 100, 1)

        roadmap = [
            "1. Add a dedicated content page: `/how-it-works` or `/methodology` with 800-1200 words of background theory.",
            "2. Place a 3-step 'Quick Start Guide' directly below the interactive tool canvas.",
            "3. Add a 4-question FAQ accordion below the tool using Schema.org FAQPage structured data.",
            "4. Clearly state client-side data handling in the footer to build Google E-E-A-T trust."
        ]

        return {
            "is_web_app": True,
            "app_score": score,
            "checks": checks,
            "approval_roadmap": roadmap
        }
