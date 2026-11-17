<div align="center">

# ⚡ The Developer Vault
### Top 1% Production AI Prompts • Claude Engineering SOPs • Software PRDs • Developer Playbooks

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/oathanrex/developer-vault/pulls)
[![Curated by Oathan Rex](https://img.shields.io/badge/Curator-Oathan%20Rex-0d6e52.svg)](https://oathanrex.github.io/)

*An authoritative, battle-tested collection of production-grade AI prompts, deterministic Claude execution playbooks, architectural software specifications (PRDs), and developer tools crafted by **[@oathanrex](https://github.com/oathanrex)**.*

[Explore AI Prompts](#-01-ai-prompts--engineering-playbooks) • [Product PRDs](#-02-product-specifications--prds) • [Tools & Audits](#-03-tools--case-studies) • [AI Skill & MCP](#-04-universal-ai-skills--mcp-servers) • [Claude SOP](#-claude-zero-error-execution-workflow)

---

</div>

## 📌 Repository Architecture

```
developer-vault/
├── 01-ai-prompts/                           # Battle-tested prompts & LLM behavioral controls
│   ├── code-review/                         # Universal technical reviews & complexity audits
│   │   ├── universal-code-review-master.md  # Exhaustive master review prompt
│   │   └── code-review-playbook.md          # Multi-tier review templates (Beginner to Advanced)
│   ├── debugging/                           # Multi-platform & domain-specific bug isolation
│   │   ├── cross-platform-debugging.md      # Tailored for ChatGPT, Claude, and GitHub Copilot
│   │   └── domain-specific-debugging.md     # Frontend, Backend, ML, Python, and JavaScript
│   ├── prompt-engineering/                  # Meta-prompts & prompt synthesis systems
│   │   ├── universal-prompt-engineer.md     # Multi-perspective master meta-prompt
│   │   ├── coding-prompt-engineer.md        # Software engineering prompt generator
│   │   └── prompt-studio-flow.json          # AI Studio visual prompt flow pipeline
│   ├── claude-playbooks/                    # Deterministic Claude execution & guardrails
│   │   ├── claude-error-control-playbook.md # Hallucination prevention & error mitigation
│   │   ├── claude-sop-guide.md              # Zero-error paste-only sequential workflow
│   │   └── claude-engineering-guidelines.md # Karpathy-inspired tradeoff dials & rules
│   ├── media-and-video/                     # Automated content creation prompts
│   │   ├── video-generation-instructions.md # Video pipeline master instructions
│   │   └── voiceover-script-prompt.md       # Synchronized voiceover script generator
│   └── seo-and-content/                     # High-ranking search & editorial engines
│       ├── blogger-seo-prompts.md           # Page assembly, metadata & alt-text generator
│       └── adsense-human-content-engine/    # Complete editorial quality gate & standards
├── 02-product-specifications-prds/          # Enterprise-grade product specifications
│   ├── markdown-studio/                     # MarkdownStudio Pro v3.0.0 & Editor Architecture
│   ├── orex-ui/                             # OrexUI Design System, Token System & Primitives
│   ├── image-converter/                     # Client-side Image Transcoder & Geometry Engine
│   └── blogger-widgeta/                     # Blogger Widget SDK & Custom Tiptap Extensions
└── 03-tools-and-audits/                     # Standalone utilities & technical reviews
    ├── markdown-renderer/                   # Standalone Primer GitHub Markdown Viewer
    ├── audits/                              # Static site audit checklist & in-depth case study
    └── referrals/                           # Curated developer utilities & partner benefits
├── 04-skill/                                # Universal AI Skills & Native MCP Servers
│   ├── src/                                 # 360° Forensic Audit Engine & MCP Server
│   ├── policies/                            # Dynamic versioned Google AdSense policy ruleset
│   ├── scripts/sync_policies.py             # Evergreen Google RSS policy sync automation
│   ├── SKILL.md                             # Universal Agent Skill for Antigravity & AI
│   └── README.md                            # AdSenseReady-AI Top 1% Documentation
```

---

## 🚀 01. AI Prompts & Engineering Playbooks

### 🔍 Code Review Suite
* **Master Review Prompt** ([`01-ai-prompts/code-review/universal-code-review-master.md`](./01-ai-prompts/code-review/universal-code-review-master.md)): Exhaustive technical audit evaluating correctness, time/space complexity, error handling, memory leaks, architecture cohesion, and test coverage.
* **Code Review Playbook** ([`01-ai-prompts/code-review/code-review-playbook.md`](./01-ai-prompts/code-review/code-review-playbook.md)): Beginner-friendly explanations to senior-architect deep dives with standardized variable placeholders (`{{CODE}}`, `{{LANGUAGE}}`, `{{TARGET_COMPLEXITY}}`).

### 🐛 Debugging Suite
* **Platform-Targeted Debugging** ([`01-ai-prompts/debugging/cross-platform-debugging.md`](./01-ai-prompts/debugging/cross-platform-debugging.md)): Optimized for how different LLMs reason:
  * **ChatGPT**: Focuses on conceptual refactoring and step-by-step logic tracing.
  * **Claude**: Focuses on systemic root-cause isolation and strict non-breaking diffs.
  * **GitHub Copilot**: Focuses on fast, inline localized repairs.
* **Domain-Specific Debugging** ([`01-ai-prompts/debugging/domain-specific-debugging.md`](./01-ai-prompts/debugging/domain-specific-debugging.md)): Dedicated patterns for Frontend (React/CSS/DOM), Backend (APIs/Databases/Concurrency), Machine Learning, Python, and TypeScript.

### 🧠 Prompt Engineering
* **Universal Meta-Prompt** ([`01-ai-prompts/prompt-engineering/universal-prompt-engineer.md`](./01-ai-prompts/prompt-engineering/universal-prompt-engineer.md)): Generates prompts using a 9-dimensional perspective matrix (reasoning, safety, multimodal, optimization, and edge cases).
* **Coding Prompt Engineer** ([`01-ai-prompts/prompt-engineering/coding-prompt-engineer.md`](./01-ai-prompts/prompt-engineering/coding-prompt-engineer.md)): Converts fuzzy requirements into rock-solid software engineering specifications.

---

## 🛡️ Claude Zero-Error Execution Workflow

When delegating complex multi-file codebase changes to Claude or any advanced agent, use our **Sequential Paste Workflow** from [`01-ai-prompts/claude-playbooks/claude-sop-guide.md`](./01-ai-prompts/claude-playbooks/claude-sop-guide.md):

```
┌────────────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
│  Phase 1: Architecture │ ───> │   Phase 2: Execution   │ ───> │  Phase 3: Verification │
│  (Read-Only Research)  │      │   (Targeted Diff Only) │      │  (Tests & Lint Check)  │
└────────────────────────┘      └────────────────────────┘      └────────────────────────┘
```

1. **Step 1 (Context Ingestion)**: Instruct the model to review files in read-only mode and declare its understanding before writing any code.
2. **Step 2 (Targeted Diff)**: Enforce unified diffs or minimal surgical edits to prevent file truncation or unintended regressions.
3. **Step 3 (Post-Execution Verification)**: Require explicit verification commands (`npm test`, `npm run lint`) and confirmation of untouched boundaries.

---

## 📐 02. Product Specifications & PRDs

The PRD library provides complete, production-ready specifications written according to strict product engineering principles:

| System | Focus | Core Features | Documentation |
| :--- | :--- | :--- | :--- |
| **MarkdownStudio Pro** | Privacy-first Markdown Editor | Zero-upload local storage, live split-pane, KaTeX, Mermaid, syntax highlighting | [`MarkdownStudio-Pro-v3.0.0.md`](./02-product-specifications-prds/markdown-studio/MarkdownStudio-Pro-v3.0.0.md) |
| **OrexUI** | Modern Design System | OKLCH color token scales, accessible primitives, zero-runtime overhead | [`orex-ui-prd-part-1.md`](./02-product-specifications-prds/orex-ui/orex-ui-prd-part-1.md) |
| **Image Converter** | Client-Side Image Suite | Client-side Canvas/WASM batch conversion, WebP/AVIF export, Perspective Correction | [`image-converter-prd.md`](./02-product-specifications-prds/image-converter/image-converter-prd.md) |
| **Blogger Widgeta** | Headless Blog Extensions | Lightweight `widget.js` SDK, Tiptap Notion-style blocks (FAQ, CTA, Pros/Cons) | [`blogger-widgeta/`](./02-product-specifications-prds/blogger-widgeta/) |

---

## 🛠️ 03. Tools & Case Studies

* **GitHub Markdown Viewer** ([`03-tools-and-audits/markdown-renderer/index.html`](./03-tools-and-audits/markdown-renderer/index.html)): A zero-dependency, single-file HTML application simulating GitHub Primer design. Open directly in any browser to fetch and render raw markdown with syntax highlighting.
* **Technical Audits & Case Studies** ([`03-tools-and-audits/audits/`](./03-tools-and-audits/audits/)):
  * `static-site-audit-prompt.md`: A 50-point technical checklist covering performance, SEO, accessibility (WCAG), and responsive integrity.
  * `image-converter-audit-case-study.md`: A 247 KB real-world audit detailing memory management, WASM pipelines, and production hardening.

---

## 🎯 04. Universal AI Skills & MCP Servers

### AdSenseReady-AI (`04-skill/`)
A production-grade, 360-degree forensic Google AdSense readiness audit engine and native **Model Context Protocol (MCP)** server.

* **7-Pillar Evaluation Matrix**: Audits Legal & Trust Foundation, E-E-A-T Content Substance, Technical SEO, Navigation Architecture, Google Publisher Policies, Ad Ergonomics, and Structured Data.
* **Universal Cross-AI Compatibility**: Compatible with **Antigravity** (`SKILL.md`), **Claude Code** (`CLAUDE.md`), **Cursor** (`.cursorrules`), and **ChatGPT** (`prompts/`).
* **Native MCP Server** (`04-skill/src/mcp_server.py`): Enables Claude Desktop, Cursor, and Zed to invoke live website audits and policy checks.
* **Dynamic Policy Sync**: Weekly automated cron workflow (`.github/workflows/policy-sync.yml`) monitors official Google Search Central and AdSense RSS feeds to keep audit rules 100% evergreen.
* **Full Documentation**: See [`04-skill/README.md`](./04-skill/README.md).

---

## 🤝 Contributing

Contributions, enhancements, and new prompt archetypes are welcomed!
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/new-prompt`).
3. Ensure all filenames follow the kebab-case standard without special characters.
4. Open a Pull Request with a clear description of the prompt's purpose and benchmark results.

---

## 👤 Author & Ecosystem

**Oathan Rex**
- **Portfolio & Apps**: [https://oathanrex.github.io/](https://oathanrex.github.io/)
- **GitHub**: [@oathanrex](https://github.com/oathanrex)
- **CodePen**: [codepen.io/OathanRex](https://codepen.io/OathanRex)
- **Sponsor / Support**: [buymeacoffee.com/oathanrex](https://buymeacoffee.com/oathanrex)

---

<div align="center">
  <sub>Built with precision for the global developer and AI engineering community. © 2026 Oathan Rex.</sub>
</div>
