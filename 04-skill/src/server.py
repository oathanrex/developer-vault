"""
AdSenseReady-AI: Lightweight Embedded Web Dashboard Server
Runs an instant browser UI for entering website URLs and viewing visual audit reports.
"""

import sys
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.auditor import AdSenseAuditor
from src.reporter import AuditReporter

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AdSenseReady-AI Web Audit Studio</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #0f172a;
            color: #f8fafc;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 1.5rem;
        }
        .card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 2.5rem;
            max-width: 580px;
            width: 100%;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }
        h1 { font-size: 2rem; margin-bottom: 0.5rem; color: #f8fafc; }
        p { color: #94a3b8; font-size: 1rem; margin-bottom: 2rem; }
        input[type="url"] {
            width: 100%;
            box-sizing: border-box;
            padding: 1rem 1.25rem;
            border-radius: 10px;
            border: 1px solid #475569;
            background: #0f172a;
            color: #f8fafc;
            font-size: 1.05rem;
            margin-bottom: 1.25rem;
            outline: none;
        }
        input[type="url"]:focus { border-color: #3b82f6; box-shadow: 0 0 10px rgba(59,130,246,0.3); }
        button {
            width: 100%;
            padding: 1rem;
            border-radius: 10px;
            border: none;
            background: #2563eb;
            color: white;
            font-weight: 700;
            font-size: 1.1rem;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover { background: #1d4ed8; }
        .footer-note { margin-top: 1.5rem; font-size: 0.85rem; color: #64748b; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🎯 AdSenseReady-AI</h1>
        <p>Enter your website URL to run a forensic 360° Google AdSense approval audit.</p>
        <form action="/audit" method="GET">
            <input type="url" name="url" placeholder="https://myblog.com" required autofocus>
            <button type="submit">Run 360° Readiness Audit 🚀</button>
        </form>
        <div class="footer-note">
            Evaluates 7 Pillars: Legal, E-E-A-T, Tech SEO, UX, Policies, Layout & Schema.
        </div>
    </div>
</body>
</html>
"""


class AuditDashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(INDEX_HTML.encode("utf-8"))
        elif parsed.path == "/audit":
            qs = urllib.parse.parse_qs(parsed.query)
            url = qs.get("url", [""])[0]
            if not url:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Error: URL parameter required.")
                return

            try:
                auditor = AdSenseAuditor()
                report = auditor.audit_site(url)
                html_report = AuditReporter.to_html(report)
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html_report.encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<h2>Audit Error:</h2><p>{str(e)}</p>".encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def start_server(port: int = 8080):
    server = HTTPServer(("0.0.0.0", port), AuditDashboardHandler)
    print("=" * 60)
    print(f" 🚀 AdSenseReady-AI Web Studio running at: http://localhost:{port}")
    print(" Press Ctrl+C to stop the server.")
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopping server...")
        server.server_close()


if __name__ == "__main__":
    start_server(8080)
