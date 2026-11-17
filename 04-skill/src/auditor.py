"""
AdSenseReady-AI: Master Auditor Orchestrator
"""

import os
import re
import sys
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

from .models import AuditReport, PillarResult, CheckResult, CheckStatus, Severity
from .checkers import (
    LegalTrustChecker,
    ContentEEATChecker,
    TechSEOChecker,
    SiteStructureChecker,
    PolicyProhibitedChecker,
    AdLayoutChecker,
    OrganicFootprintChecker,
    CMSDetector
)

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_PATH = BASE_DIR / "policies" / "adsense_rules.json"


class AdSenseAuditor:
    def __init__(self, rules_path: Optional[Path] = None, user_agent: Optional[str] = None):
        self.rules_path = rules_path or RULES_PATH
        self.rules = self._load_rules()
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AdSenseReady-AI/2026.11 Crawler"
        self.session_headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }

    def _load_rules(self) -> Dict[str, Any]:
        if self.rules_path.exists():
            with open(self.rules_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"version": "2026.11.0", "pillars": {}}

    def fetch_url(self, url: str, timeout: int = 10) -> Tuple[Optional[str], float, Optional[str]]:
        """Fetches page content, measures response latency, and returns content, latency, and error."""
        start_t = time.time()
        req = urllib.request.Request(url, headers=self.session_headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw_bytes = resp.read()
                latency = round(time.time() - start_t, 2)
                # Decode
                try:
                    text = raw_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    text = raw_bytes.decode("latin-1", errors="ignore")
                return text, latency, None
        except Exception as e:
            return None, 0.0, str(e)

    def extract_links(self, base_url: str, html: str) -> List[str]:
        """Extracts internal links from HTML."""
        found = set()
        parsed_base = urllib.parse.urlparse(base_url)
        base_domain = parsed_base.netloc.lower()

        hrefs = re.findall(r'href=["\']([^"\'#\s]+)["\']', html, re.IGNORECASE)
        for href in hrefs:
            if href.startswith("javascript:") or href.startswith("mailto:") or href.startswith("tel:"):
                continue
            abs_url = urllib.parse.urljoin(base_url, href)
            parsed = urllib.parse.urlparse(abs_url)
            if parsed.netloc.lower() == base_domain and parsed.scheme in ["http", "https"]:
                # Normalize link
                clean_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
                found.add(clean_url)
        return list(found)

    def audit_site(
        self,
        target_url: str,
        max_crawl_pages: int = 15,
        mock_html: Optional[str] = None,
        mock_articles: Optional[Dict[str, str]] = None
    ) -> AuditReport:
        """Runs the complete 360-degree AdSense Readiness Audit."""
        # Ensure scheme
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = "https://" + target_url

        parsed_url = urllib.parse.urlparse(target_url)
        origin = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # 1. Fetch Homepage
        if mock_html:
            homepage_html = mock_html
            latency = 0.25
        else:
            homepage_html, latency, err = self.fetch_url(target_url)
            if not homepage_html:
                homepage_html = f"<html><head><title>Offline Analysis</title></head><body>Offline/Error: {err}</body></html>"
                latency = 5.0

        # 2. Extract Internal Links & Sitemaps
        internal_links = self.extract_links(target_url, homepage_html)

        legal_candidates = []
        article_candidates = []

        legal_keywords = ["privacy", "terms", "about", "contact", "disclaimer", "legal", "cookies"]
        for link in internal_links:
            lower_link = link.lower()
            if any(k in lower_link for k in legal_keywords):
                legal_candidates.append(link)
            else:
                if not any(ex in lower_link for ex in ["/category/", "/tag/", "/author/", "/page/", ".jpg", ".png", "/feed"]):
                    article_candidates.append(link)

        # 3. Probe Robots.txt & Sitemap
        robots_txt = None
        sitemap_found = False
        sitemap_url = ""

        if not mock_html:
            robots_content, _, _ = self.fetch_url(f"{origin}/robots.txt", timeout=6)
            if robots_content and "User-agent" in robots_content:
                robots_txt = robots_content
                sitemap_match = re.search(r"Sitemap:\s*(\S+)", robots_content, re.IGNORECASE)
                if sitemap_match:
                    sitemap_found = True
                    sitemap_url = sitemap_match.group(1)

            if not sitemap_found:
                for s_path in ["/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml"]:
                    s_content, _, _ = self.fetch_url(f"{origin}{s_path}", timeout=6)
                    if s_content and ("<urlset" in s_content or "<sitemapindex" in s_content):
                        sitemap_found = True
                        sitemap_url = f"{origin}{s_path}"
                        break
        else:
            robots_txt = "User-agent: *\nAllow: /\nUser-agent: Mediapartners-Google\nAllow: /"
            sitemap_found = True
            sitemap_url = f"{origin}/sitemap.xml"

        # 4. Crawl Sample Legal Pages & Articles
        crawled_pages = {"homepage": homepage_html}

        if not mock_html:
            for l_url in legal_candidates[:5]:
                content, _, _ = self.fetch_url(l_url, timeout=6)
                if content:
                    crawled_pages[l_url] = content

            sample_articles = {}
            for a_url in article_candidates[:6]:
                content, _, _ = self.fetch_url(a_url, timeout=6)
                if content:
                    sample_articles[a_url] = content
                    crawled_pages[a_url] = content
        else:
            if mock_articles:
                article_candidates = list(mock_articles.keys())
                sample_articles = mock_articles
            else:
                # If mock_html is provided without explicit mock_articles, synthesize candidates
                article_candidates = [f"{origin}/post-{i}" for i in range(1, 26)]
                sample_articles = {f"{origin}/post-{i}": homepage_html for i in range(1, 6)}

        # 5. Execute 7-Pillar Checkers
        p1 = LegalTrustChecker(self.rules).run(target_url, homepage_html, crawled_pages)
        p2 = ContentEEATChecker(self.rules).run(article_candidates, sample_articles)
        p3 = TechSEOChecker(self.rules).run(target_url, homepage_html, robots_txt, sitemap_found, sitemap_url, latency)
        p4 = SiteStructureChecker(self.rules).run(homepage_html, crawled_pages, internal_links)
        p5 = PolicyProhibitedChecker(self.rules).run(homepage_html, crawled_pages)
        p6 = AdLayoutChecker(self.rules).run(homepage_html)
        p7 = OrganicFootprintChecker(self.rules).run(homepage_html)

        pillars = {
            "legal_trust": p1,
            "content_eeat": p2,
            "technical_seo": p3,
            "site_navigation_ux": p4,
            "google_publisher_policy": p5,
            "ad_layout_readiness": p6,
            "organic_footprint": p7
        }

        # 6. Detect CMS Platform & Tailor Recommendations
        cms_data = CMSDetector.detect(homepage_html)

        # 7. Aggregate Composite Scores
        total_score = sum(p.earned_score for p in pillars.values())
        max_possible = sum(p.max_score for p in pillars.values())
        normalized_score = round((total_score / max_possible) * 100, 1) if max_possible > 0 else 0

        # Gather Blockers & High Severity Issues
        all_blockers = []
        action_plan = []
        for pillar in pillars.values():
            for c in pillar.checks:
                if c.status == CheckStatus.FAIL and c.severity == Severity.BLOCKER:
                    all_blockers.append(c)
                    action_plan.append(f"[CRITICAL BLOCKER] {c.name}: {c.fix_recommendation or c.details}")
                elif c.status in [CheckStatus.FAIL, CheckStatus.WARNING] and c.severity == Severity.HIGH:
                    action_plan.append(f"[HIGH PRIORITY] {c.name}: {c.fix_recommendation or c.details}")
                elif c.status == CheckStatus.WARNING:
                    action_plan.append(f"[RECOMMENDED] {c.name}: {c.fix_recommendation or c.details}")

        # Add CMS specific tips
        if cms_data.get("customized_tips"):
            for tip in cms_data["customized_tips"][:2]:
                action_plan.append(f"[{cms_data['cms']} OPTIMIZATION] {tip}")

        # Verdict Logic
        if len(all_blockers) == 0 and normalized_score >= 85.0:
            verdict = "APPROVED_READY"
            summary_verdict = "10/10 READY FOR ADSENSE APPROVAL (High Confidence)"
        elif len(all_blockers) == 0 and normalized_score >= 65.0:
            verdict = "AT_RISK"
            summary_verdict = "AT RISK - POLISH REQUIRED (Moderate Confidence)"
        else:
            verdict = "REJECTION_GUARANTEED"
            summary_verdict = f"REJECTION RISK - {len(all_blockers)} CRITICAL BLOCKER(S) DETECTED"

        return AuditReport(
            target_url=target_url,
            timestamp=datetime.utcnow().isoformat() + "Z",
            policy_version=self.rules.get("version", "2026.11.1"),
            total_score=total_score,
            max_possible=max_possible,
            verdict=verdict,
            summary_verdict=summary_verdict,
            pillars=pillars,
            all_blockers=all_blockers,
            action_plan=action_plan,
            cms_info=cms_data
        )
