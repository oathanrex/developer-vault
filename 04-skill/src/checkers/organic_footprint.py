"""
Pillar 7: Organic Search Footprint & Domain Maturity Checker
"""

import re
from typing import Dict, Any
from ..models import PillarResult, CheckResult, CheckStatus, Severity


class OrganicFootprintChecker:
    def __init__(self, rules: Dict[str, Any]):
        self.rules = rules.get("pillars", {}).get("organic_footprint", {})
        self.weight = self.rules.get("weight", 5)

    def run(self, homepage_html: str) -> PillarResult:
        pillar = PillarResult(
            id="organic_footprint",
            name="Organic Search Footprint & Domain Maturity",
            weight=self.weight,
            earned_score=0.0,
            max_score=0.0,
            checks=[]
        )

        lower_html = homepage_html.lower()

        # 1. Canonical Tag & Search Indexability
        has_canonical = bool(re.search(r'<link[^>]+rel=["\']canonical["\']', lower_html))
        is_noindex = bool(re.search(r'<meta[^>]+content=["\'][^"\']*noindex[^"\']*["\']', lower_html))

        if is_noindex:
            pillar.checks.append(CheckResult(
                id="search_console_indexing_signals",
                name="Search Indexing & Canonical Directives",
                status=CheckStatus.FAIL,
                severity=Severity.BLOCKER,
                score=0.0,
                max_score=3.0,
                details="CRITICAL BLOCKER: Site contains 'noindex' meta tag. Google cannot index or evaluate the website.",
                fix_recommendation="Remove 'noindex' directive from meta tags or CMS SEO settings.",
                doc_url="https://developers.google.com/search/docs/crawling-indexing/block-indexing"
            ))
        elif has_canonical:
            pillar.checks.append(CheckResult(
                id="search_console_indexing_signals",
                name="Search Indexing & Canonical Directives",
                status=CheckStatus.PASS,
                severity=Severity.HIGH,
                score=3.0,
                max_score=3.0,
                details="Canonical URLs specified and indexation permitted.",
                doc_url="https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls"
            ))
            pillar.earned_score += 3.0
        else:
            pillar.checks.append(CheckResult(
                id="search_console_indexing_signals",
                name="Search Indexing & Canonical Directives",
                status=CheckStatus.WARNING,
                severity=Severity.MEDIUM,
                score=1.5,
                max_score=3.0,
                details="No canonical link tag found. Indexable, but duplicate content risk exists.",
                fix_recommendation="Add self-referencing <link rel='canonical' href='...'> to all pages.",
                doc_url="https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls"
            ))
            pillar.earned_score += 1.5
        pillar.max_score += 3.0

        # 2. Schema.org / Structured Data
        has_schema = "application/ld+json" in lower_html or "itemscope" in lower_html
        if has_schema:
            pillar.checks.append(CheckResult(
                id="structured_data_breadcrumbs",
                name="Schema.org Structured Data & Rich Snippets",
                status=CheckStatus.PASS,
                severity=Severity.MEDIUM,
                score=2.0,
                max_score=2.0,
                details="Schema.org structured data (JSON-LD or microdata) detected.",
                doc_url="https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data"
            ))
            pillar.earned_score += 2.0
        else:
            pillar.checks.append(CheckResult(
                id="structured_data_breadcrumbs",
                name="Schema.org Structured Data & Rich Snippets",
                status=CheckStatus.WARNING,
                severity=Severity.LOW,
                score=1.0,
                max_score=2.0,
                details="No Schema.org JSON-LD found (strongly recommended for modern E-E-A-T entity recognition).",
                fix_recommendation="Implement JSON-LD Schema (WebSite, Organization, Article, BreadcrumbList).",
                doc_url="https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data"
            ))
            pillar.earned_score += 1.0
        pillar.max_score += 2.0

        return pillar
