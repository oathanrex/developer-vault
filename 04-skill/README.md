<div align="center">

# 🎯 AdSenseReady-AI
### The Universal AI Skill, Native MCP Server & 360° Automated Audit Engine for 100% Google AdSense Approval Readiness

[![CI Test Suite](https://img.shields.io/badge/CI-Passing-brightgreen.svg)]()
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Compatible-purple.svg)](https://modelcontextprotocol.io/)
[![Google Policies](https://img.shields.io/badge/Google%20Policy%20Sync-Live%20v2026.11-success.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Curated by Oathan Rex](https://img.shields.io/badge/Author-Oathan%20Rex-0d6e52.svg)](https://github.com/oathanrex)

*Eliminate Google AdSense rejections for **"Low Value Content"**, **"Site Under Construction"**, and **"Policy Violations"**. Forensic 7-pillar evaluation with dynamic auto-updating Google policy sync.*

[Quick Start](#-quick-start--installation) • [7-Pillar Matrix](#-the-7-pillar-audit-matrix) • [HTML Dashboard](#-multi-format-reporting) • [MCP Server Setup](#-model-context-protocol-mcp-integration) • [Cross-AI Agents](#-universal-cross-ai-compatibility)

---

</div>

## 🌟 Overview & Problem Solved

Every year, millions of webmasters, bloggers, and indie hackers receive automated rejection emails from Google AdSense stating:
> *"Your site isn't ready to show ads. We found some policy violations: Low-value content / Site behavior: Navigation."*

Google's review system uses a combination of **automated ML classifiers** and **human quality raters**. Standard SEO audit tools (Ahrefs, Semrush, Lighthouse) only check generic technical scores — **none of them evaluate Google's exact publisher compliance rules**.

**AdSenseReady-AI** bridges this gap:
- Reverse-engineers Google's 7 approval pillars into a weighted 100-point calibrated index.
- Detects **instant blockers** before you waste weeks waiting for rejection emails.
- Generates a prioritized, step-by-step remediation action plan with exact fixes.
- **Evergreen Policy Sync:** Probes Google's official Search Central RSS feeds and AdSense Help documentation, automatically updating rules via GitHub Actions.

---

## 🏛️ The 7-Pillar Audit Matrix

| Pillar | Weight | Key Google Requirements & Checks |
| :--- | :---: | :--- |
| **1. Legal & Trust Foundation** | 20% | Mandatory Privacy Policy with explicit Google/DoubleClick DART cookie disclosure & opt-out links (`aboutads.info`), Terms of Service, Human About Us page, and working Contact Us form/email. |
| **2. Content Depth & E-E-A-T** | 25% | Min 25-30+ original articles, 700-1200+ avg word count, Flesch Reading Ease analysis, zero generic AI boilerplate (*"In conclusion...", "As an AI language model..."*), H1/H2 hierarchy, named author attribution. |
| **3. Technical SEO & Crawlability** | 15% | SSL/HTTPS enforced everywhere, clean `robots.txt` explicitly allowing `User-agent: Mediapartners-Google`, valid XML sitemap, mobile responsive viewport. |
| **4. Site Navigation & UX** | 15% | Intuitive primary menu, semantic footer, zero dead/placeholder links (`href="#"`), zero 'Under Construction' or demo posts ('Hello World'). |
| **5. Google Publisher Policies** | 15% | Zero prohibited niche content (warez, torrents, cracks, betting, hacking, adult), zero deceptive download triggers or fake CTA buttons. |
| **6. Ad Layout & Ergonomics** | 5% | Content superiority (content visible above fold), CLS layout shift prevention, zero intrusive popups/interstitials blocking reading. |
| **7. Organic Footprint & Signals** | 5% | Canonical tags configured, robots allowing `index, follow`, Schema.org structured data (Article/Organization). |

---

## 🚀 Quick Start & Installation

### 1. Installation
Clone the repository and install optional rich dependencies:
```bash
git clone https://github.com/oathanrex/developer-vault.git
cd developer-vault/04-skill
pip install -r requirements.txt
```
*(Zero mandatory dependencies: The core audit engine runs on pure Python standard library out of the box!)*

### 2. Run a Live Audit via CLI
```bash
# Terminal colored display
python -m src.cli https://mytechblog.com

# Generate Standalone Interactive HTML Executive Dashboard
python -m src.cli https://mytechblog.com --format html --output adsense_report.html

# Generate Markdown Report
python -m src.cli https://mytechblog.com --format markdown --output report.md

# Generate Structured JSON for CI/CD Pipelines
python -m src.cli https://mytechblog.com --format json --output report.json
```

### 3. Launch Local Web Studio
```bash
python -m src.cli --serve 8080
# Open http://localhost:8080 in your browser for instant GUI auditing
```

### 4. Run Built-In Benchmark Demo
```bash
python -m src.cli --demo
```

---

## 🔌 Model Context Protocol (MCP) Integration

AdSenseReady-AI includes a production-grade **MCP Server** (`src/mcp_server.py`) conforming to the official Model Context Protocol JSON-RPC standard.

### Connect with Claude Desktop / Cursor
Add the following snippet to your MCP settings file:
- **Claude Desktop:** `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
- **Cursor Settings:** `Cursor Settings -> Features -> MCP -> Add New MCP Server`

```json
{
  "mcpServers": {
    "adsenseready": {
      "command": "python",
      "args": ["<PATH_TO_REPO>/04-skill/src/mcp_server.py"]
    }
  }
}
```

Now you can instruct your AI assistant in plain English:
> *"Audit https://myblog.com for Google AdSense readiness."*  
> *"Explain why AdSense rejected my application for 'Low Value Content' and tell me how to fix it."*

---

## 🤖 Universal Cross-AI Compatibility

| AI Assistant | Integration Method | Configuration File |
| :--- | :--- | :--- |
| **Antigravity / Gemini CLI** | Built-in Agent Skill | [`SKILL.md`](./SKILL.md) |
| **Claude Code** | Native CLI instructions | [`CLAUDE.md`](./CLAUDE.md) |
| **Cursor IDE** | Project & Directory Rules | [`.cursorrules`](./.cursorrules) & [`.cursor/rules/`](./.cursor/rules/adsense-readiness.mdc) |
| **ChatGPT / Custom GPT** | 1-Click Instructions | [`prompts/chatgpt_custom_gpt.md`](./prompts/chatgpt_custom_gpt.md) |
| **Terminal / Bash / Python** | Standalone Executable | `python -m src.cli` |

---

## 🔄 Dynamic Self-Updating Policy Engine

Google continuously modifies Search Essentials, spam algorithms, and consent management guidelines. AdSenseReady-AI keeps your rules evergreen:

```bash
python scripts/sync_policies.py
```

- **Live RSS Monitoring:** Probes Google Search Central and Google Ads official RSS feeds, extracting latest announcements.
- **Policy Versioning:** Updates `policies/adsense_rules.json` and records changelogs in `policies/changelog.json`.
- **Automated GitHub Action:** [`.github/workflows/policy-sync.yml`](./.github/workflows/policy-sync.yml) runs weekly on cron (`0 0 * * 0`) and automatically creates a Pull Request when Google updates policy documentation.

---

## 🧪 Testing & Verification

Run the full automated test suite (all 7 tests passing):
```bash
python -m pytest tests/
```

---

## 📄 License & Credits

Created and curated by **[Oathan Rex](https://github.com/oathanrex)** under the **MIT License**.  
Part of **[The Developer Vault](https://github.com/oathanrex/developer-vault)**.
