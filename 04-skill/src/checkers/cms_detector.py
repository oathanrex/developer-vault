"""
CMS & Tech Stack Detector for Tailored AdSense Recommendations
"""

import re
from typing import Dict, Any, Optional


class CMSDetector:
    """Detects CMS platform and returns customized AdSense setup recommendations."""

    SIGNATURES = {
        "WordPress": [
            r"/wp-content/",
            r"/wp-includes/",
            r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']WordPress',
            r"wp-json"
        ],
        "Ghost": [
            r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']Ghost',
            r"ghost-portal",
            r"/assets/built/screen\.css"
        ],
        "Shopify": [
            r"cdn\.shopify\.com",
            r"Shopify\.theme",
            r"shopify-section"
        ],
        "Blogger / Blogspot": [
            r"blogger\.com",
            r"blogspot\.com",
            r'<meta[^>]+content=["\']blogger["\']'
        ],
        "Webflow": [
            r"uploads-ssl\.webflow\.com",
            r'<html[^>]+data-wf-page',
            r'<meta[^>]+content=["\']Webflow["\']'
        ],
        "Next.js": [
            r"/_next/static/",
            r'<script[^>]+id=["\']__NEXT_DATA__["\']',
            r'<div[^>]+id=["\']__next["\']'
        ],
        "Nuxt.js": [
            r"/_nuxt/",
            r'<div[^>]+id=["\']__nuxt["\']'
        ],
        "Hugo": [
            r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']Hugo'
        ],
        "Jekyll": [
            r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']Jekyll'
        ]
    }

    RECOMMENDATIONS = {
        "WordPress": [
            "Install 'Site Kit by Google' for 1-click official AdSense verification tag injection.",
            "Use 'WP AutoTerms' or 'Complianz' to ensure GDPR/CCPA cookie consent CMP compliance.",
            "Remove default 'Hello World!' post and 'Sample Page' in WordPress dashboard under Posts/Pages.",
            "Set your Privacy Policy page explicitly in Settings -> Privacy."
        ],
        "Ghost": [
            "Inject Google AdSense verification code via Settings -> Code Injection -> Site Header.",
            "Add custom navigation links to Privacy, Terms, and Contact in Settings -> Navigation.",
            "Use Ghost Members & Portal to reinforce human E-E-A-T credentials."
        ],
        "Next.js": [
            "Load Google AdSense script using `next/script` with `strategy='afterInteractive'` to avoid CLS.",
            "Implement next-sitemap to generate clean static `sitemap.xml` and `robots.txt`.",
            "Ensure dynamic pages generate static `<head>` meta tags via Next.js Metadata API."
        ],
        "Webflow": [
            "Add Google AdSense publisher tag into Project Settings -> Custom Code -> Head Code.",
            "Ensure all collection list dynamic templates have unique meta titles and descriptions.",
            "Connect custom domain and enforce HTTPS in Hosting settings."
        ],
        "Blogger / Blogspot": [
            "Link your Google AdSense account directly from Blogger Dashboard -> Earnings tab.",
            "Ensure custom domain (TLD) is mapped rather than `.blogspot.com` for faster approval.",
            "Add Static Pages for About Us, Contact Us, and Privacy Policy via Pages -> New Page."
        ]
    }

    @classmethod
    def detect(cls, html: str) -> Dict[str, Any]:
        detected_cms = "Custom / Static HTML"
        for cms, patterns in cls.SIGNATURES.items():
            for p in patterns:
                if re.search(p, html, re.IGNORECASE):
                    detected_cms = cms
                    break
            if detected_cms != "Custom / Static HTML":
                break

        recs = cls.RECOMMENDATIONS.get(detected_cms, [
            "Manually inject Google AdSense meta tag `<meta name=\"google-adsense-account\" content=\"ca-pub-XXXXX\">` in `<head>`.",
            "Ensure all static pages (Privacy, Terms, About, Contact) are clearly linked in the footer."
        ])

        return {
            "cms": detected_cms,
            "customized_tips": recs
        }
