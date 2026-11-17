"""
Data models for AdSenseReady-AI audit results.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


class Severity(str, Enum):
    BLOCKER = "BLOCKER"     # Instant rejection by Google AdSense
    HIGH = "HIGH"           # Substantial penalty; very likely rejection
    MEDIUM = "MEDIUM"       # Moderate negative signal
    LOW = "LOW"             # Best practice / optimization


class CheckStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"


@dataclass
class CheckResult:
    id: str
    name: str
    status: CheckStatus
    severity: Severity
    score: float
    max_score: float
    details: str
    fix_recommendation: str = ""
    doc_url: str = "https://support.google.com/adsense"


@dataclass
class PillarResult:
    id: str
    name: str
    weight: float
    earned_score: float
    max_score: float
    checks: List[CheckResult] = field(default_factory=list)

    @property
    def percentage(self) -> float:
        if self.max_score <= 0:
            return 100.0
        return round((self.earned_score / self.max_score) * 100, 1)

    @property
    def blockers(self) -> List[CheckResult]:
        return [c for c in self.checks if c.status == CheckStatus.FAIL and c.severity == Severity.BLOCKER]

    @property
    def warnings(self) -> List[CheckResult]:
        return [c for c in self.checks if c.status == CheckStatus.WARNING or (c.status == CheckStatus.FAIL and c.severity != Severity.BLOCKER)]


@dataclass
class AuditReport:
    target_url: str
    timestamp: str
    policy_version: str
    total_score: float
    max_possible: float
    verdict: str  # "APPROVED_READY" | "AT_RISK" | "REJECTION_GUARANTEED"
    summary_verdict: str
    pillars: Dict[str, PillarResult] = field(default_factory=dict)
    all_blockers: List[CheckResult] = field(default_factory=list)
    action_plan: List[str] = field(default_factory=list)
    cms_info: Optional[Dict[str, Any]] = None

    @property
    def normalized_score(self) -> float:
        if self.max_possible <= 0:
            return 0.0
        return round((self.total_score / self.max_possible) * 100, 1)
