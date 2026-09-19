import requests
from bs4 import BeautifulSoup
from smolagents import Tool

class WebpageFetchTool(Tool):
    name = "webpage_fetch"
    description = "Fetch a webpage URL and extract a compact text version."
    inputs = {"url": {"type": "string", "description": "The webpage URL."}}
    output_type = "string"

    def forward(self, url: str) -> str:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script","style","nav","header","footer","aside","form","noscript"]):
            tag.decompose()
        return " ".join(soup.stripped_strings)[:1800]

def build_webpage_fetch_tool():
    return WebpageFetchTool()
