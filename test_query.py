import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

keywords = [
    'all:"super-resolution" AND all:diffusion',
    '(all:multimodal OR all:"multi-modal")',
    '(all:"large language model" OR all:"LLM")'
]

for keyword in keywords:
    query = urllib.parse.quote(keyword.replace(" ", "+"), safe='+:()')
    url = f'http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results=2'
    try:
        resp = urllib.request.urlopen(url, timeout=10)
        xml_data = resp.read()
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', ns)
        print(f"Keyword: {keyword}")
        print(f"URL: {url}")
        print(f"Found: {len(entries)}\n")
    except Exception as e:
        print(f"Keyword: {keyword} -> Error: {e}")
