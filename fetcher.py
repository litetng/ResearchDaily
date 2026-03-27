import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import datetime
import re
import time
from typing import List, Dict, Any

# 预设你的专属核心研究阵列 (已应用 ArXiv 高级语法)
DEFAULT_KEYWORDS = [
    'all:"super-resolution" AND all:diffusion',
    '(all:multimodal OR all:"multi-modal")',
    '(all:"large language model" OR all:"LLM")'
]

def build_arxiv_query(keyword: str) -> str:
    """构建 ArXiv API 支持的查询字符串"""
    # 智能判断：如果你的关键词里已经写了冒号或括号（说明是高级语法）
    if ":" in keyword or "(" in keyword:
        # 把空格替换成 +，并且保护 + : ( ) 这四个符号不被错误转义
        return urllib.parse.quote(keyword.replace(" ", "+"), safe='+:()')
    
    # 如果只是随便输入了几个普通单词，再走自动拼接逻辑
    terms = keyword.split()
    query_parts = [f"all:{urllib.parse.quote(term)}" for term in terms]
    return "+AND+".join(query_parts)

def fetch_papers_for_keyword(keyword: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """针对单一关键词抓取论文，带有超时保护机制"""
    query = build_arxiv_query(keyword)
    url = f'http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}'
    
    try:
        # 【优化点】必须设置 timeout，防止 ArXiv 服务器卡死导致 APP 无响应
        response = urllib.request.urlopen(url, timeout=10)
        xml_data = response.read()
    except urllib.error.URLError as e:
        print(f"⚠️ 网络请求失败，关键词 '{keyword}': {e.reason}")
        return []
    except Exception as e:
        print(f"⚠️ 未知错误，关键词 '{keyword}': {e}")
        return []
        
    papers = []
    try:
        root = ET.fromstring(xml_data)
    except Exception as e:
        print(f"❌ XML 解析错误，关键词 '{keyword}': {e}")
        return papers
        
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    for entry in root.findall('atom:entry', ns):
        id_element = entry.find('atom:id', ns)
        if id_element is None:
            continue
            
        paper_id_url = id_element.text
        paper_id = paper_id_url.split('/abs/')[-1]
        
        # 【优化点】使用正则表达式清理标题和摘要中的多余空格和换行
        title_element = entry.find('atom:title', ns)
        title = re.sub(r'\s+', ' ', title_element.text).strip() if title_element is not None else "No Title"
        
        authors = []
        for author in entry.findall('atom:author', ns):
            author_name_elem = author.find('atom:name', ns)
            if author_name_elem is not None:
                authors.append(author_name_elem.text)
        authors_str = ", ".join(authors) if authors else "Unknown Authors"
        
        summary_element = entry.find('atom:summary', ns)
        abstract = re.sub(r'\s+', ' ', summary_element.text).strip() if summary_element is not None else ""
        
        published_element = entry.find('atom:published', ns)
        published_date_raw = published_element.text if published_element is not None else ""
        try:
            dt = datetime.datetime.strptime(published_date_raw, "%Y-%m-%dT%H:%M:%SZ")
            published_date = dt.strftime("%Y-%m-%d")
        except Exception:
            published_date = published_date_raw
            
        papers.append({
            'id': paper_id,
            'title': title,
            'authors': authors_str,
            'abstract': abstract,
            'url': paper_id_url,
            'published_date': published_date,
            'keyword': keyword
        })
        
    return papers

def fetch_all_papers(keywords: List[str] = None, max_results_per_keyword: int = 5) -> List[Dict[str, Any]]:
    """遍历所有关键词抓取论文，并在内存中进行临时去重"""
    if keywords is None:
        keywords = DEFAULT_KEYWORDS
        
    all_papers = []
    seen_ids = set()
    
    for kw in keywords:
        papers = fetch_papers_for_keyword(kw, max_results=max_results_per_keyword)
        for p in papers:
            if p['id'] not in seen_ids:
                seen_ids.add(p['id'])
                all_papers.append(p)
            else:
                # 若重复出现，将新的 keyword 追加到原有标签中
                for existing_p in all_papers:
                    if existing_p['id'] == p['id'] and kw not in existing_p.get('keyword', ''):
                        existing_p['keyword'] += f" | {kw}"
                        break
                        
        # 【必定要加的机制】严格遵守 ArXiv 官方规定：两次请求之间必须暂停 3 秒，否则会被服务器直接拒连导致抓取到 0 篇
        time.sleep(3)
                        
    # 按照发布日期倒序排序
    all_papers.sort(key=lambda x: x['published_date'], reverse=True)
    return all_papers

if __name__ == "__main__":
    print("🚀 正在启动学术雷达，为您抓取最新文献...\n")
    papers = fetch_all_papers(max_results_per_keyword=2)
    for p in papers:
        print(f"📅 [{p['published_date']}] {p['title']}")
        print(f"👥 作者: {p['authors']}")
        print(f"🔗 链接: {p['url']}")
        print("-" * 60)