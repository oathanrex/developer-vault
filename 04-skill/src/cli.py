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

    args = parser.parse_args()

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
