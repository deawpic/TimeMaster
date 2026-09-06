---
name: avoid-ai-writing
description: "Audit and rewrite content to remove 21 categories of AI writing patterns and hollow clichés. Enforces human-grade, authentic academic and technical prose in both Thai and English."
category: style-discipline
risk: safe
tags: [writing, anti-ai, style-guide, academic-quality, humanize]
---

# Avoid AI Writing — Academic & Technical Edition

Detects and eliminates machine-generated writing patterns ("AI-isms") that degrade scientific papers, technical reports, and educational articles.

---

## 1. When to Activate This Skill

- Before finalizing any academic article, research report, or long-form documentation.
- When reviewing text to ensure it sounds like a senior metrologist or distributed systems professor rather than an LLM.
- Whenever auditing Thai or English content for robotic phrasing, unnecessary filler, or hollow enthusiasm.

---

## 2. The 21 AI Writing Patterns to Eliminate

| # | Pattern Category | What to Avoid | What to Do Instead |
|---|---|---|---|
| 1 | **Significance Inflation** | "serves as a testament to", "pivotal role", "game-changer", "revolutionary breakthrough" | State the factual impact directly with measurable metrics. |
| 2 | **The "Embark / Journey" Cliché** | "embarking on a transformative journey", "navigating the complex landscape" | Use direct verbs: "designing", "deploying", "analyzing", "evaluating". |
| 3 | **Copula Avoidance & Hollow Verbs** | "boasts exceptional accuracy", "features a robust architecture" | Use simple, direct verbs: "has", "delivers", "achieves", "runs". |
| 4 | **The "Tapestry / Mosaic" Trope** | "a rich tapestry of interconnected nodes", "a vibrant ecosystem of clocks" | Use technical terminology: "network topology", "hierarchical Stratum tier". |
| 5 | **Hollow Intensifiers** | "deeply fascinating", "remarkably crucial", "vital component" | Delete the intensifier; explain *why* it matters with physical laws. |
| 6 | **Synonym Cycling** | Alternating between "pivotal", "paramount", "imperative", "quintessential" in one section | Stick to consistent, clear engineering terminology. |
| 7 | **The "Rule of Three" Habit** | "efficiency, reliability, and scalability", "fast, secure, and robust" | List only the specific parameters actually measured or analyzed. |
| 8 | **Vague Attributions** | "experts agree", "industry leaders note", "scientists widely acknowledge" | Cite the exact paper, standard, or author (e.g. "BIPM CGPM Resolution 4 (2022)"). |
| 9 | **Generic Conclusions** | "In conclusion, the future of time is bright and full of possibilities..." | Conclude with concrete technical takeaways, open questions, or upcoming transitions (e.g. 2035 leap second phaseout). |
| 10| **Promotional Hype** | "unleash the true power of nanosecond synchronization" | State the operational boundary: "synchronizes within $\pm 10\ \text{ns}$". |
| 11| **Chatbot Artifacts** | "Sure! Let's dive in!", "Certainly! Here is the breakdown:" | Start directly with the technical thesis. |
| 12| **Formulaic Transition Words** | Excessive use of "Moreover,", "Furthermore,", "In addition,", "Delving deeper," | Use substantive contextual transitions that build on the previous argument. |
| 13| **Bullet Point Overuse in Prose** | Turning every explanation into 5 bullet points with bold keywords | Write continuous, flowing paragraphs with strong topic sentences. |
| 14| **Superficial "-ing" Analyses** | "highlighting the importance of...", "underscoring the necessity for..." | State the causal link: "Because oscillator drift exceeds $1\ \mu\text{s}$, the system must..." |
| 15| **False Ranges** | "from atomic clocks to everyday smartwatches" | Be technically specific: "from Cesium fountains at NMIs to quartz RTCs in edge gateways". |
| 16| **Inline-Header Fatigue** | Repeating `### 1. Introduction: The Dawn of...` every 5 lines | Use clean, conventional academic section numbering. |
| 17| **Cutoff Disclaimers** | "As of my last training update...", "It's important to keep in mind..." | Write definitively based on the grounded knowledge base (`kb/`). |
| 18| **Title Case Overkill in Body** | Capitalizing Every Word In Mid-Sentence Headings | Use standard sentence case or clean title case for major headings only. |
| 19| **Thai Robotic Translations** | "เป็นพยานถึงความสำคัญ", "นำทางภูมิทัศน์ที่ซับซ้อน", "ก้าวเข้าสู่การเดินทางอันทรงพลัง" | ใช้ภาษาเขียนทางวิชาการภาษาไทยที่กระชับ แม่นยำ เช่น "เป็นปัจจัยกำหนด", "วิเคราะห์โครงข่าย", "ดำเนินการปรับเทียบ" |
| 20| **Unearned Optimism** | "poised to revolutionize the global timing paradigm" | Analyze trade-offs, engineering hurdles, and implementation costs realistically. |
| 21| **Hedging Overdose** | "It might potentially be argued that perhaps..." | State the engineering thesis with measured academic certainty. |

---

## 3. Vocabulary Replacement Reference

```text
AVOID                     ───> PREFER
leverage / utilize        ───> use / employ / implement
robust                    ───> resilient / fault-tolerant / stable
crucial / pivotal         ───> essential / necessary / determinant
delve into / unpack       ───> examine / analyze / trace / calculate
testament to              ───> evidence of / demonstrates
tapestry / landscape      ───> architecture / domain / topology / state of the art
streamline                ───> simplify / accelerate / optimize
groundbreaking            ───> novel / high-precision / state-of-the-art
seamless                  ───> continuous / uninterrupted / low-jitter
```
