"""
AdSenseReady-AI: Report Generator
Produces Rich Terminal Output, Clean Markdown Artifacts, and Structured JSON.
"""

import json
from typing import Dict, Any
from .models import AuditReport, CheckStatus, Severity

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


class AuditReporter:
    @staticmethod
    def render_terminal(report: AuditReport):
        """Displays formatted report to terminal."""
        if HAS_RICH:
            console = Console()
            
            # Header
            status_color = "green" if report.verdict == "APPROVED_READY" else ("yellow" if report.verdict == "AT_RISK" else "red")
            console.print(Panel(
                f"[bold white]{report.target_url}[/bold white]\n"
                f"Status: [{status_color} bold]{report.summary_verdict}[/{status_color} bold]\n"
                f"Overall Score: [bold cyan]{report.normalized_score} / 100[/bold cyan] (Policy Ruleset: v{report.policy_version})",
                title="[bold yellow]🎯 Google AdSense Readiness Audit Report[/bold yellow]",
                border_style=status_color
            ))

            # Pillar Breakdown Table
            table = Table(title="📊 7-Pillar Performance Matrix", header_style="bold magenta")
            table.add_column("Pillar Evaluation", style="bold")
            table.add_column("Score", justify="right")
            table.add_column("Percentage", justify="right")
            table.add_column("Status", justify="center")

            for p_id, p in report.pillars.items():
                p_color = "green" if p.percentage >= 85 else ("yellow" if p.percentage >= 65 else "red")
                icon = "✅" if p.percentage >= 85 else ("⚠️" if p.percentage >= 65 else "❌")
                table.add_row(
                    p.name,
                    f"{round(p.earned_score, 1)} / {round(p.max_score, 1)}",
                    f"[{p_color}]{p.percentage}%[/{p_color}]",
                    f"{icon}"
                )
            console.print(table)

            # Blockers
            if report.all_blockers:
                console.print("\n[bold red]🚨 Critical Blockers (Guaranteed Rejection Triggers):[/bold red]")
                for b in report.all_blockers:
                    console.print(f"  • [red bold]{b.name}[/red bold]: {b.details}")
                    if b.fix_recommendation:
                        console.print(f"    [yellow]Fix:[/yellow] {b.fix_recommendation}")

            # Top Action Items
            console.print("\n[bold cyan]📋 Priority Remediation Action Plan:[/bold cyan]")
            for i, act in enumerate(report.action_plan[:8], 1):
                console.print(f"  {i}. {act}")
            print("\n")
        else:
            # Fallback ANSI
            print("\n" + "=" * 65)
            print(f" 🎯 GOOGLE ADSENSE READINESS AUDIT: {report.target_url}")
            print("=" * 65)
            print(f" Verdict: {report.summary_verdict}")
            print(f" Overall Score: {report.normalized_score} / 100 (Policy v{report.policy_version})\n")
            print(" 7-Pillar Performance Matrix:")
            print("-" * 65)
            for p_id, p in report.pillars.items():
                icon = "PASS" if p.percentage >= 85 else ("WARN" if p.percentage >= 65 else "FAIL")
                print(f" [{icon}] {p.name:<45} {p.earned_score:>4.1f}/{p.max_score:<4.1f} ({p.percentage}%)")
            print("-" * 65)

            if report.all_blockers:
                print("\n 🚨 CRITICAL BLOCKERS:")
                for b in report.all_blockers:
                    print(f"  * {b.name}: {b.details}")
                    if b.fix_recommendation:
                        print(f"    Fix: {b.fix_recommendation}")

            print("\n 📋 PRIORITY REMEDIATION PLAN:")
            for i, act in enumerate(report.action_plan[:8], 1):
                print(f"  {i}. {act}")
            print("=" * 65 + "\n")

    @staticmethod
    def to_markdown(report: AuditReport) -> str:
        """Generates comprehensive GitHub Flavored Markdown report."""
        badge_color = "brightgreen" if report.verdict == "APPROVED_READY" else ("yellow" if report.verdict == "AT_RISK" else "red")
        verdict_icon = "✅" if report.verdict == "APPROVED_READY" else ("⚠️" if report.verdict == "AT_RISK" else "❌")

        md = []
        md.append(f"# 🎯 Google AdSense Readiness Audit Report\n")
        md.append(f"> **Target Domain:** `{report.target_url}`  ")
        md.append(f"> **Audit Date:** `{report.timestamp}` | **Policy Ruleset:** `v{report.policy_version}`  ")
        md.append(f"> **Approval Confidence Score:** **`{report.normalized_score} / 100`**\n")

        md.append(f"### Overall Verdict: {verdict_icon} **{report.summary_verdict}**\n")

        if report.verdict == "APPROVED_READY":
            md.append("> [!TIP]\n> **Congratulations!** Your site demonstrates top 1% AdSense readiness standards with zero critical blockers and high content authority.\n")
        elif report.verdict == "AT_RISK":
            md.append("> [!WARNING]\n> **Caution:** While your site is structurally sound, several policy metrics fall below the ideal safety threshold. Polish the flagged items before submission.\n")
        else:
            md.append("> [!CAUTION]\n> **Rejection Risk:** Your site currently triggers automated Google AdSense rejection flags. Resolving the Critical Blockers below is required prior to applying.\n")

        # Table
        md.append("## 📊 7-Pillar Evaluation Matrix\n")
        md.append("| Pillar | Score Earned | Max Points | Readiness % | Status |")
        md.append("| :--- | :---: | :---: | :---: | :---: |")

        for p_id, p in report.pillars.items():
            status_str = "✅ Ready" if p.percentage >= 85 else ("⚠️ Polish" if p.percentage >= 65 else "❌ High Risk")
            md.append(f"| **{p.name}** | {p.earned_score:.1f} | {p.max_score:.1f} | {p.percentage}% | {status_str} |")

        # Blockers section
        if report.all_blockers:
            md.append("\n## 🚨 Critical Blockers (Must Fix Before Submission)\n")
            for b in report.all_blockers:
                md.append(f"### ❌ {b.name}")
                md.append(f"- **Details:** {b.details}")
                if b.fix_recommendation:
                    md.append(f"- **Required Action:** {b.fix_recommendation}")
                md.append(f"- **Reference:** [{b.doc_url}]({b.doc_url})\n")

        # Priority Action Checklist
        md.append("\n## 📋 Prioritized Step-by-Step Remediation Action Plan\n")
        for i, act in enumerate(report.action_plan, 1):
            md.append(f"- [ ] **Step {i}:** {act}")

        # Detailed Checks Breakdown
        md.append("\n## 🔍 Granular Audit Breakdown\n")
        for p_id, p in report.pillars.items():
            md.append(f"### {p.name} ({p.earned_score:.1f}/{p.max_score:.1f} pts)")
            for c in p.checks:
                icon = "✅" if c.status == CheckStatus.PASS else ("⚠️" if c.status == CheckStatus.WARNING else "❌")
                md.append(f"- {icon} **{c.name}** [{c.score:.1f}/{c.max_score:.1f} pts]: {c.details}")
                if c.fix_recommendation and c.status != CheckStatus.PASS:
                    md.append(f"  - *Fix:* {c.fix_recommendation}")

        md.append("\n---\n*Report generated automatically by [AdSenseReady-AI](https://github.com/your-username/adsense-readiness-skill).*")
        return "\n".join(md)

    @staticmethod
    def to_html(report: AuditReport) -> str:
        """Generates a modern, standalone HTML Executive Dashboard Report."""
        status_color = "#10b981" if report.verdict == "APPROVED_READY" else ("#f59e0b" if report.verdict == "AT_RISK" else "#ef4444")
        score = int(report.normalized_score)
        
        # Build pillar cards
        cards_html = []
        for p_id, p in report.pillars.items():
            badge_color = "#10b981" if p.percentage >= 85 else ("#f59e0b" if p.percentage >= 65 else "#ef4444")
            checks_list = []
            for c in p.checks:
                icon = "✓" if c.status == CheckStatus.PASS else ("⚠" if c.status == CheckStatus.WARNING else "✕")
                icon_color = "#10b981" if c.status == CheckStatus.PASS else ("#f59e0b" if c.status == CheckStatus.WARNING else "#ef4444")
                rec_html = f"<div class='fix-tip'><strong>Action:</strong> {c.fix_recommendation}</div>" if c.fix_recommendation and c.status != CheckStatus.PASS else ""
                checks_list.append(f"""
                <li class="check-item">
                    <span class="check-icon" style="color: {icon_color}; font-weight: bold;">{icon}</span>
                    <div class="check-text">
                        <div class="check-name"><strong>{c.name}</strong> <span class="pts">({c.score:.1f}/{c.max_score:.1f} pts)</span></div>
                        <div class="check-desc">{c.details}</div>
                        {rec_html}
                    </div>
                </li>
                """)

            cards_html.append(f"""
            <div class="pillar-card">
                <div class="pillar-header">
                    <h3>{p.name}</h3>
                    <span class="pillar-badge" style="background: {badge_color}22; color: {badge_color}; border: 1px solid {badge_color};">
                        {p.percentage}% ({p.earned_score:.1f}/{p.max_score:.1f} pts)
                    </span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {p.percentage}%; background: {badge_color};"></div>
                </div>
                <ul class="checks-list">
                    {''.join(checks_list)}
                </ul>
            </div>
            """)

        # Blockers HTML
        blockers_html = ""
        if report.all_blockers:
            b_items = []
            for b in report.all_blockers:
                b_items.append(f"""
                <div class="blocker-box">
                    <h4>✕ {b.name}</h4>
                    <p>{b.details}</p>
                    {f'<p class="fix-box"><strong>Fix Required:</strong> {b.fix_recommendation}</p>' if b.fix_recommendation else ''}
                </div>
                """)
            blockers_html = f"""
            <section class="blockers-section">
                <h2>🚨 Critical Blockers (Instant Rejection Triggers)</h2>
                {''.join(b_items)}
            </section>
            """

        # Action Plan HTML
        action_items = []
        for i, act in enumerate(report.action_plan, 1):
            action_items.append(f"""
            <li class="action-item">
                <input type="checkbox" id="act-{i}">
                <label for="act-{i}"><strong>Step {i}:</strong> {act}</label>
            </li>
            """)

        cms_html = ""
        if report.cms_info:
            cms_name = report.cms_info.get("cms", "Unknown")
            cms_html = f"<div class='cms-tag'>Detected CMS: <strong>{cms_name}</strong></div>"

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AdSense Readiness Executive Report - {report.target_url}</title>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --primary: #3b82f6;
            --accent: {status_color};
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text-main);
            padding: 2.5rem 1.5rem;
            line-height: 1.6;
        }}
        .container {{ max-width: 1080px; margin: 0 auto; }}
        header.report-hero {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2.5rem;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        .hero-info h1 {{ font-size: 2.2rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 0.5rem; }}
        .hero-info p {{ color: var(--text-muted); font-size: 1rem; margin-bottom: 0.25rem; }}
        .cms-tag {{ display: inline-block; background: #3b82f622; color: #60a5fa; border: 1px solid #3b82f6; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.85rem; margin-top: 0.5rem; }}
        
        .score-circle {{
            position: relative;
            width: 160px;
            height: 160px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            border-radius: 50%;
            border: 8px solid {status_color};
            background: rgba(30, 41, 59, 0.8);
            box-shadow: 0 0 25px {status_color}44;
        }}
        .score-number {{ font-size: 3rem; font-weight: 900; color: {status_color}; line-height: 1; }}
        .score-total {{ font-size: 0.9rem; color: var(--text-muted); }}

        .verdict-banner {{
            border-radius: 12px;
            padding: 1.25rem 1.75rem;
            margin-bottom: 2rem;
            background: {status_color}1a;
            border-left: 6px solid {status_color};
            font-size: 1.15rem;
            font-weight: 600;
        }}

        .blockers-section {{
            background: #ef444415;
            border: 1px solid #ef444466;
            border-radius: 14px;
            padding: 1.75rem;
            margin-bottom: 2.5rem;
        }}
        .blockers-section h2 {{ color: #f87171; margin-bottom: 1.25rem; font-size: 1.4rem; }}
        .blocker-box {{ background: #1e293b; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem; border-left: 4px solid #ef4444; }}
        .blocker-box h4 {{ color: #fca5a5; font-size: 1.1rem; margin-bottom: 0.5rem; }}
        .fix-box {{ margin-top: 0.5rem; color: #fbbf24; background: #fbbf2415; padding: 0.5rem; border-radius: 6px; }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }}
        @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr; }} }}

        .pillar-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }}
        .pillar-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }}
        .pillar-header h3 {{ font-size: 1.2rem; }}
        .pillar-badge {{ font-size: 0.85rem; font-weight: 700; padding: 0.25rem 0.65rem; border-radius: 999px; }}
        
        .progress-bar-bg {{ background: #334155; border-radius: 999px; height: 8px; width: 100%; margin-bottom: 1.25rem; overflow: hidden; }}
        .progress-bar-fill {{ height: 100%; border-radius: 999px; transition: width 0.5s ease; }}

        .checks-list {{ list-style: none; }}
        .check-item {{ display: flex; gap: 0.85rem; margin-bottom: 1rem; font-size: 0.92rem; align-items: flex-start; }}
        .check-name .pts {{ color: var(--text-muted); font-size: 0.85rem; }}
        .check-desc {{ color: var(--text-muted); font-size: 0.88rem; margin-top: 0.15rem; }}
        .fix-tip {{ margin-top: 0.4rem; color: #fbbf24; font-size: 0.85rem; }}

        .action-plan-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
        }}
        .action-plan-card h2 {{ font-size: 1.5rem; margin-bottom: 1rem; color: #60a5fa; }}
        .action-list {{ list-style: none; }}
        .action-item {{ display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 0.85rem; font-size: 0.95rem; }}
        .action-item input[type="checkbox"] {{ margin-top: 0.3rem; transform: scale(1.2); accent-color: var(--primary); }}

        footer.report-footer {{
            text-align: center;
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="report-hero">
            <div class="hero-info">
                <p>Official Readiness Audit Evaluation</p>
                <h1>{report.target_url}</h1>
                <p>Audited on {report.timestamp[:10]} | Google Policy Ruleset: <strong>v{report.policy_version}</strong></p>
                {cms_html}
            </div>
            <div class="score-circle">
                <span class="score-number">{score}</span>
                <span class="score-total">/ 100 PTS</span>
            </div>
        </header>

        <div class="verdict-banner">
            Verdict: {report.summary_verdict}
        </div>

        {blockers_html}

        <h2 style="font-size: 1.6rem; margin-bottom: 1rem;">📊 7-Pillar Detailed Evaluation</h2>
        <div class="grid">
            {''.join(cards_html)}
        </div>

        <div class="action-plan-card">
            <h2>📋 Prioritized Remediation Action Plan</h2>
            <ul class="action-list">
                {''.join(action_items)}
            </ul>
        </div>

        <footer class="report-footer">
            Generated automatically by <strong>AdSenseReady-AI</strong>. Open source under MIT License.
        </footer>
    </div>
</body>
</html>
"""
        return html_template

    @staticmethod
    def to_json(report: AuditReport) -> str:
        """Serializes report to structured JSON format."""
        data = {
            "target_url": report.target_url,
            "timestamp": report.timestamp,
            "policy_version": report.policy_version,
            "total_score": report.total_score,
            "max_possible": report.max_possible,
            "normalized_score": report.normalized_score,
            "verdict": report.verdict,
            "summary_verdict": report.summary_verdict,
            "all_blockers_count": len(report.all_blockers),
            "pillars": {
                p_id: {
                    "name": p.name,
                    "earned_score": p.earned_score,
                    "max_score": p.max_score,
                    "percentage": p.percentage,
                    "checks": [
                        {
                            "id": c.id,
                            "name": c.name,
                            "status": c.status.value,
                            "severity": c.severity.value,
                            "score": c.score,
                            "max_score": c.max_score,
                            "details": c.details,
                            "fix_recommendation": c.fix_recommendation,
                            "doc_url": c.doc_url
                        }
                        for c in p.checks
                    ]
                }
                for p_id, p in report.pillars.items()
            },
            "action_plan": report.action_plan
        }
        return json.dumps(data, indent=2)
