"""
Pillar 5: Google Publisher Policies & Prohibited Niches Checker
"""

import re
from typing import Dict, Any, List
from ..models import PillarResult, CheckResult, CheckStatus, Severity


class PolicyProhibitedChecker:
    def __init__(self, rules: Dict[str, Any]):
        self.rules = rules.get("pillars", {}).get("google_publisher_policy", {})
        self.weight = self.rules.get("weight", 15)

    def run(self, homepage_html: str, crawled_pages: Dict[str, str]) -> PillarResult:
        pillar = PillarResult(
            id="google_publisher_policy",
            name="Google Publisher Policies & Prohibited Niches",
            weight=self.weight,
            earned_score=0.0,
            max_score=0.0,
            checks=[]
        )

        all_text = (homepage_html + " " + " ".join(crawled_pages.values())).lower()

        # 1. Banned Niches / Illegal Content
        prohibited_terms = [
            "keygen", "warez", "torrent download", "crack download", "mod apk unlimited",
            "casino online", "sports betting odds", "porn", "adult video", "escort service",
            "buy weapons", "counterfeit goods", "hack account", "bypass paywall",
            "free movie streaming full hd", "cracked software", "pirate bay"
        ]

        found_prohibited = [t for t in prohibited_terms if re.search(rf"\b{re.escape(t)}\b", all_text)]

        if not found_prohibited:
            pillar.checks.append(CheckResult(
                id="banned_niche_detection",
                name="Google Prohibited Content Compliance",
                status=CheckStatus.PASS,
                severity=Severity.BLOCKER,
                score=6.0,
                max_score=6.0,
                details="No prohibited niche keywords, pirated links, or policy-violating topics identified.",
                doc_url="https://support.google.com/adsense/answer/10502938"
            ))
            pillar.earned_score += 6.0
        else:
            pillar.checks.append(CheckResult(
                id="banned_niche_detection",
                name="Google Prohibited Content Compliance",
                status=CheckStatus.FAIL,
                severity=Severity.BLOCKER,
                score=0.0,
                max_score=6.0,
                details=f"CRITICAL VIOLATION: Found Google prohibited content signals: {', '.join(found_prohibited)}.",
                fix_recommendation="Completely purge all references, downloads, or discussions of illegal, pirated, adult, or hacking material immediately.",
                doc_url="https://support.google.com/adsense/answer/10502938"
            ))
        pillar.max_score += 6.0

        # 2. Deceptive UI Buttons (Fake download buttons)
        deceptive_patterns = [
            r'<a[^>]+>(?:direct\s+)?download\s+now</a>',
            r'<a[^>]+>play\s+now\s+free</a>',
            r'<button[^>]+>download\s+here</button>',
            r'class=["\'][^"\']*fake-button[^"\']*["\']'
        ]
        found_deceptive = []
        for pattern in deceptive_patterns:
            matches = re.findall(pattern, all_text)
            if matches:
                found_deceptive.extend(matches)

        if not found_deceptive:
            pillar.checks.append(CheckResult(
                id="deceptive_ui_buttons",
                name="Absence of Deceptive 'Download' Triggers",
                status=CheckStatus.PASS,
                severity=Severity.BLOCKER,
                score=5.0,
                max_score=5.0,
                details="No deceptive download triggers or trick-to-click UI designs detected.",
                doc_url="https://support.google.com/adsense/answer/1346295"
            ))
            pillar.earned_score += 5.0
        else:
            pillar.checks.append(CheckResult(
                id="deceptive_ui_buttons",
                name="Absence of Deceptive 'Download' Triggers",
                status=CheckStatus.FAIL,
                severity=Severity.BLOCKER,
                score=1.0,
                max_score=5.0,
                details=f"Identified misleading call-to-action designs that risk being classified as invalid click tricks.",
                fix_recommendation="Ensure all download/play buttons clearly indicate their true action and are separated from future ad placements.",
                doc_url="https://support.google.com/adsense/answer/1346295"
            ))
            pillar.earned_score += 1.0
        pillar.max_score += 5.0

        # 3. Copyright / Piracy Safety
        piracy_flags = ["dmca takedown", "we do not host files on our server", "all links are from third party", "magnet:?xt="]
        found_piracy_disclaimers = [f for f in piracy_flags if f in all_text]

        if not found_piracy_disclaimers:
            pillar.checks.append(CheckResult(
                id="copyright_safe_check",
                name="Copyright & Intellectual Property Safety",
                status=CheckStatus.PASS,
                severity=Severity.BLOCKER,
                score=4.0,
                max_score=4.0,
                details="Clean intellectual property profile. No pirated streaming disclaimers or torrent links detected.",
                doc_url="https://support.google.com/adsense/answer/10502938"
            ))
            pillar.earned_score += 4.0
        else:
            pillar.checks.append(CheckResult(
                id="copyright_safe_check",
                name="Copyright & Intellectual Property Safety",
                status=CheckStatus.FAIL,
                severity=Severity.BLOCKER,
                score=0.0,
                max_score=4.0,
                details="Detected evasive copyright disclaimers (e.g. 'we do not host files'), which Google explicitly flags as pirated content syndication.",
                fix_recommendation="Remove third-party copyrighted embeds or streaming links.",
                doc_url="https://support.google.com/adsense/answer/10502938"
            ))
        pillar.max_score += 4.0

        return pillar
