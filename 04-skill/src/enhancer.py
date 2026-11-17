"""
AdSenseReady-AI: Low-Value Content Eliminator & E-E-A-T Content Maximizer
------------------------------------------------------------------------
Analyzes thin/shallow web articles and transforms them into 1200+ word,
Google-compliant, high-substance publications with rich E-E-A-T signals.
"""

import re
import json
from typing import Dict, Any, List, Optional, Tuple
from .checkers.content_eeat import ContentEEATChecker

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


class LowValueContentEliminator:
    """Diagnoses thin content and generates comprehensive expansion blueprints."""

    EXPANSION_PILLARS = [
        "First-Hand Experience / Practical Implementation Example",
        "Common Pitfalls & Architectural Countermeasures",
        "Comparative Analysis Matrix (Pros, Cons, Alternatives)",
        "Structured Step-by-Step Execution Blueprint",
        "Google Search People Also Ask (PAA) Schema FAQ Section",
        "Authoritative E-E-A-T Bio & Editorial Disclosure"
    ]

    def __init__(self):
        self.eeat_checker = ContentEEATChecker({})

    def extract_text(self, html_or_text: str) -> str:
        if "<html" in html_or_text.lower() or "<article" in html_or_text.lower() or "<div" in html_or_text.lower():
            return self.eeat_checker.extract_main_text(html_or_text)
        return " ".join(html_or_text.split())

    def diagnose(self, text_or_html: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Runs a diagnostic audit on the article to pinpoint thin content risks."""
        plain_text = self.extract_text(text_or_html)
        words = plain_text.split()
        word_count = len(words)

        readability_score, readability_label = self.eeat_checker.calculate_readability(plain_text)

        # Detect structural gaps
        has_faq = bool(re.search(r"(faq|frequently asked questions|\bquestions\b)", text_or_html, re.I))
        has_table = bool(re.search(r"<table", text_or_html, re.I))
        has_headings = bool(re.search(r"<h[23]", text_or_html, re.I))
        has_author = bool(re.search(r"(written by|author|byline|about the author)", text_or_html, re.I))
        has_bullet_points = bool(re.search(r"(<ul|<ol|\b1\.\s|\b•\s)", text_or_html, re.I))

        # Thin content risk calculation
        risk_level = "CRITICAL" if word_count < 500 else ("HIGH" if word_count < 750 else ("MODERATE" if word_count < 1000 else "LOW"))

        deficits = []
        if word_count < 750:
            deficits.append(f"Substance Deficit: {word_count} words is below the safe 800-1200+ threshold.")
        if not has_faq:
            deficits.append("Missing FAQ Section: No 'People Also Ask' question cluster detected.")
        if not has_author:
            deficits.append("Missing E-E-A-T Signature: No author attribution or editorial credentials found.")
        if not has_table:
            deficits.append("Missing Data Representation: No comparison or summary table found.")
        if not has_bullet_points:
            deficits.append("Scannability Deficit: Content lacks bulleted lists or step-by-step breakdown.")

        target_additional_words = max(0, 1000 - word_count)

        return {
            "title": title or "Analyzed Article",
            "current_word_count": word_count,
            "target_word_count": 1200,
            "words_needed": target_additional_words,
            "risk_level": risk_level,
            "readability_score": readability_score,
            "readability_label": readability_label,
            "structural_gaps": deficits,
            "ready_for_adsense": risk_level == "LOW" and has_author
        }

    def generate_expansion_plan(self, topic: str, current_content: str, author_name: str = "Editorial Team") -> Dict[str, Any]:
        """Generates a structured, production-ready blueprint to expand thin articles into 1000-1500+ words."""
        diagnosis = self.diagnose(current_content, title=topic)

        prompt_instructions = f"""
### Comprehensive High-Value Article Expansion Blueprint
Target Topic: {topic}
Current Word Count: {diagnosis['current_word_count']} words | Target: 1,200+ words
Author / Publisher: {author_name}

To eliminate Google AdSense 'Low Value Content' rejections, incorporate these exact 6 structural sections:

1. **Executive Key Takeaways / Summary Box (Above the fold)**
   - 3-4 bullet points highlighting the core resolution or insight.

2. **Core Deep-Dive & Real-World Case Study (400-500 words)**
   - Replace shallow dictionary definitions with practical implementation details.
   - Include specific numbers, benchmarks, or actionable real-world scenarios.

3. **Comparative Analysis Table (Markdown or HTML Table)**
   - Contrast 3-4 options, approaches, or configurations across key criteria (Efficiency, Cost, Complexity, Trade-offs).

4. **Common Mistakes & Countermeasures (250-300 words)**
   - Outline 3 typical errors beginners or professionals make, and exact step-by-step solutions.

5. **Schema-Ready People Also Ask (PAA) FAQs (3-4 Questions)**
   - Answer high-intent questions in direct, authoritative 2-3 sentence answers.

6. **E-E-A-T Author Credentials Box**
   - Verified author profile explaining years of experience and domain authority.
"""

        sample_faq = [
            {
                "question": f"What is the most effective approach to {topic}?",
                "answer": f"The most reliable method involves systematic decoupling of dependencies, continuous validation, and establishing baseline performance benchmarks prior to optimization."
            },
            {
                "question": f"What are common mistakes when dealing with {topic}?",
                "answer": f"The most frequent pitfall is premature optimization without adequate observability, leading to unnecessary complexity and maintenance overhead."
            },
            {
                "question": f"How long does it take to see results from {topic}?",
                "answer": f"Typical implementation cycles range from a few days for fundamental configurations to 2-4 weeks for enterprise-grade deployments."
            }
        ]

        faq_schema_json = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["question"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item["answer"]
                    }
                }
                for item in sample_faq
            ]
        }

        author_box_html = f"""
<div class="author-eeat-box" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-top: 2rem; background: #f8fafc;">
    <div style="display: flex; gap: 1rem; align-items: center;">
        <div style="width: 56px; height: 56px; border-radius: 50%; background: #3b82f6; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.25rem;">
            {author_name[:1]}
        </div>
        <div>
            <h4 style="margin: 0; font-size: 1.1rem; color: #1e293b;">Written by {author_name}</h4>
            <p style="margin: 0.25rem 0 0; font-size: 0.9rem; color: #64748b;">Domain Specialist & Technical Editor | Verified Industry Practitioner</p>
        </div>
    </div>
    <p style="margin-top: 1rem; font-size: 0.92rem; color: #334155; line-height: 1.5;">
        This article has been researched, formatted, and fact-checked according to strict editorial quality guidelines to provide original, actionable, and verified technical insights.
    </p>
</div>
"""

        return {
            "diagnosis": diagnosis,
            "blueprint_instructions": prompt_instructions,
            "sample_faq_items": sample_faq,
            "faq_schema_ldjson": json.dumps(faq_schema_json, indent=2),
            "eeat_author_box_html": author_box_html
        }
