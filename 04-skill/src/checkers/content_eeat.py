"""
Pillar 2: Content Depth, Originality & E-E-A-T Quality Checker
Advanced semantic analysis, Flesch Reading Ease, and anti-AI-spam validation.
"""

import re
from typing import List, Dict, Any, Tuple
from ..models import PillarResult, CheckResult, CheckStatus, Severity

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


class ContentEEATChecker:
    def __init__(self, rules: Dict[str, Any]):
        self.rules = rules.get("pillars", {}).get("content_eeat", {})
        self.weight = self.rules.get("weight", 25)

    def extract_main_text(self, html: str) -> str:
        """Extracts substantive article content, removing headers, footers, nav, and sidebars."""
        if HAS_BS4:
            soup = BeautifulSoup(html, "html.parser")
            # Remove irrelevant or noisy tags
            for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form", "noscript"]):
                tag.decompose()

            # Look for explicit content containers
            content_container = (
                soup.find("article") or
                soup.find("main") or
                soup.find(class_=re.compile(r"(post|entry|article|content|body)-content", re.I)) or
                soup.find(id=re.compile(r"(post|entry|article|content|body)", re.I)) or
                soup.body
            )
            if content_container:
                return " ".join(content_container.get_text().split())
            return " ".join(soup.get_text().split())
        else:
            cleaned = re.sub(r"<(script|style|nav|footer|header|aside)[^>]*>.*?</\1>", " ", html, flags=re.DOTALL | re.IGNORECASE)
            cleaned = re.sub(r"<[^>]+>", " ", cleaned)
            return " ".join(cleaned.split())

    @staticmethod
    def _count_syllables(word: str) -> int:
        """Estimates syllable count of an English word."""
        word = word.lower().strip(".:;?!")
        if not word:
            return 1
        count = len(re.findall(r"[aeiouy]+", word))
        if word.endswith("e") and not word.endswith("le") and count > 1:
            count -= 1
        return max(1, count)

    def calculate_readability(self, text: str) -> Tuple[float, str]:
        """Calculates Flesch-Kincaid Reading Ease (0-100)."""
        words = text.split()
        if len(words) < 30:
            return 60.0, "Sample too small"

        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 3]
        total_sentences = max(1, len(sentences))
        total_words = len(words)
        total_syllables = sum(self._count_syllables(w) for w in words)

        # Flesch Reading Ease Formula: 206.835 - 1.015*(words/sentences) - 84.6*(syllables/words)
        score = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)
        score = round(max(0.0, min(100.0, score)), 1)

        if score >= 70:
            rating = "Easy & Engaging (General Audience)"
        elif score >= 50:
            rating = "Optimal & Clear (Standard Web Reader)"
        elif score >= 30:
            rating = "Dense / Professional (Specialized Audience)"
        else:
            rating = "Extremely Complex / Robotic"

        return score, rating

    def run(self, article_urls: List[str], article_pages: Dict[str, str]) -> PillarResult:
        pillar = PillarResult(
            id="content_eeat",
            name="Content Depth, Originality & E-E-A-T Quality",
            weight=self.weight,
            earned_score=0.0,
            max_score=0.0,
            checks=[]
        )

        total_articles = len(article_urls)

        # 1. Total Article Volume
        if total_articles >= 25:
            pillar.checks.append(CheckResult(
                id="minimum_article_count",
                name="Article Inventory Volume",
                status=CheckStatus.PASS,
                severity=Severity.BLOCKER,
                score=6.0,
                max_score=6.0,
                details=f"Healthy publication volume detected ({total_articles} substantive posts found). Meets Google manual review criteria.",
                doc_url="https://support.google.com/adsense/answer/10502938"
            ))
            pillar.earned_score += 6.0
        elif total_articles >= 15:
            pillar.checks.append(CheckResult(
                id="minimum_article_count",
                name="Article Inventory Volume",
                status=CheckStatus.WARNING,
                severity=Severity.BLOCKER,
                score=3.5,
                max_score=6.0,
                details=f"Borderline article volume ({total_articles} posts). Google manual raters expect 20-30+ fully fleshed posts.",
                fix_recommendation="Publish at least 10 more original, high-substance articles before submitting to AdSense.",
                doc_url="https://support.google.com/adsense/answer/10502938"
            ))
            pillar.earned_score += 3.5
        else:
            pillar.checks.append(CheckResult(
                id="minimum_article_count",
                name="Article Inventory Volume",
                status=CheckStatus.FAIL,
                severity=Severity.BLOCKER,
                score=1.0,
                max_score=6.0,
                details=f"Critically low article volume ({total_articles} posts found). Immediate risk of 'Site Under Construction' or 'Low Value Content'.",
                fix_recommendation="Publish a minimum of 20 to 30 comprehensive, original articles prior to application.",
                doc_url="https://support.google.com/adsense/answer/10502938"
            ))
            pillar.earned_score += 1.0
        pillar.max_score += 6.0

        # Sample word counts across crawled articles
        word_counts = []
        ai_cliches_found = []
        headings_ok = 0
        authors_found = 0
        images_with_alt = 0
        total_images = 0
        readability_scores = []

        ai_cliche_patterns = [
            r"in conclusion,?\s+it is (important|crucial|essential)",
            r"as an ai language model",
            r"delve into the (world|realm|tapestry)",
            r"in this fast-paced (world|digital era|landscape)",
            r"a testament to",
            r"without further ado",
            r"tapestry of modern",
            r"beacon of hope",
            r"ever-evolving landscape",
            r"it is worth noting that",
            r"in summary, it's clear that"
        ]

        for url, html in article_pages.items():
            plain_text = self.extract_main_text(html)
            words = plain_text.split()
            word_count = len(words)
            word_counts.append(word_count)

            # Readability
            if word_count > 50:
                r_score, _ = self.calculate_readability(plain_text)
                readability_scores.append(r_score)

            # Check AI markers
            lower_text = plain_text.lower()
            for pattern in ai_cliche_patterns:
                if re.search(pattern, lower_text):
                    ai_cliches_found.append(pattern)

            # Check Headings
            h1_count = len(re.findall(r"<h1[^>]*>", html, re.IGNORECASE))
            h2_count = len(re.findall(r"<h2[^>]*>", html, re.IGNORECASE))
            if h1_count >= 1 and h2_count >= 1:
                headings_ok += 1

            # Check Author Attribution (E-E-A-T)
            if any(k in lower_text for k in ["written by", "by ", "author:", "author bio", "published by", "reviewed by"]) or "class=\"byline\"" in html.lower() or "rel=\"author\"" in html.lower():
                authors_found += 1

            # Images & Alt
            imgs = re.findall(r"<img[^>]+>", html, re.IGNORECASE)
            total_images += len(imgs)
            for img in imgs:
                if 'alt="' in img.lower() and not 'alt=""' in img.lower():
                    images_with_alt += 1

        avg_words = int(sum(word_counts) / len(word_counts)) if word_counts else 0
        avg_readability = round(sum(readability_scores) / len(readability_scores), 1) if readability_scores else 60.0

        # 2. Average Word Count (Thin Content Check)
        if avg_words >= 800:
            pillar.checks.append(CheckResult(
                id="average_word_count",
                name="Article Depth & Substance (Avg Word Count)",
                status=CheckStatus.PASS,
                severity=Severity.BLOCKER,
                score=5.0,
                max_score=5.0,
                details=f"High substantive depth: Average article length is {avg_words} words.",
                doc_url="https://developers.google.com/search/docs/essentials/spam-policies#thin-content"
            ))
            pillar.earned_score += 5.0
        elif avg_words >= 600:
            pillar.checks.append(CheckResult(
                id="average_word_count",
                name="Article Depth & Substance (Avg Word Count)",
                status=CheckStatus.PASS,
                severity=Severity.BLOCKER,
                score=4.0,
                max_score=5.0,
                details=f"Acceptable article depth: Average article length is {avg_words} words.",
                doc_url="https://developers.google.com/search/docs/essentials/spam-policies#thin-content"
            ))
            pillar.earned_score += 4.0
        else:
            pillar.checks.append(CheckResult(
                id="average_word_count",
                name="Article Depth & Substance (Avg Word Count)",
                status=CheckStatus.FAIL,
                severity=Severity.BLOCKER,
                score=1.5,
                max_score=5.0,
                details=f"Low content substance ({avg_words} words avg). Triggers AdSense 'Thin Content / Low Value' penalty.",
                fix_recommendation="Expand articles to at least 800-1200+ words with unique insights, data, and structured explanations.",
                doc_url="https://developers.google.com/search/docs/essentials/spam-policies#thin-content"
            ))
            pillar.earned_score += 1.5
        pillar.max_score += 5.0

        # 3. Readability & Natural Flow Score (Flesch-Kincaid)
        if 45.0 <= avg_readability <= 75.0:
            pillar.checks.append(CheckResult(
                id="readability_index",
                name="Reading Flow & Natural Prose Index",
                status=CheckStatus.PASS,
                severity=Severity.HIGH,
                score=3.0,
                max_score=3.0,
                details=f"Optimal readability index ({avg_readability}/100 Flesch score) - engaging for human readers.",
                doc_url="https://developers.google.com/search/docs/fundamentals/creating-helpful-content"
            ))
            pillar.earned_score += 3.0
        else:
            pillar.checks.append(CheckResult(
                id="readability_index",
                name="Reading Flow & Natural Prose Index",
                status=CheckStatus.PASS,
                severity=Severity.MEDIUM,
                score=2.0,
                max_score=3.0,
                details=f"Readability score is {avg_readability}/100. Suitable, but could be tuned for clearer audience comprehension.",
                doc_url="https://developers.google.com/search/docs/fundamentals/creating-helpful-content"
            ))
            pillar.earned_score += 2.0
        pillar.max_score += 3.0

        # 4. AI Fluff / Templated Content Detection
        unique_cliches = list(set(ai_cliches_found))
        if len(unique_cliches) == 0:
            pillar.checks.append(CheckResult(
                id="ai_filler_detection",
                name="Human Authenticity & Low AI Boilerplate",
                status=CheckStatus.PASS,
                severity=Severity.HIGH,
                score=4.0,
                max_score=4.0,
                details="Clean natural prose detected. No repetitive automated AI generation cliches flagged.",
                doc_url="https://developers.google.com/search/blog/2023/02/google-search-and-ai-content"
            ))
            pillar.earned_score += 4.0
        elif len(unique_cliches) <= 2:
            pillar.checks.append(CheckResult(
                id="ai_filler_detection",
                name="Human Authenticity & Low AI Boilerplate",
                status=CheckStatus.WARNING,
                severity=Severity.HIGH,
                score=2.5,
                max_score=4.0,
                details=f"Minor AI-sounding phrasing found ({len(unique_cliches)} common patterns like '{unique_cliches[0]}').",
                fix_recommendation="Refactor robotic transitions and replace with personal commentary, real examples, or first-hand perspective.",
                doc_url="https://developers.google.com/search/blog/2023/02/google-search-and-ai-content"
            ))
            pillar.earned_score += 2.5
        else:
            pillar.checks.append(CheckResult(
                id="ai_filler_detection",
                name="Human Authenticity & Low AI Boilerplate",
                status=CheckStatus.FAIL,
                severity=Severity.BLOCKER,
                score=1.0,
                max_score=4.0,
                details=f"Heavy AI boilerplate markers detected across articles ({len(unique_cliches)} patterns found). High risk of unoriginal content flag.",
                fix_recommendation="Heavily edit AI content to include original opinions, case studies, personal voice, and specialized insights.",
                doc_url="https://developers.google.com/search/blog/2023/02/google-search-and-ai-content"
            ))
            pillar.earned_score += 1.0
        pillar.max_score += 4.0

        # 5. Heading Hierarchy
        if headings_ok >= max(1, int(len(article_pages) * 0.7)):
            pillar.checks.append(CheckResult(
                id="heading_hierarchy",
                name="Semantic Heading Structure (H1, H2, H3)",
                status=CheckStatus.PASS,
                severity=Severity.MEDIUM,
                score=3.0,
                max_score=3.0,
                details="Articles properly formatted with structured H1 and H2 subheadings.",
                doc_url="https://developers.google.com/search/docs/appearance/title-link"
            ))
            pillar.earned_score += 3.0
        else:
            pillar.checks.append(CheckResult(
                id="heading_hierarchy",
                name="Semantic Heading Structure (H1, H2, H3)",
                status=CheckStatus.WARNING,
                severity=Severity.MEDIUM,
                score=1.5,
                max_score=3.0,
                details="Several articles lack proper H1/H2 heading hierarchy.",
                fix_recommendation="Break down long text walls using H2 and H3 subheadings for better readability.",
                doc_url="https://developers.google.com/search/docs/appearance/title-link"
            ))
            pillar.earned_score += 1.5
        pillar.max_score += 3.0

        # 6. Author Attribution / Bylines (E-E-A-T)
        if authors_found >= max(1, int(len(article_pages) * 0.6)):
            pillar.checks.append(CheckResult(
                id="author_byline",
                name="Author Attribution & E-E-A-T Byline",
                status=CheckStatus.PASS,
                severity=Severity.HIGH,
                score=2.0,
                max_score=2.0,
                details="Articles feature clear author attribution and editorial credit.",
                doc_url="https://developers.google.com/search/docs/fundamentals/creating-helpful-content"
            ))
            pillar.earned_score += 2.0
        else:
            pillar.checks.append(CheckResult(
                id="author_byline",
                name="Author Attribution & E-E-A-T Byline",
                status=CheckStatus.WARNING,
                severity=Severity.HIGH,
                score=0.5,
                max_score=2.0,
                details="Missing clear author bylines or bios on multiple articles.",
                fix_recommendation="Add an author byline box with author name, short bio, and profile avatar to all posts.",
                doc_url="https://developers.google.com/search/docs/fundamentals/creating-helpful-content"
            ))
            pillar.earned_score += 0.5
        pillar.max_score += 2.0

        # 7. Visual Media with Alt Tags
        alt_ratio = (images_with_alt / total_images) if total_images > 0 else 1.0
        if alt_ratio >= 0.7:
            pillar.checks.append(CheckResult(
                id="media_and_alt_attributes",
                name="Visual Media & Descriptive Alt Text",
                status=CheckStatus.PASS,
                severity=Severity.MEDIUM,
                score=2.0,
                max_score=2.0,
                details=f"Visual media present with good alt text coverage ({int(alt_ratio * 100)}%).",
                doc_url="https://developers.google.com/search/docs/appearance/google-images"
            ))
            pillar.earned_score += 2.0
        else:
            pillar.checks.append(CheckResult(
                id="media_and_alt_attributes",
                name="Visual Media & Descriptive Alt Text",
                status=CheckStatus.WARNING,
                severity=Severity.MEDIUM,
                score=1.0,
                max_score=2.0,
                details=f"Some images are missing descriptive alt tags ({images_with_alt}/{total_images} tagged).",
                fix_recommendation="Add descriptive alt attributes to all embedded images.",
                doc_url="https://developers.google.com/search/docs/appearance/google-images"
            ))
            pillar.earned_score += 1.0
        pillar.max_score += 2.0

        return pillar
