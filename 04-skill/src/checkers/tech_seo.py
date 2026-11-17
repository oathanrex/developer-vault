"""
Pillar 3: Technical Crawlability & Web Health Checker
"""

import re
from typing import Dict, Any, Optional
from ..models import PillarResult, CheckResult, CheckStatus, Severity


class TechSEOChecker:
    def __init__(self, rules: Dict[str, Any]):
        self.rules = rules.get("pillars", {}).get("technical_seo", {})
        self.weight = self.rules.get("weight", 15)

    def run(
        self,
        base_url: str,
        homepage_html: str,
        robots_txt: Optional[str],
        sitemap_found: bool,
        sitemap_url: str,
        latency_seconds: float
    ) -> PillarResult:
        pillar = PillarResult(
            id="technical_seo",
            name="Technical Crawlability & Web Health",
            weight=self.weight,
            earned_score=0.0,
            max_score=0.0,
            checks=[]
        )

        # 1. HTTPS / SSL Enforcement
        is_https = base_url.lower().startswith("https://")
        if is_https:
            pillar.checks.append(CheckResult(
                id="ssl_https_enforcement",
                name="HTTPS / SSL Encryption",
                status=CheckStatus.PASS,
                severity=Severity.BLOCKER,
                score=4.0,
                max_score=4.0,
                details="Site is served over secure HTTPS protocol.",
                doc_url="https://developers.google.com/search/docs/crawling-indexing/https"
            ))
            pillar.earned_score += 4.0
        else:
            pillar.checks.append(CheckResult(
                id="ssl_https_enforcement",
                name="HTTPS / SSL Encryption",
                status=CheckStatus.FAIL,
                severity=Severity.BLOCKER,
                score=0.0,
                max_score=4.0,
                details="Site is not enforcing HTTPS. AdSense requires SSL across all monetized domains.",
                fix_recommendation="Install an SSL certificate (e.g. Let's Encrypt or Cloudflare) and enforce HTTPS redirect.",
                doc_url="https://developers.google.com/search/docs/crawling-indexing/https"
            ))
        pillar.max_score += 4.0

        # 2. Robots.txt crawlability
        if robots_txt is not None:
            robots_lower = robots_txt.lower()
            blocks_mediapartners = "user-agent: mediapartners-google\ndisallow: /" in robots_lower or "user-agent: mediapartners-google\r\ndisallow: /" in robots_lower
            blocks_all = "user-agent: *\ndisallow: /" in robots_lower or "user-agent: *\r\ndisallow: /" in robots_lower

            if blocks_mediapartners:
                pillar.checks.append(CheckResult(
                    id="robots_txt_accessibility",
                    name="Robots.txt AdSense Crawler Access",
                    status=CheckStatus.FAIL,
                    severity=Severity.BLOCKER,
                    score=0.0,
                    max_score=4.0,
                    details="CRITICAL BLOCKER: Robots.txt explicitly disallows 'Mediapartners-Google' crawler.",
                    fix_recommendation="Remove disallow rule for User-agent: Mediapartners-Google in robots.txt immediately.",
                    doc_url="https://support.google.com/adsense/answer/10532"
                ))
            elif blocks_all:
                pillar.checks.append(CheckResult(
                    id="robots_txt_accessibility",
                    name="Robots.txt AdSense Crawler Access",
                    status=CheckStatus.FAIL,
                    severity=Severity.BLOCKER,
                    score=0.5,
                    max_score=4.0,
                    details="Robots.txt disallows all crawlers ('User-agent: * Disallow: /').",
                    fix_recommendation="Update robots.txt to allow Googlebot and Mediapartners-Google to crawl public content.",
                    doc_url="https://support.google.com/adsense/answer/10532"
                ))
                pillar.earned_score += 0.5
            else:
                pillar.checks.append(CheckResult(
                    id="robots_txt_accessibility",
                    name="Robots.txt AdSense Crawler Access",
                    status=CheckStatus.PASS,
                    severity=Severity.BLOCKER,
                    score=4.0,
                    max_score=4.0,
                    details="Robots.txt allows Googlebot and Mediapartners-Google.",
                    doc_url="https://support.google.com/adsense/answer/10532"
                ))
                pillar.earned_score += 4.0
        else:
            pillar.checks.append(CheckResult(
                id="robots_txt_accessibility",
                name="Robots.txt AdSense Crawler Access",
                status=CheckStatus.WARNING,
                severity=Severity.MEDIUM,
                score=2.5,
                max_score=4.0,
                details="No robots.txt detected (defaults to allow-all, but explicit robots.txt is recommended).",
                fix_recommendation="Create a clean /robots.txt declaring sitemap and permitting Mediapartners-Google.",
                doc_url="https://support.google.com/adsense/answer/10532"
            ))
            pillar.earned_score += 2.5
        pillar.max_score += 4.0

        # 3. XML Sitemap Detected
        if sitemap_found:
            pillar.checks.append(CheckResult(
                id="sitemap_xml_detected",
                name="XML Sitemap Detection",
                status=CheckStatus.PASS,
                severity=Severity.HIGH,
                score=4.0,
                max_score=4.0,
                details=f"Valid XML sitemap detected at {sitemap_url}.",
                doc_url="https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview"
            ))
            pillar.earned_score += 4.0
        else:
            pillar.checks.append(CheckResult(
                id="sitemap_xml_detected",
                name="XML Sitemap Detection",
                status=CheckStatus.FAIL,
                severity=Severity.HIGH,
                score=0.0,
                max_score=4.0,
                details="No XML sitemap found at /sitemap.xml or referenced in robots.txt.",
                fix_recommendation="Generate and submit an XML sitemap (e.g. sitemap.xml) and add 'Sitemap: https://yourdomain.com/sitemap.xml' to robots.txt.",
                doc_url="https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview"
            ))
        pillar.max_score += 4.0

        # 4. Mobile Responsive Viewport
        has_viewport = bool(re.search(r'<meta[^>]+name=["\']viewport["\'][^>]+content=["\'][^"\']*width=device-width', homepage_html, re.IGNORECASE))
        if has_viewport:
            pillar.checks.append(CheckResult(
                id="mobile_responsive_viewport",
                name="Mobile-Responsive Viewport Meta",
                status=CheckStatus.PASS,
                severity=Severity.HIGH,
                score=3.0,
                max_score=3.0,
                details="Responsive viewport meta tag configured correctly.",
                doc_url="https://developers.google.com/search/docs/appearance/mobile-sites"
            ))
            pillar.earned_score += 3.0
        else:
            pillar.checks.append(CheckResult(
                id="mobile_responsive_viewport",
                name="Mobile-Responsive Viewport Meta",
                status=CheckStatus.FAIL,
                severity=Severity.HIGH,
                score=0.0,
                max_score=3.0,
                details="Missing responsive viewport meta tag (<meta name='viewport' content='width=device-width, initial-scale=1.0'>).",
                fix_recommendation="Add mobile viewport meta tag in the <head> of all pages.",
                doc_url="https://developers.google.com/search/docs/appearance/mobile-sites"
            ))
        pillar.max_score += 3.0

        return pillar
