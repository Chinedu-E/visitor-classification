import time
import random
import httpx
from bs4 import BeautifulSoup
import asyncio
from urllib.parse import urljoin

from bs4 import BeautifulSoup, SoupStrainer
import httpx
import asyncio
from urllib.parse import urljoin, urlparse
from typing import Set, Dict, Optional
import logging
from functools import lru_cache
import re
import json_fix


class WebsiteScraper:
    def __init__(self, url: str, max_concurrent: int = 10, timeout: int = 30):
        """
        Initialize the scraper with configurable parameters.
        
        Args:
            url: Base URL to scrape
            max_concurrent: Maximum number of concurrent requests
            timeout: Request timeout in seconds
        """
        self.url = url
        self.base_domain = urlparse(url).netloc
        self.home_page_text = ""
        self.links: Set[str] = set()
        self.link_texts: Dict[str, str] = {}
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.timeout = timeout
        self.session: Optional[httpx.AsyncClient] = None
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def __json__(self):
        return {
            'main_page_text': self.home_page_text,
            'links': self.links,
            'link_texts': self.link_texts,
            'url': self.url,
        }

    @lru_cache(maxsize=100)
    def _is_valid_url(self, url: str) -> bool:
        """Cache-enabled URL validation."""
        try:
            parsed = urlparse(url)
            return (
                parsed.netloc == self.base_domain and
                parsed.scheme in ('http', 'https') and
                not any(ext in parsed.path.lower() for ext in ('.pdf', '.jpg', '.png', '.gif'))
            )
        except Exception:
            return False

    async def _init_session(self):
        """Initialize HTTP session with optimized settings."""
        if not self.session:
            self.session = httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
                limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                    'Accept-Language': 'en-US,en;q=0.5',
                }
            )

    def _clean_text(self, text: str) -> str:
        """Efficiently clean and normalize text."""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    async def _fetch_page(self, url: str, parse_links: bool = False) -> tuple[str, set]:
        """
        Fetch and parse a single page with optimized BeautifulSoup parsing.
        Returns tuple of (cleaned_text, found_links).
        """
        new_links = set()
        
        async with self.semaphore:
            try:
                # Only parse links if needed (main page)
                parse_only = None if parse_links else SoupStrainer(['p', 'article', 'section', 'div', 'nav'])
                
                response = await self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser', parse_only=parse_only)

                # Remove unwanted elements
                for element in soup.select('script, style, footer, header, [class*="menu"]'):
                    element.decompose() 

                # Extract links if needed
                if parse_links:
                    for link in soup.find_all('a', href=True):
                        href = urljoin(self.url, link['href'])
                        if self._is_valid_url(href):
                            new_links.add(href)

                # Extract and clean text
                text = self._clean_text(soup.get_text())
                
                return text, new_links

            except Exception as e:
                self.logger.error(f"Error fetching {url}: {str(e)}")
                return "", set()

    async def scrape_main_page(self):
        """Scrape the main page and extract links."""
        await self._init_session()
        self.home_page_text, links = await self._fetch_page(self.url, parse_links=True)
        self.links = random.choices(list(links), k=min(len(links), self.max_concurrent))

    async def scrape_linked_pages(self):
        """Efficiently scrape all linked pages concurrently."""
        chunks = [list(self.links)[i:i + 10] for i in range(0, len(self.links), 10)]
        
        for chunk in chunks:
            tasks = [self._fetch_page(link) for link in chunk]
            results = await asyncio.gather(*tasks)
            
            for link, (text, _) in zip(chunk, results):
                if text:  # Only store if we got valid text
                    self.link_texts[link] = text

    async def scrape_all(self):
        """Scrape both the main page and all linked pages."""
        try:
            await self._init_session()
            await self.scrape_main_page()
            await self.scrape_linked_pages()
        finally:
            if self.session:
                await self.session.aclose()

    def get_main_page_text(self) -> str:
        """Access the main page's scraped text."""
        return self.home_page_text

    def get_link_texts(self) -> Dict[str, str]:
        """Access all scraped texts from linked pages."""
        return self.link_texts
        
        
        
if __name__ == '__main__':
    start_time = time.time()
    url = "https://www.apple.com/"
    scraper = WebsiteScraper(url)
    asyncio.run(scraper.scrape_all())
    print(scraper.get_main_page_text())
    print(scraper.get_link_texts())
    print(time.time() - start_time)