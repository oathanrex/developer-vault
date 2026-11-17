"""
AdSenseReady-AI: Model Context Protocol (MCP) Server
Allows Claude Desktop, Cursor, Antigravity, and any MCP client to use AdSenseReady-AI as a native tool.
"""

import sys
import json
import os
from pathlib import Path
from typing import Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.auditor import AdSenseAuditor
from src.reporter import AuditReporter
from scripts.sync_policies import sync as sync_policies_func
from src.enhancer import LowValueContentEliminator

SERVER_INFO = {
    "name": "adsenseready-ai-mcp",
    "version": "2026.11.1"
}

TOOLS = [
    {
        "name": "audit_website",
        "description": "Performs a 360-degree Google AdSense readiness audit on any website across 7 pillars (Legal, EEAT, SEO, UX, Policies, Layout, Footprint).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The full target website URL (e.g. 'https://myblog.com')"
                },
                "crawl_depth": {
                    "type": "integer",
                    "description": "Maximum number of articles to sample (default: 15)",
                    "default": 15
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "sync_policies",
        "description": "Syncs local AdSense audit rules with official live Google Publisher Policy endpoints.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "explain_rejection_reason",
        "description": "Explains common Google AdSense rejection notices (e.g. 'Low Value Content', 'Site Under Construction', 'Policy Violation') and gives exact recovery steps.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "description": "The exact rejection message received from Google AdSense"
                }
            },
            "required": ["reason"]
        }
    },
    {
        "name": "diagnose_thin_content",
        "description": "Diagnoses an article text or HTML for Google AdSense 'Thin Content' and 'Low Value Content' risks, calculating word deficit and structural gaps.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The article text or raw HTML to diagnose"
                },
                "title": {
                    "type": "string",
                    "description": "Title of the article (optional)"
                }
            },
            "required": ["content"]
        }
    },
    {
        "name": "eliminate_low_value_content",
        "description": "Generates a 1200+ word expansion blueprint, Schema.org FAQPage JSON-LD, and E-E-A-T credentials box to completely resolve Google AdSense 'Low Value Content' penalties.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The primary topic of the article"
                },
                "current_content": {
                    "type": "string",
                    "description": "Current thin article text or draft"
                },
                "author_name": {
                    "type": "string",
                    "description": "Author name for E-E-A-T byline",
                    "default": "Oathan Rex"
                }
            },
            "required": ["topic", "current_content"]
        }
    }
]


REJECTION_GUIDES = {
    "low value content": """
### How to Fix Google AdSense "Low Value Content":
1. **Article Count**: Ensure you have at least 25-30+ published, indexed posts.
2. **Word Count**: Expand every article to at least 800-1200+ substantive words. Remove posts under 500 words.
3. **E-E-A-T**: Add a named author byline with expertise, experience, and editorial disclosure on every post.
4. **Originality**: Eliminate generic AI fluff and provide unique perspectives, case studies, or first-hand experience.
5. **Topical Authority**: Focus on 1-3 tightly coherent categories rather than scattered random topics.
""",
    "site under construction": """
### How to Fix Google AdSense "Site Under Construction":
1. **Broken Links**: Audit all navigation links and eliminate empty `href="#"` links.
2. **Demo Posts**: Delete WordPress default 'Hello World!' post and 'Sample Page'.
3. **Empty Categories**: Remove any category or tag archive that has fewer than 3 posts.
4. **Header/Footer**: Ensure your top menu and footer are populated with real working links.
""",
    "site behavior": """
### How to Fix Google AdSense "Site Behavior: Navigation":
1. **Category Navigation**: Every menu item must lead to an index of active articles.
2. **No Misleading Clicks**: Do not place download buttons near future ad units.
3. **Mobile Responsiveness**: Verify that the mobile menu opens and functions cleanly on phones.
"""
}


def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if name == "audit_website":
        url = arguments.get("url")
        crawl_depth = arguments.get("crawl_depth", 15)
        auditor = AdSenseAuditor()
        report = auditor.audit_site(url, max_crawl_pages=crawl_depth)
        md = AuditReporter.to_markdown(report)
        return {
            "content": [
                {
                    "type": "text",
                    "text": md
                }
            ]
        }
    elif name == "sync_policies":
        code = sync_policies_func()
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Policy sync completed with exit code: {code}. Local rules updated to match official Google standards."
                }
            ]
        }
    elif name == "explain_rejection_reason":
        reason = arguments.get("reason", "").lower()
        explanation = None
        for key, text in REJECTION_GUIDES.items():
            if key in reason:
                explanation = text
                break
        if not explanation:
            explanation = f"General Remediation for '{arguments.get('reason')}': Ensure mandatory legal pages (Privacy Policy with DART cookie clause), minimum 25 original articles, and clean navigation."

        return {
            "content": [
                {
                    "type": "text",
                    "text": explanation
                }
            ]
        }
    elif name == "diagnose_thin_content":
        content = arguments.get("content", "")
        title = arguments.get("title", "Article")
        eliminator = LowValueContentEliminator()
        diag = eliminator.diagnose(content, title=title)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(diag, indent=2)
                }
            ]
        }
    elif name == "eliminate_low_value_content":
        topic = arguments.get("topic", "")
        current_content = arguments.get("current_content", "")
        author_name = arguments.get("author_name", "Oathan Rex")
        eliminator = LowValueContentEliminator()
        plan = eliminator.generate_expansion_plan(topic, current_content, author_name=author_name)
        text_result = f"""
{plan['blueprint_instructions']}

### 1. Schema.org FAQPage JSON-LD:
```json
{plan['faq_schema_ldjson']}
```

### 2. E-E-A-T Author Credentials Box HTML:
```html
{plan['eeat_author_box_html']}
```
"""
        return {
            "content": [
                {
                    "type": "text",
                    "text": text_result
                }
            ]
        }
    else:
        raise ValueError(f"Unknown tool: {name}")


def main():
    """Runs standard JSON-RPC 2.0 loop over stdin/stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": SERVER_INFO,
                        "capabilities": {
                            "tools": {}
                        }
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": TOOLS
                    }
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                result = handle_call_tool(tool_name, tool_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": result
                }
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": f"Internal MCP server error: {str(e)}"
                }
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
