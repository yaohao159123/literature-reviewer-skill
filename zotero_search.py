"""
Zotero Local Search — 搜索本地Zotero文献库
用法: python3 zotero_search.py "keyword" [--limit 10] [--tag Q1]
功能:
  1. 搜索本地Zotero库（标题/作者/摘要）
  2. 输出标题/作者/DOI/期刊/年份/标签
  3. 支持按标签筛选
  4. 需要Zotero桌面版运行（本地API端口23119）
"""
import sys
import json
import urllib.request
import urllib.parse
import argparse

ZOTERO_BASE = 'http://localhost:23119/api/users/0'

def get_items(query=None, tag=None, limit=20):
    """从Zotero本地API获取文献"""
    params = {
        'limit': limit,
        'sort': 'dateModified',
        'direction': 'desc',
        'itemType': 'journalArticle || conferencePaper || book || bookSection || thesis',
    }
    if query:
        params['q'] = query
    if tag:
        params['tag'] = tag
    
    url = f'{ZOTERO_BASE}/items?{urllib.parse.urlencode(params)}'
    try:
        resp = urllib.request.urlopen(url, timeout=5)
        return json.loads(resp.read().decode())
    except Exception as e:
        print(f'Error: {e}')
        print('确保Zotero桌面版正在运行')
        return []

def format_item(item, index):
    """格式化单条文献"""
    d = item.get('data', {})
    title = d.get('title', 'No title')
    doi = d.get('DOI', '')
    year = d.get('date', '')[:4]
    journal = d.get('publicationTitle', d.get('bookTitle', ''))
    tags = [t['tag'] for t in d.get('tags', [])]
    key = d.get('citationKey', d.get('key', ''))
    
    creators = d.get('creators', [])
    authors = []
    for c in creators[:3]:
        name = f"{c.get('lastName', '')}"
        if name:
            authors.append(name)
    if len(creators) > 3:
        authors.append('et al.')
    author_str = ', '.join(authors)
    
    lines = [f'{index:>2}. [{year}] {title}']
    lines.append(f'    {author_str} | {journal}')
    if doi:
        lines.append(f'    DOI: {doi}')
    if tags:
        lines.append(f'    Tags: {", ".join(tags[:5])}')
    lines.append(f'    Key: {key}')
    return '\n'.join(lines)

def export_bibtex(item):
    """导出单条文献的BibTeX"""
    key = item.get('data', {}).get('key', '')
    url = f'{ZOTERO_BASE}/items/{key}?format=bibtex'
    try:
        resp = urllib.request.urlopen(url, timeout=5)
        return resp.read().decode()
    except:
        return None

def main():
    parser = argparse.ArgumentParser(description='Search local Zotero library')
    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('--limit', '-n', type=int, default=10)
    parser.add_argument('--tag', '-t', help='Filter by tag (e.g. Q1)')
    parser.add_argument('--bibtex', '-b', action='store_true', help='Export BibTeX')
    parser.add_argument('--json', '-j', action='store_true', help='JSON output')
    parser.add_argument('--doi-only', action='store_true', help='Only show DOIs')
    parser.add_argument('--count', action='store_true', help='Just count items')
    args = parser.parse_args()
    
    items = get_items(args.query, args.tag, args.limit)
    
    if not items:
        print('未找到文献。' if args.query else '无法连接Zotero。')
        return
    
    if args.count:
        print(f'{len(items)} items')
        return
    
    if args.json:
        for item in items:
            d = item.get('data', {})
            print(json.dumps({
                'title': d.get('title', ''),
                'doi': d.get('DOI', ''),
                'year': d.get('date', '')[:4],
                'journal': d.get('publicationTitle', ''),
                'key': d.get('citationKey', d.get('key', '')),
            }))
        return
    
    if args.bibtex:
        for item in items:
            bib = export_bibtex(item)
            if bib:
                print(bib)
        return
    
    if args.doi_only:
        for item in items:
            doi = item.get('data', {}).get('DOI', '')
            if doi:
                print(doi)
        return
    
    print(f'Zotero本地库搜索: "{args.query or "all"}" ({len(items)} results)\n')
    for i, item in enumerate(items, 1):
        print(format_item(item, i))
        print()

if __name__ == '__main__':
    main()
