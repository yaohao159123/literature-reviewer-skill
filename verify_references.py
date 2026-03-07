"""
Reference Verifier — 验证论文引用的DOI/URL真实性
用法: python3 verify_references.py <markdown_file>
功能:
  1. 从markdown中提取所有引用条目
  2. 验证DOI是否存在（via CrossRef API）
  3. 验证URL是否可访问
  4. 输出验证报告
"""
import re
import sys
import json
import urllib.request
import urllib.error
import time
import ssl

# 忽略SSL证书问题
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def extract_references(filepath):
    """从markdown文件提取引用列表"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 匹配 [数字] 开头的引用行
    refs = re.findall(r'\[(\d+)\]\s*(.+?)(?=\n\[|\n\n|\Z)', text, re.DOTALL)
    return refs

def extract_doi(text):
    """从引用文本中提取DOI"""
    patterns = [
        r'(?:doi[:\s]*|https?://doi\.org/)(10\.\d{4,}/[^\s\]]+)',
        r'(10\.\d{4,}/[^\s\],]+)',
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            doi = m.group(1).rstrip('.')
            return doi
    return None

def lookup_doi_crossref(text):
    """通过CrossRef查询文献信息来找DOI"""
    # 提取作者和标题的简短查询
    query = re.sub(r'[\[\]\(\)]', '', text)[:120]
    query = urllib.parse.quote(query)
    url = f'https://api.crossref.org/works?query={query}&rows=1'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'PaperVerifier/1.0 (mailto:research@example.com)'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=10, context=ctx)
        data = json.loads(resp.read().decode())
        items = data.get('message', {}).get('items', [])
        if items:
            doi = items[0].get('DOI', '')
            title = items[0].get('title', [''])[0][:60]
            score = items[0].get('score', 0)
            return doi, title, score
    except:
        pass
    return None, None, 0

def extract_urls(text):
    """从引用文本中提取URL"""
    urls = re.findall(r'https?://[^\s\]\)]+', text)
    return urls

def verify_doi(doi):
    """通过CrossRef API验证DOI"""
    url = f'https://api.crossref.org/works/{doi}'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'PaperVerifier/1.0 (mailto:research@example.com)'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=10, context=ctx)
        data = json.loads(resp.read().decode())
        title = data.get('message', {}).get('title', [''])[0]
        return True, title[:80]
    except urllib.error.HTTPError as e:
        return False, f'HTTP {e.code}'
    except Exception as e:
        return False, str(e)[:50]

def verify_url(url):
    """验证URL是否可访问"""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0'
    })
    req.method = 'HEAD'
    try:
        resp = urllib.request.urlopen(req, timeout=10, context=ctx)
        return True, resp.status
    except urllib.error.HTTPError as e:
        if e.code in [403, 405]:  # some sites block HEAD
            return True, f'{e.code} (blocked HEAD, likely ok)'
        return False, f'HTTP {e.code}'
    except Exception as e:
        return False, str(e)[:50]

def main():
    if len(sys.argv) < 2:
        print('用法: python3 verify_references.py <markdown_file>')
        sys.exit(1)
    
    filepath = sys.argv[1]
    refs = extract_references(filepath)
    
    if not refs:
        print('未找到引用条目。确保格式为 [1] Author, Title...')
        sys.exit(1)
    
    print(f'找到 {len(refs)} 条引用，开始验证...\n')
    print(f'{"#":>3} {"DOI":>5} {"URL":>5}  详情')
    print('-' * 70)
    
    ok_count = 0
    fail_count = 0
    no_id_count = 0
    
    for num, text in refs:
        text_clean = text.strip().replace('\n', ' ')
        doi = extract_doi(text_clean)
        urls = extract_urls(text_clean)
        
        doi_status = '—'
        url_status = '—'
        detail = text_clean[:60]
        
        if doi:
            time.sleep(0.3)
            valid, info = verify_doi(doi)
            doi_status = '✅' if valid else '❌'
            if valid:
                ok_count += 1
            else:
                fail_count += 1
                detail = f'DOI失败: {doi} ({info})'
        elif urls:
            time.sleep(0.2)
            valid, info = verify_url(urls[0])
            url_status = '✅' if valid else '❌'
            if valid:
                ok_count += 1
            else:
                fail_count += 1
                detail = f'URL失败: {urls[0][:40]} ({info})'
        else:
            # 没有DOI/URL，尝试CrossRef查找
            time.sleep(0.5)
            found_doi, found_title, score = lookup_doi_crossref(text_clean)
            if found_doi and score > 50:
                valid, info = verify_doi(found_doi)
                doi_status = '🔍' if valid else '❌'
                if valid:
                    ok_count += 1
                    detail = f'自动匹配: {found_doi} → {found_title}'
                else:
                    fail_count += 1
                    detail = f'匹配但验证失败: {found_doi}'
            else:
                no_id_count += 1
                detail = f'⚠️ 未能匹配: {text_clean[:50]}'
        
        print(f'[{num:>2}] {doi_status:>3} {url_status:>3}  {detail}')
    
    print('\n' + '=' * 70)
    print(f'总计: {len(refs)} 条引用')
    print(f'  ✅ 验证通过: {ok_count}')
    print(f'  ❌ 验证失败: {fail_count}')
    print(f'  ⚠️ 无DOI/URL: {no_id_count}')

if __name__ == '__main__':
    main()
