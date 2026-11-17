"""
Pillar 1: Mandatory Legal & Trust Foundation Checker
"""

import re
from urllib.parse import urljoin
from typing import List, Dict, Any
from ..models import PillarResult, CheckResult, CheckStatus, Severity


class LegalTrustChecker:
    def __init__(self, rules: Dict[str, Any]):
        self.rules = rules.get("pillars", {}).get("legal_trust", {})
        self.weight = self.rules.get("weight", 20)

    def run(self, base_url: str, homepage_html: str, crawled_pages: Dict[str, str]) -> PillarResult:
        pillar = PillarResult(
            id="legal_trust",
            name="Mandatory Legal & Trust Foundation",
            weight=self.weight,
            earned_score=0.0,
            max_score=0.0,
            checks=[]
        )

        all_html_text = " ".join(crawled_pages.values()).lower()
        homepage_lower = homepage_html.lower()

        # 1. Privacy Policy Check
        privacy_found = any(k in homepage_lower for k in ["privacy policy", "privacy", "politica de privacidad", "datenschutz"])
        privacy_content = ""
        for url, content in crawled_pages.items():
            if "privacy" in url.lower():
                privacy_content = content.lower()
                privacy_found = True
                break

        if privacy_found:
            pillar.checks.append(CheckResult(
                id="privacy_policy",
                name="Privacy Policy Page Detected",
                status=CheckStatus.PASS,
                severity=Severity.BLOCKER,
                score=5.0,
                max_score=5.0,
                details="Privacy policy link/page is present on the site.",
                doc_url="https://support.google.com/adsense/answer/10502938"
            ))
            pillar.earned_score += 5.0

            # 1.1 AdSense & Cookie Opt-Out Clause Check
            adsense_clauses = ["google", "adsense", "cookie", "dart cookie", "opt-out", "personalized advertising", "third-party vendors"]
            matches = [term for term in adsense_clauses if term in privacy_content or term in all_html_text]
            if len(matches) >= 3:
                pillar.checks.append(CheckResult(
                    id="google_cookie_disclosure",
                    name="Google AdSense & Cookie Opt-Out Clause",
                    status=CheckStatus.PASS,
                    severity=Severity.BLOCKER,
                    score=4.0,
                    max_score=4.0,
                    details=f"Required AdSense cookie clauses detected (matched: {', '.join(matches[:4])}).",
                    doc_url="https://support.google.com/adsense/answer/48182"
                ))
                pillar.earned_score += 4.0
            else:
                pillar.checks.append(CheckResult(
                    id="google_cookie_disclosure",
                    name="Google AdSense & Cookie Opt-Out Clause",
                    status=CheckStatus.FAIL,
                    severity=Severity.BLOCKER,
                    score=1.0,
                    max_score=4.0,
                    details="Privacy Policy does NOT explicitly disclose Google third-party cookies or provide opt-out instructions (aboutads.info).",
                    fix_recommendation="Add explicit AdSense cookie disclosure clause mentioning Google, third-party advertising cookies, and an opt-out link.",
                    doc_url="https://support.google.com/adsense/answer/48182"
                ))
                pillar.earned_score += 1.0
        else:
            pillar.checks.append(CheckResult(
                id="privacy_policy",
                name="Privacy Policy Page Detected",
                status=CheckStatus.FAIL,
                severity=Severity.BLOCKER,
                score=0.0,
                max_score=5.0,
                details="No Privacy Policy page or footer link could be detected.",
                fix_recommendation="Create a standalone /privacy-policy page and link it prominently in your footer navigation.",
                doc_url="https://support.google.com/adsense/answer/10502938"
            ))
            pillar.checks.append(CheckResult(
                id="google_cookie_disclosure",
                name="Google AdSense & Cookie Opt-Out Clause",
                status=CheckStatus.FAIL,
                severity=Severity.BLOCKER,
                score=0.0,
                max_score=4.0,
                details="Cannot verify AdSense cookie disclosure because Privacy Policy is missing.",
                fix_recommendation="Draft a compliant Privacy Policy with Google AdSense and DoubleClick cookie opt-out clauses.",
                doc_url="https://support.google.com/adsense/answer/48182"
            ))

        pillar.max_score += 9.0

        # 2. Terms of Service
        terms_found = any(k in homepage_lower for k in ["terms of service", "terms and conditions", "terms of use", "terms"])
        if terms_found:
            pillar.checks.append(CheckResult(
                id="terms_of_service",
                name="Terms of Service / Conditions",
                status=CheckStatus.PASS,
                severity=Severity.HIGH,
                score=3.0,
                max_score=3.0,
                details="Terms of Service/Conditions page detected.",
                doc_url="https://support.google.com/adsense/answer/48182"
            ))
            pillar.earned_score += 3.0
        else:
            pillar.checks.append(CheckResult(
                id="terms_of_service",
                name="Terms of Service / Conditions",
                status=CheckStatus.WARNING,
                severity=Severity.HIGH,
                score=0.0,
                max_score=3.0,
                details="No clear Terms of Service link found in navigation.",
                fix_recommendation="Add a clear Terms of Service page establishing rules and limitations of liability.",
                doc_url="https://support.google.com/adsense/answer/48182"
            ))
        pillar.max_score += 3.0

        # 3. About Us with E-E-A-T Human Credibility
        about_found = any(k in homepage_lower for k in ["about us", "about me", "who we are", "about the author"])
        about_content = ""
        for url, content in crawled_pages.items():
            if "about" in url.lower():
                about_content = content.lower()
                about_found = True
                break

        has_placeholder = "lorem ipsum" in about_content or "replace with your text" in about_content
        if about_found and not has_placeholder:
            pillar.checks.append(CheckResult(
                id="about_us_transparency",
                name="Genuine About Us / Author Credibility Page",
                status=CheckStatus.PASS,
                severity=Severity.HIGH,
                score=4.0,
                max_score=4.0,
                details="About Us page present with legitimate editorial / creator background.",
                doc_url="https://developers.google.com/search/docs/fundamentals/creating-helpful-content"
            ))
            pillar.earned_score += 4.0
        elif has_placeholder:
            pillar.checks.append(CheckResult(
                id="about_us_transparency",
                name="Genuine About Us / Author Credibility Page",
                status=CheckStatus.FAIL,
                severity=Severity.BLOCKER,
                score=0.0,
                max_score=4.0,
                details="About page contains placeholder template text ('Lorem Ipsum').",
                fix_recommendation="Replace dummy placeholder text on About page with genuine author bio, editorial standards, and credentials.",
                doc_url="https://developers.google.com/search/docs/fundamentals/creating-helpful-content"
            ))
        else:
            pillar.checks.append(CheckResult(
                id="about_us_transparency",
                name="Genuine About Us / Author Credibility Page",
                status=CheckStatus.FAIL,
                severity=Severity.HIGH,
                score=0.0,
                max_score=4.0,
                details="No About Us / Creator information page detected.",
                fix_recommendation="Publish an in-depth About Us page highlighting author expertise, editorial mission, and experience.",
                doc_url="https://developers.google.com/search/docs/fundamentals/creating-helpful-content"
            ))
        pillar.max_score += 4.0

        # 4. Contact Us
        contact_found = any(k in homepage_lower for k in ["contact us", "contact me", "get in touch"])
        contact_content = ""
        for url, content in crawled_pages.items():
            if "contact" in url.lower():
                contact_content = content.lower()
                contact_found = True
                break

        has_email_or_form = (
            "mailto:" in contact_content or
            "@" in contact_content or
            "<form" in contact_content or
            "contact-form" in contact_content or
            "mailto:" in homepage_lower
        )

        if contact_found and has_email_or_form:
            pillar.checks.append(CheckResult(
                id="contact_us_reachability",
                name="Direct Contact Reachability (Email/Form)",
                status=CheckStatus.PASS,
                severity=Severity.BLOCKER,
                score=3.0,
                max_score=3.0,
                details="Contact page found with working email or submission form.",
                doc_url="https://support.google.com/adsense/answer/10502938"
            ))
            pillar.earned_score += 3.0
        elif contact_found and not has_email_or_form:
            pillar.checks.append(CheckResult(
                id="contact_us_reachability",
                name="Direct Contact Reachability (Email/Form)",
                status=CheckStatus.WARNING,
                severity=Severity.HIGH,
                score=1.5,
                max_score=3.0,
                details="Contact page found but lacks an explicit email address or functional form.",
                fix_recommendation="Add an active contact email (e.g. contact@yourdomain.com) or a working contact form.",
                doc_url="https://support.google.com/adsense/answer/10502938"
            ))
            pillar.earned_score += 1.5
        else:
            pillar.checks.append(CheckResult(
                id="contact_us_reachability",
                name="Direct Contact Reachability (Email/Form)",
                status=CheckStatus.FAIL,
                severity=Severity.BLOCKER,
                score=0.0,
                max_score=3.0,
                details="No Contact Us page or direct email found.",
                fix_recommendation="Add a Contact Us page with direct email reachability in header/footer.",
                doc_url="https://support.google.com/adsense/answer/10502938"
            ))
        pillar.max_score += 3.0

        # 5. Disclaimer
        disclaimer_found = any(k in homepage_lower for k in ["disclaimer", "affiliate disclosure"])
        if disclaimer_found:
            pillar.checks.append(CheckResult(
                id="disclaimer_page",
                name="Disclaimer / Disclosure Notice",
                status=CheckStatus.PASS,
                severity=Severity.LOW,
                score=1.0,
                max_score=1.0,
                details="Legal disclaimer/disclosure page found.",
                doc_url="https://support.google.com/adsense/answer/48182"
            ))
            pillar.earned_score += 1.0
        else:
            pillar.checks.append(CheckResult(
                id="disclaimer_page",
                name="Disclaimer / Disclosure Notice",
                status=CheckStatus.WARNING,
                severity=Severity.LOW,
                score=0.5,
                max_score=1.0,
                details="No explicit Disclaimer page found (recommended for monetized/affiliate sites).",
                fix_recommendation="Consider adding a general disclaimer page to protect against legal ambiguity.",
                doc_url="https://support.google.com/adsense/answer/48182"
            ))
            pillar.earned_score += 0.5
        pillar.max_score += 1.0

        return pillar
