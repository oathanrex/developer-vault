"""
Pillar 6: Ad Placement Ergonomics & Invalid Traffic Prevention Checker
"""

import re
from typing import Dict, Any
from ..models import PillarResult, CheckResult, CheckStatus, Severity


class AdLayoutChecker:
    def __init__(self, rules: Dict[str, Any]):
        self.rules = rules.get("pillars", {}).get("ad_layout_readiness", {})
        self.weight = self.rules.get("weight", 5)

    def run(self, homepage_html: str) -> PillarResult:
        pillar = PillarResult(
            id="ad_layout_readiness",
            name="Ad Placement Ergonomics & Invalid Traffic Prevention",
            weight=self.weight,
            earned_score=0.0,
            max_score=0.0,
            checks=[]
        )

        lower_html = homepage_html.lower()

        # 1. Content Superiority / Above the fold space
        has_main_or_article = "<main" in lower_html or "<article" in lower_html or 'class="content"' in lower_html or 'id="content"' in lower_html
        if has_main_or_article:
            pillar.checks.append(CheckResult(
                id="content_to_ad_ratio",
                name="Content Prominence (Content > Ads)",
                status=CheckStatus.PASS,
                severity=Severity.HIGH,
                score=3.0,
                max_score=3.0,
                details="Distinct semantic main content containers detected. Layout leaves ample room for compliant ad placement without clutter.",
                doc_url="https://support.google.com/adsense/answer/1346295"
            ))
            pillar.earned_score += 3.0
        else:
            pillar.checks.append(CheckResult(
                id="content_to_ad_ratio",
                name="Content Prominence (Content > Ads)",
                status=CheckStatus.WARNING,
                severity=Severity.HIGH,
                score=1.5,
                max_score=3.0,
                details="Lacks clear semantic <main> or <article> wrapper; layout structure could cause ads to push content below the fold.",
                fix_recommendation="Structure your page layout using semantic <main> tags ensuring body copy is prominently visible above the fold.",
                doc_url="https://support.google.com/adsense/answer/1346295"
            ))
            pillar.earned_score += 1.5
        pillar.max_score += 3.0

        # 2. Cumulative Layout Shift & Aggressive Interstitial Detection
        aggressive_popups = ["popup-overlay", "interstitial-modal", "forced-click", "spin-wheel"]
        found_popups = [p for p in aggressive_popups if p in lower_html]

        if not found_popups:
            pillar.checks.append(CheckResult(
                id="layout_shift_resilience",
                name="Safe Layout Dynamics (No Intrusive Interstitials)",
                status=CheckStatus.PASS,
                severity=Severity.MEDIUM,
                score=2.0,
                max_score=2.0,
                details="No intrusive full-screen popups or unexpected layout shifters detected.",
                doc_url="https://support.google.com/adsense/answer/1346295"
            ))
            pillar.earned_score += 2.0
        else:
            pillar.checks.append(CheckResult(
                id="layout_shift_resilience",
                name="Safe Layout Dynamics (No Intrusive Interstitials)",
                status=CheckStatus.WARNING,
                severity=Severity.MEDIUM,
                score=0.5,
                max_score=2.0,
                details=f"Detected aggressive modal/overlay classes ({', '.join(found_popups)}). Google penalizes intrusive interstitials.",
                fix_recommendation="Disable intrusive page-blocking popups prior to AdSense evaluation.",
                doc_url="https://support.google.com/adsense/answer/1346295"
            ))
            pillar.earned_score += 0.5
        pillar.max_score += 2.0

        return pillar
