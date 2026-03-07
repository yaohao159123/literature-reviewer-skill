"""
Paper Search — 自动检索相关论文
用法: python3 search_papers.py "query" [--limit 10] [--year 2024]
数据源: OpenAlex API (免费，无需API key)
功能:
  1. 关键词检索
  2. 按引用数排序
  3. 输出标题/作者/年份/DOI/引用数
  4. 可指定年份范围
"""
import sys
import json
import urllib.request
import urllib.parse
import argparse
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

OPENALEX_BASE = 'https://api.openalex.org/works'

def search(query, limit=10, year_from=None, year_to=None, sort='cited_by_count:desc'):
    """Search OpenAlex for papers"""
    params = {
        'search': query,
        'per_page': min(limit, 50),
        'sort': sort,
        'mailto': 'research@example.com',
    }
    
    filters = []
    if year_from:
        filters.append(f'from_publication_date:{year_from}-01-01')
    if year_to:
        filters.append(f'to_publication_date:{year_to}-12-31')
    if filters:
        params['filter'] = ','.join(filters)
    
    url = f'{OPENALEX_BASE}?{urllib.parse.urlencode(params)}'
    req = urllib.request.Request(url, headers={'User-Agent': 'PaperSearch/1.0'})
    
    try:
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        data = json.loads(resp.read().decode())
        return data.get('results', [])
    except Exception as e:
        print(f'Error: {e}')
        return []

def format_authors(authorships, max_authors=3):
    """Format author list"""
    authors = []
    for a in authorships[:max_authors]:
        name = a.get('author', {}).get('display_name', 'Unknown')
        authors.append(name)
    if len(authorships) > max_authors:
        authors.append('et al.')
    return ', '.join(authors)

def main():
    parser = argparse.ArgumentParser(description='Search scientific papers via OpenAlex')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--limit', '-n', type=int, default=10, help='Number of results')
    parser.add_argument('--year-from', '-f', type=int, help='From year')
    parser.add_argument('--year-to', '-t', type=int, help='To year')
    parser.add_argument('--recent', '-r', action='store_true', help='Sort by date (newest first)')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    args = parser.parse_args()
    
    sort = 'publication_date:desc' if args.recent else 'cited_by_count:desc'
    results = search(args.query, args.limit, args.year_from, args.year_to, sort)
    
    if not results:
        print('No results found.')
        return
    
    if args.json:
        for r in results:
            print(json.dumps({
                'title': r.get('title', ''),
                'doi': r.get('doi', ''),
                'year': r.get('publication_year', ''),
                'citations': r.get('cited_by_count', 0),
                'authors': format_authors(r.get('authorships', [])),
                'journal': r.get('primary_location', {}).get('source', {}).get('display_name', ''),
            }))
        return
    
    print(f'Found {len(results)} results for: "{args.query}"\n')
    
    for i, r in enumerate(results, 1):
        title = r.get('title', 'No title')
        doi = r.get('doi', 'No DOI')
        year = r.get('publication_year', '?')
        citations = r.get('cited_by_count', 0)
        authors = format_authors(r.get('authorships', []))
        journal = r.get('primary_location', {})
        if journal:
            journal = journal.get('source', {})
            if journal:
                journal = journal.get('display_name', '')
            else:
                journal = ''
        else:
            journal = ''
        
        oa = '🔓' if r.get('open_access', {}).get('is_oa', False) else '🔒'
        
        print(f'{i:>2}. [{year}] {title}')
        print(f'    {authors}')
        print(f'    {journal} | Citations: {citations} {oa}')
        if doi:
            print(f'    {doi}')
        print()

if __name__ == '__main__':
    main()
