---
name: papers-skill
description: "Literature research assistant for chronometry, atomic physics, network synchronization, and distributed consensus. Searches Semantic Scholar (200M+ papers), queries arXiv, inspects citation graphs, downloads open-access PDFs, and extracts text."
category: research
risk: safe
tags: [research, academic, papers, citations, arxiv, semantic-scholar, chronometry]
---

# Papers Skill — Chronometry & Distributed Systems Literature

Enables the agent to conduct deep academic literature reviews, find state-of-the-art papers, inspect citation impact, and download arXiv preprints.

---

## 1. When to Activate This Skill

- When researching published literature on time and frequency standards (e.g. Optical Lattice Clocks, Cesium Fountain accuracy, Hydrogen Maser phase noise).
- When investigating distributed systems clock research (e.g. Spanner TrueTime, Hybrid Logical Clocks, Byzantine Fault Tolerant clock synchronization).
- When looking up seminal papers (e.g. Leslie Lamport 1978 "Time, Clocks, and the Ordering of Events in a Distributed System", Corbett et al. 2012 "Spanner: Google's Globally-Distributed Database", David L. Mills on NTP RFCs).
- When preparing bibliography and citation sections for academic articles.

---

## 2. CLI Execution & Subcommands

Run the bundled Python CLI located at `.agents/skills/papers-skill/scripts/papers.py`:

```bash
# 1. Search Semantic Scholar for papers by topic
python3 .agents/skills/papers-skill/scripts/papers.py search --query "optical lattice clock strontium frequency standard" --limit 5

# 2. Search arXiv preprints for cutting-edge papers
python3 .agents/skills/papers-skill/scripts/papers.py arxiv --query "ti:TrueTime OR ti:clock synchronization distributed systems" --limit 5

# 3. Get detailed paper metadata and abstract by DOI or arXiv ID
python3 .agents/skills/papers-skill/scripts/papers.py paper --id "arXiv:1206.3385"

# 4. Inspect papers citing a foundational work (Impact Analysis)
python3 .agents/skills/papers-skill/scripts/papers.py citations --id "DOI:10.1145/359545.359563" --limit 10

# 5. Inspect papers cited by a work (Reference Graph)
python3 .agents/skills/papers-skill/scripts/papers.py references --id "arXiv:1206.3385" --limit 10

# 6. Download arXiv PDF and extract text for deep reading
python3 .agents/skills/papers-skill/scripts/papers.py download --id "arXiv:1206.3385" --output-dir reports/papers/
```

---

## 3. Literature Synthesis Workflow

1. **Query Formulation**: Translate the user's research topic into boolean keywords (e.g. `"PTP" AND "boundary clock" AND "jitter"`).
2. **Scan & Filter**: Retrieve titles, abstracts, and publication years to identify high-relevance candidates.
3. **Reference Mapping**: Trace forward citations (who built upon this work) and backward references (what foundational theories were used).
4. **Citation Export**: Format the reference in standard BibTeX, IEEE, or APA format for inclusion in academic manuscripts.
