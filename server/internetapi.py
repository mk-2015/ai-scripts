import urllib.parse
import httpx
import re
from bs4 import BeautifulSoup

urlbar = "https://google.com"
useragent = "mcp-openaitools/1.0.0"
recentlyvisited = []

HTMLcache: str | None = None
VERBcache: str = ""
URLcache: str = ""

def convertHtmlToMarkdown(html_content: str) -> str:
    if not html_content:
        return ""
        
    soup = BeautifulSoup(html_content, "html.parser")
    
    for element in soup(["script", "style", "nav", "footer", "header", "form", "svg"]):
        element.decompose()
        
    for a in soup.find_all("a", href=True):
        a.replace_with(f" [{a.text.strip()}]({a['href']}) ")
        
    for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        level = int(heading.name[1])
        heading.replace_with(f"\n\n{'#' * level} {heading.text.strip()}\n")
        
    for li in soup.find_all("li"):
        li.replace_with(f"\n* {li.text.strip()}")

    text = soup.get_text()
    
    clean_text = re.sub(r'\n\s*\n', '\n\n', text)
    clean_text = re.sub(r' +', ' ', clean_text)
    
    return clean_text.strip()

def clearVisitHistory() -> str:
    global urlbar, recentlyvisited, HTMLcache, VERBcache, URLcache
    recentlyvisited = []
    urlbar = "https://google.com"
    HTMLcache = None
    VERBcache = ""
    URLcache = ""
    return "Browser state reset successfully."


async def selectUrlfromUrlBar(url: str, params: dict | str | None = None, headers: dict = {}) -> str:
    global urlbar, HTMLcache, VERBcache, URLcache
    try:
        merged_headers = {"User-Agent": useragent, **headers}

        if params:
            if isinstance(params, dict):
                encoded_params = urllib.parse.urlencode(params)
            else:
                encoded_params = str(params)
                
            joiner = "&" if "?" in url else "?"
            full_url = f"{url}{joiner}{encoded_params}"
        else:
            full_url = url

        async with httpx.AsyncClient(timeout=5.0, headers=merged_headers) as client:
            response = await client.head(full_url, follow_redirects=True)
            response.raise_for_status()
            
            if urlbar != full_url:
                HTMLcache = None
                VERBcache = ""
                URLcache = ""

            urlbar = full_url
            return f"URL successfully validated and set to: {urlbar}"

    except httpx.HTTPStatusError as e:
        return f"URL exists but returned an error status: {e.response.status_code}"
    except httpx.RequestError as e:
        return f"URL is bad or completely unreachable. Error: {e}"

async def gotoUrlInUrlBar(method: str = "GET", 
                         content: str = "None: Via MCP SERVER",
                         headers: dict = {}, 
                         caching: bool = True,
                         errinvalid_verb: bool = True) -> str:
    global VERBcache, HTMLcache, URLcache, recentlyvisited

    method = method.upper()
    
    merged_headers = {"User-Agent": useragent, **headers}
    
    if caching and HTMLcache is not None:
        if method == VERBcache and urlbar == URLcache:
            return f"[CACHED RESPONSE]\n{HTMLcache}"

    try:
        async with httpx.AsyncClient(timeout=5.0, headers=merged_headers) as client:
            if method == "GET":
                response = await client.get(urlbar, follow_redirects=True)
            elif method == "HEAD":
                response = await client.head(urlbar, follow_redirects=True)
                return f"HEAD request successful. Status: {response.status_code}, Headers: {dict(response.headers)}"
            elif method in ["PATCH", "PUT", "POST"]:
                response = await client.request(method, urlbar, follow_redirects=True, content=content)
            else:
                if errinvalid_verb:
                    raise ValueError(f"Error: Invalid HTTP verb '{method}' supplied.")
                else:
                    response = await client.get(urlbar, follow_redirects=True)

            response.raise_for_status()
            page_text = response.text[:150000]

    except Exception as e:
        return f"Failed to complete request on {urlbar}. Error: {str(e)}"

    VERBcache = method
    HTMLcache = page_text
    URLcache = urlbar

    recentlyvisited.append(urlbar)
    return page_text