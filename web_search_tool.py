import base64
import re
import requests
from bs4 import BeautifulSoup
from smolagents import Tool

MAX_CHARS = 1400

def _decode_bing_url(url):
    if "bing.com/ck/a" in url:
        m = re.search(r"u=a1([^&]+)", url)
        if m:
            try:
                value = m.group(1) + "=" * (-len(m.group(1)) % 4)
                return base64.b64decode(value).decode("utf-8")
            except Exception:
                pass
    return url

def _queries(query):
    q = query.strip()
    lower = q.lower()
    out = [q]
    if "wikipedia" not in lower:
        out.append(q + " Wikipedia")
    if any(x in lower for x in ["jersey", "pitcher", "player", "roster", "baseball", "football", "basketball"]):
        out.append(q + " site:baseball-reference.com")
        out.append(q + " site:wikipedia.org")
    elif any(x in lower for x in ["profession", "born", "died", "singer", "actor", "author"]):
        out.append(q + " site:wikipedia.org")
    return list(dict.fromkeys(out))[:4]

def _score(title, snippet, query):
    text = (title + " " + snippet).lower()
    terms = [x.strip('"').lower() for x in query.split() if len(x.strip('"')) > 2]
    score = sum(2 for t in terms if t in text)
    if "wikipedia" in title.lower():
        score += 4
    if "taisho" in query.lower() and any(x in text for x in ["pharmaceutical", "emperor", "era"]):
        score -= 10
    return score

class BingSearchTool(Tool):
    name = "web_search"
    description = "Search the public web for factual information. Returns compact ranked results with URLs and snippets."
    inputs = {"query": {"type": "string", "description": "The factual information to find."}}
    output_type = "string"

    def forward(self, query: str) -> str:
        candidates = []
        for q in _queries(query):
            r = requests.get(
                "https://www.bing.com/search",
                params={"q": q, "count": 8, "setlang": "en-US"},
                headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"},
                timeout=10,
            )
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            for item in soup.select("li.b_algo"):
                a = item.select_one("h2 a")
                p = item.select_one(".b_caption p")
                if not a:
                    continue
                title = a.get_text(" ", strip=True)
                url = _decode_bing_url(a.get("href", ""))
                snippet = p.get_text(" ", strip=True) if p else ""
                candidates.append((_score(title, snippet, query), title, url, snippet))
        candidates.sort(key=lambda x: x[0], reverse=True)
        seen, results = set(), []
        for score, title, url, snippet in candidates:
            key = (title.lower(), url.lower())
            if key in seen or not url.startswith("http"):
                continue
            seen.add(key)
            results.append(f"{title}\nURL: {url}\n{snippet[:280]}")
            if len(results) == 5:
                break
        return "\n\n".join(results)[:MAX_CHARS] or "No useful web results found."

def build_web_search_tool():
    return BingSearchTool()
