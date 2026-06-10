# Literature Reviewer Skill

A lightweight research-assistant skill for finding, checking, and organizing academic references. It combines a local Zotero-first workflow with public metadata search and citation verification.

## What It Does

- Searches a local Zotero library through the Better BibTeX JSON-RPC API.
- Falls back to OpenAlex for global paper discovery when a paper is not in Zotero.
- Verifies DOI and URL references in Markdown manuscripts through CrossRef and HTTP checks.
- Documents an optional Obsidian knowledge-graph workflow for backlink and orphan-paper discovery.

## Repository Contents

| File | Purpose |
| --- | --- |
| `SKILL.md` | Skill instructions for OpenClaw / agent runtimes. |
| `zotero_search.py` | Local Zotero search helper. |
| `search_papers.py` | OpenAlex paper search helper. |
| `verify_references.py` | CrossRef and URL reference verifier. |

## Quick Start

Clone the repository and run the scripts with Python 3. No package installation is required for the default helpers because they use the Python standard library.

```bash
git clone https://github.com/yaohao159123/literature-reviewer-skill.git
cd literature-reviewer-skill
python3 search_papers.py "microwave hydrogen reduction" --limit 5
```

For local Zotero search, start Zotero Desktop and install Better BibTeX first:

```bash
python3 zotero_search.py "biomass pyrolysis" --limit 10
python3 zotero_search.py "zinc" --doi-only
python3 zotero_search.py "reduction" --bibtex
```

To verify references in a Markdown manuscript:

```bash
python3 verify_references.py paper.md
```

## Agent Workflow

Use `SKILL.md` as the runtime-facing instruction file. A typical review loop is:

1. Search Zotero for curated local papers.
2. Inspect Obsidian backlinks or related notes when available.
3. Search OpenAlex for missing or recent papers.
4. Verify manuscript references with CrossRef before finalizing citations.

## Requirements

- Python 3.9+ recommended.
- Zotero Desktop is optional and only required for `zotero_search.py`.
- Better BibTeX is optional and only required for Zotero BibTeX export / citekeys.
- Internet access is required for OpenAlex and CrossRef helpers.

## Privacy Notes

- `zotero_search.py` queries the local Zotero API on `localhost:23119`.
- `search_papers.py` sends search terms to OpenAlex.
- `verify_references.py` sends extracted citation text or DOI values to CrossRef and may probe URLs found in a manuscript.
- Do not run verification on private manuscripts unless you are comfortable sending citation metadata to those services.

## Maintenance

This project is maintained as a practical research workflow tool. Issues and pull requests that improve reliability, citation parsing, metadata quality, or agent-runtime compatibility are welcome.

## License

MIT License. See `LICENSE`.
