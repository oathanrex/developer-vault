---
name: adsense-readiness
description: >-
  Universal 360-degree Google AdSense readiness audit engine and evaluator.
  Analyzes websites across all 7 pillars of Google Publisher Policies, E-E-A-T,
  content depth, technical SEO, navigation UX, legal compliance, and invalid
  activity risks. Includes self-updating policy sync with official Google guidelines.
---

# 🎯 AdSenseReady-AI: Universal Google AdSense Readiness Skill

This skill equips any AI assistant (Antigravity, Claude Code, Cursor, ChatGPT, Codex, GitHub Copilot) to conduct forensic audits of any website or codebase to determine its readiness for **100% Google AdSense approval**.

---

## 🧭 When to Activate This Skill

Activate this skill whenever the user asks:
- "Check if my website is ready for Google AdSense."
- "Why was my site rejected by AdSense for 'Low Value Content' or 'Site Behavior'?"
- "Audit my blog for Google Publisher Policy compliance."
- "What pages, articles, or legal disclosures am I missing before applying to AdSense?"
- "Update local AdSense policies with the latest Google publisher guidelines."

---

## ⚡ Quick Execution Commands

The skill provides an integrated Python audit engine that can be executed directly:

### 1. Run Live Audit on Any Website:
```bash
python -m src.cli https://example.com
```

### 2. Export Detailed Markdown Report for Client / User:
```bash
python -m src.cli https://example.com --format markdown --output adsense_report.md
```

### 3. Export JSON for Automated CI/CD Pipelines:
```bash
python -m src.cli https://example.com --format json --output adsense_report.json
```

### 4. Sync Policies with Latest Live Google Guidelines:
```bash
python scripts/sync_policies.py
```

### 5. Run Built-In Benchmark Test:
```bash
python -m src.cli --demo
```

---

## 🏛️ The 7 Pillars of AdSense Approval (Scoring Rubric)

Google evaluates publications using both automated machine-learning classifiers and human quality raters. This skill calculates a weighted index from **0 to 100**:

| Pillar | Weight | Key Google Requirements |
| :--- | :---: | :--- |
| **1. Mandatory Legal & Trust** | 20% | Explicit Privacy Policy disclosing Google/DoubleClick cookies & opt-out links, Terms of Service, Human About Us page, Direct Contact Us (email/form). |
| **2. Content Depth & E-E-A-T** | 25% | Min 25-30+ original articles, 700-1200+ avg word count, zero generic AI boilerplate/hallucination markers, structured H1/H2 hierarchy, named author attribution. |
| **3. Technical SEO & Crawlability** | 15% | SSL/HTTPS enforced everywhere, clean `robots.txt` explicitly allowing `Mediapartners-Google`, valid XML sitemap, mobile responsive viewport. |
| **4. Site Navigation & UX** | 15% | Intuitive primary menu, semantic footer, zero dead/placeholder links (`href="#"`), zero 'Under Construction' or demo posts ('Hello World'). |
| **5. Google Publisher Policies** | 15% | Zero prohibited niche content (warez, torrents, cracks, betting, hacking, adult), zero deceptive download triggers or fake CTA buttons. |
| **6. Ad Layout & Ergonomics** | 5% | Content superiority (content visible above fold), CLS layout shift prevention, zero intrusive popups/interstitials blocking reading. |
| **7. Organic Footprint & Signals** | 5% | Canonical tags configured, robots allowing `index, follow`, Schema.org structured data (Article/Organization). |

---

## 📊 Approval Verdict Thresholds

- **Score 85 - 100 & 0 Blockers:** `✅ APPROVED_READY`
  - High confidence. Publication meets all Google publisher guidelines.
- **Score 65 - 84 & 0 Blockers:** `⚠️ AT_RISK`
  - Needs polish. Likely rejection for "Low Value Content" or missing legal nuance.
- **Score < 65 OR >= 1 Blocker:** `❌ REJECTION_GUARANTEED`
  - Immediate rejection by automated bot or manual reviewer. Blockers must be remediated first.

---

## 🔄 Self-Updating Policy Synchronization

Google updates its Search Essentials, spam policies, and publisher compliance rules regularly. This skill maintains evergreen accuracy via `scripts/sync_policies.py`:

- Monitors official Google AdSense Help Center, Search Central RSS, EU Consent requirements, and Publisher Policy endpoints.
- Auto-detects content changes and increments policy version.
- Configurable via GitHub Actions (`.github/workflows/policy-sync.yml`) for automated weekly updates and pull requests.
