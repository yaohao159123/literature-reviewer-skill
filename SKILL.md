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

## Files

- `zotero_search.py` — Tier 1: Local Zotero search
- `search_papers.py` — Tier 2: OpenAlex global search
- `verify_references.py` — Tier 3: CrossRef citation verification
- `SKILL.md` — This file
