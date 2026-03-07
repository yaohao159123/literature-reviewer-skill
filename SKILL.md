---
name: literature-reviewer
description: "Three-tier academic literature review system: Zotero local search → OpenAlex global search → CrossRef citation verification. Includes Obsidian knowledge graph integration for backlink-based literature discovery."
metadata:
  openclaw:
    emoji: "📚"
    requires:
      tools: ["exec"]
    optional:
      - "Zotero desktop running (port 23119) for local search"
      - "Obsidian 1.12+ CLI for knowledge graph queries"
      - "Better BibTeX Zotero plugin for citekey support"
allowed-tools: ["exec", "read", "write"]
---

# Literature Reviewer Skill

A three-tier academic literature review pipeline for AI research assistants.

## Architecture

```
Tier 1: Zotero Local Search (fast, your curated library)
  ↓ not found?
Tier 2: OpenAlex Global Search (free, 250M+ works)
  ↓ paper found, need to verify?
Tier 3: CrossRef Citation Verification (DOI validation)
```

**Bonus**: Obsidian 1.12 CLI integration for knowledge graph traversal (backlinks, orphans, outlines).

## Tools

### 1. Zotero Local Search (`zotero_search.py`)
Search your local Zotero library via the Better BibTeX JSON-RPC API.

```bash
python3 zotero_search.py "microwave heating"
python3 zotero_search.py "EAFD" --limit 20
python3 zotero_search.py "reduction" --tag Q1
python3 zotero_search.py "biomass" --bibtex    # output BibTeX
python3 zotero_search.py "zinc" --doi-only     # DOIs only
python3 zotero_search.py "pyrolysis" --json    # JSON output
```

**Requires**: Zotero desktop running (port 23119), Better BibTeX plugin.

### 2. OpenAlex Paper Search (`search_papers.py`)
Search 250M+ academic works via OpenAlex (free, no API key).

```bash
python3 search_papers.py "microwave hydrogen reduction"
python3 search_papers.py "EAFD zinc removal" --limit 20
python3 search_papers.py "biomass pyrolysis" --recent          # sort by date
python3 search_papers.py "dielectric properties" --year-from 2023
python3 search_papers.py "kinetics activation energy" --json
```

**Output**: title, authors, year, journal, DOI, citation count.

### 3. Citation Verification (`verify_references.py`)
Verify all citations in a manuscript against CrossRef.

```bash
python3 verify_references.py paper.md
python3 verify_references.py manuscript.docx
```

**Output**:
- ✅ Verified (exact DOI match)
- 🔍 Auto-matched (found via CrossRef search)
- ❌ Failed (DOI invalid)
- ⚠️ Unmatched (couldn't find in CrossRef)

### 4. Obsidian Knowledge Graph (CLI)
Use Obsidian 1.12+ CLI for graph-based literature discovery.

```bash
# Vault overview (133x faster than file traversal)
obsidian vault="Obsidian Vault" vault

# Find all papers linked to a specific paper
obsidian vault="Obsidian Vault" backlinks file="xiongRecentDevelopmentsRemoval2024"

# Get paper outline without reading full file (~11x token savings)
obsidian vault="Obsidian Vault" outline file="微波动力学耦合框架"

# Search across all literature notes
obsidian vault="Obsidian Vault" search query="microwave kinetics"

# Find orphan papers (no backlinks — potentially underused)
obsidian vault="Obsidian Vault" orphans

# Find dead-end papers (no outgoing links)
obsidian vault="Obsidian Vault" deadends

# Find broken links
obsidian vault="Obsidian Vault" unresolved

# Tag statistics
obsidian vault="Obsidian Vault" tags counts
```

**Note**: Obsidian CLI path on macOS: `/Applications/Obsidian.app/Contents/MacOS/Obsidian`

## Workflow: Writing a Paper

When writing a paper and needing references:

1. **Search Zotero first** (your curated library):
   ```bash
   python3 zotero_search.py "your topic"
   ```

2. **Check Obsidian graph** for related papers via backlinks:
   ```bash
   obsidian vault="Obsidian Vault" backlinks file="relevantPaper2024"
   ```

3. **If not found locally**, search OpenAlex:
   ```bash
   python3 search_papers.py "your topic" --recent
   ```

4. **After writing**, verify all citations:
   ```bash
   python3 verify_references.py your_paper.md
   ```

## Workflow: Literature Review

1. **Define scope** with OpenAlex search + Zotero tag filtering
2. **Map connections** using Obsidian backlinks and graph view
3. **Identify gaps** using orphans (unlinked papers) and unresolved links
4. **Verify integrity** with citation verification

## Token Efficiency (vs traditional file reading)

| Operation | Traditional | With Skill | Savings |
|-----------|-------------|------------|---------|
| Vault overview | 45KB (traverse) | 351B (CLI) | ~130x |
| Paper search | 47KB (grep) | 8.7KB (CLI) | ~5x |
| File outline | 63KB (read all) | 5.6KB (CLI) | ~11x |
| Orphan detection | Custom script | 1 command | ∞ |

## Setup Requirements

1. **Zotero** desktop with Better BibTeX plugin (for Tier 1)
2. **Python 3** with standard library only (no pip installs needed)
3. **Obsidian 1.12+** with CLI enabled (Settings → General → Command Line Interface)
4. Literature notes imported to Obsidian Zotero folder (use `zotero_to_obsidian.py` for batch import)

## Workflow: Automated Multi-Day Literature Review (Proven Pipeline)

This pipeline was battle-tested for an EAFD microwave hydrogen reduction review (72 papers in 3 days).

### Setup
1. Define topic, keywords, and search criteria in `TASK.md`
2. Search and curate paper list → `papers_list.md` (with DOI/URLs)
3. Schedule cron jobs for batch reading (3 batches/day × 9 papers each)

### Daily Schedule (per day)
```
09:00 — Batch 1 (papers 1-9): Deep read, save to dayN_notes.md
14:00 — Batch 2 (papers 10-18): Deep read, append to dayN_notes.md  
19:00 — Batch 3 (papers 19-27): Deep read, append to dayN_notes.md
21:00 — Daily summary: Summarize findings, notify user
```

### Per-Paper Note Template
For each paper, record:
- **Title / Authors / Year / Journal / DOI**
- **Research question**: What problem does it solve?
- **Method**: Experimental setup, parameters, conditions
- **Key findings**: Quantitative results with numbers
- **Limitations**: What's missing or weak?
- **Relevance**: How does it connect to your research?

### Output Structure
```
literature_review/
├── TASK.md              # Topic, keywords, timeline
├── papers_list.md       # Full paper list with DOIs (72+ papers)
├── day1_notes.md        # Day 1 detailed notes
├── day2_notes.md        # Day 2 detailed notes  
├── day3_notes.md        # Day 3 detailed notes
├── review_batch1-6.md   # Batch review notes
├── day1_summary.md      # Daily summaries
├── day2_summary.md
└── REVIEW.md            # Final synthesized review (~10,000 words)
```

### Final Review Structure
1. Research Background & Significance
2. Current Research Status (domestic & international)
3. Technical Route Comparison (parameters, efficiency, energy)
4. Research Gaps & Future Directions
5. References (all verified via CrossRef)

### Cron Job Template
```json
{
  "name": "Literature Review Day1 Batch1",
  "schedule": {"kind": "at", "at": "2026-01-29T09:00:00+02:00"},
  "payload": {
    "kind": "agentTurn",
    "message": "Read papers 1-9 from papers_list.md. For each paper: fetch via DOI/URL, extract key info, save detailed notes to day1_notes.md"
  },
  "sessionTarget": "isolated"
}
```

## Zotero → Obsidian Batch Import

Import all Zotero papers into Obsidian with auto-generated wikilinks:

1. **Batch import** (`zotero_to_obsidian.py`): Fetches all items from Zotero via Better BibTeX JSON-RPC, creates Obsidian notes with frontmatter (citekey, authors, year, journal, DOI, tags)
2. **Auto wikilinks** (`zotero_wikilinks.py`): Builds relationship graph — links papers by shared authors and shared topic keywords (≥2 keyword overlap from 150+ topic clusters)

Result: 392 literature notes with "Related Papers" sections containing `[[wikilinks]]`, enabling Obsidian graph view for citation network visualization.

## Files

- `zotero_search.py` — Tier 1: Local Zotero search
- `search_papers.py` — Tier 2: OpenAlex global search
- `verify_references.py` — Tier 3: CrossRef citation verification
- `SKILL.md` — This file

## Example Output

The EAFD microwave review produced:
- 72 papers deeply read across 3 days
- 392 Zotero papers imported to Obsidian with wikilinks
- 9,060-word final review with 23 verified citations
- Chinese mind map (137 nodes) + citation network
- Copied to Obsidian vault for permanent knowledge graph integration
