# Contributing

Thanks for improving Literature Reviewer Skill. This project is intentionally small and standard-library-first.

## Good First Contributions

- Improve citation parsing coverage in `verify_references.py`.
- Add safer API error handling or clearer CLI messages.
- Improve documentation for Zotero, Better BibTeX, or Obsidian workflows.
- Add tests for DOI extraction and reference parsing edge cases.

## Development Guidelines

- Keep scripts runnable with Python 3 and standard-library dependencies when possible.
- Avoid committing private manuscript text, Zotero exports, API keys, or local Obsidian vault paths.
- Prefer small, focused pull requests with a short reproduction or sample command.
- If a change sends data to a remote service, document what is sent.

## Manual Checks

Run the helper you changed with a safe public query or minimal fixture before opening a PR:

```bash
python3 search_papers.py --help
python3 zotero_search.py --help
printf '[1] Example title. doi:10.1038/nphys1170\n' > /tmp/lit-reviewer-smoke.md
python3 verify_references.py /tmp/lit-reviewer-smoke.md
```
