"""
AdSenseReady-AI: Command Line Interface
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.auditor import AdSenseAuditor
from src.reporter import AuditReporter
from scripts.sync_policies import sync as sync_policies_func
from src.server import start_server
from src.enhancer import LowValueContentEliminator


def main():
    parser = argparse.ArgumentParser(
        description="🎯 AdSenseReady-AI: 360-Degree Google AdSense Readiness Audit Engine (Top 1% Quality)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.cli https://mytechblog.com
  python -m src.cli https://mytechblog.com --format markdown --output adsense_report.md
  python -m src.cli https://mytechblog.com --format json --output report.json
  python -m src.cli --sync-policies
  python -m src.cli --demo
        """
    )

    parser.add_argument("url", nargs="?", help="Target website URL to audit (e.g. https://example.com)")
    parser.add_argument("--format", choices=["terminal", "markdown", "json", "html"], default="terminal", help="Output format (default: terminal)")
    parser.add_argument("--output", "-o", help="Optional output file path to write Markdown or JSON report")
    parser.add_argument("--crawl-depth", type=int, default=15, help="Maximum number of pages to sample (default: 15)")
    parser.add_argument("--sync-policies", action="store_true", help="Sync local rules with live Google Publisher Policy updates")
    parser.add_argument("--demo", action="store_true", help="Run auditor on built-in mock demo sites (ready vs rejected)")
    parser.add_argument("--serve", nargs="?", const=8080, type=int, help="Launch local web UI studio on specified port (default: 8080)")
    parser.add_argument("--fix-content", help="Diagnose thin content and generate a 1200+ word expansion blueprint for an article or URL")
    parser.add_argument("--topic", default="Technical Guide", help="Topic name for the article expansion (default: 'Technical Guide')")
    parser.add_argument("--author", default="Oathan Rex", help="Author name for E-E-A-T credentials box (default: 'Oathan Rex')")

    args = parser.parse_args()

    if args.fix_content:
        run_content_fix(args.fix_content, args.topic, args.author, args.format, args.output)
        return

    if args.serve:
        start_server(args.serve)
        return

    if args.sync_policies:
        sys.exit(sync_policies_func())

    if args.demo:
        run_demo(args.format, args.output)
        return

    if not args.url:
        parser.print_help()
        sys.exit(1)

    auditor = AdSenseAuditor()
    print(f"[*] Crawling and auditing target site: {args.url} ...")
    report = auditor.audit_site(args.url, max_crawl_pages=args.crawl_depth)

    if args.format == "terminal":
        AuditReporter.render_terminal(report)
    elif args.format == "markdown":
        md = AuditReporter.to_markdown(report)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(md)
            print(f"[✓] Markdown report successfully written to {args.output}")
        else:
            print(md)
    elif args.format == "html":
        ht = AuditReporter.to_html(report)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(ht)
            print(f"[✓] Interactive HTML report successfully written to {args.output}")
        else:
            print(ht)
    elif args.format == "json":
        js = AuditReporter.to_json(report)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(js)
            print(f"[✓] JSON report successfully written to {args.output}")
        else:
            print(js)


def run_content_fix(source: str, topic: str, author: str, out_format: str, output_file: str):
    eliminator = LowValueContentEliminator()
    raw_content = source

    # If it's a file path
    p = Path(source)
    if p.exists() and p.is_file():
        with open(p, "r", encoding="utf-8") as f:
            raw_content = f.read()
    elif source.startswith("http://") or source.startswith("https://"):
        auditor = AdSenseAuditor()
        html, _, _ = auditor.fetch_url(source)
        if html:
            raw_content = html

    plan = eliminator.generate_expansion_plan(topic, raw_content, author_name=author)
    diag = plan["diagnosis"]

    print("=" * 65)
    print(f" 🚀 Low-Value Content Eliminator: {topic}")
    print("=" * 65)
    print(f" Current Substance: {diag['current_word_count']} words (Target: 1,200+ words)")
    print(f" Risk Assessment:   {diag['risk_level']} (Thin Content Penalty Risk)")
    print(f" Readability:       {diag['readability_score']}/100 ({diag['readability_label']})")
    print(f" Additional Needed: +{diag['words_needed']} words of high-substance value\n")

    if diag["structural_gaps"]:
        print(" 🚨 Detected Structural Deficits:")
        for gap in diag["structural_gaps"]:
            print(f"   • {gap}")
        print()

    print(plan["blueprint_instructions"])

    if output_file:
        out_content = f"""# High-Value Content Transformation: {topic}

{plan['blueprint_instructions']}

## 1. Schema.org FAQPage JSON-LD
```json
{plan['faq_schema_ldjson']}
```

## 2. E-E-A-T Author Credentials Box HTML
```html
{plan['eeat_author_box_html']}
```
"""
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(out_content)
        print(f"[✓] Full High-Value Content Blueprint saved to: {output_file}")


def run_demo(out_format="terminal", output_file=None):
    from tests.mock_sites.sample_data import READY_SITE_HTML
    auditor = AdSenseAuditor()
    print("[*] Running demonstration audit on High-Quality Ready Site...")
    report = auditor.audit_site("https://demotechjournal.com", mock_html=READY_SITE_HTML)
    if out_format == "terminal":
        AuditReporter.render_terminal(report)
    elif out_format == "markdown":
        md = AuditReporter.to_markdown(report)
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(md)
            print(f"[✓] Demo Markdown report written to {output_file}")
        else:
            print(md)


if __name__ == "__main__":
    main()
