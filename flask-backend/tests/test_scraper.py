import pytest
import asyncio
from src.utils.scraper import WebsiteScraper

@pytest.mark.asyncio
async def test_scraper_initialization():
    """
    Test WebsiteScraper initialization
    """
    url = "https://www.example.com"
    scraper = WebsiteScraper(url)
    
    assert scraper.url == url
    assert scraper.base_domain == "www.example.com"
    assert scraper.max_concurrent == 10
    assert scraper.timeout == 30

@pytest.mark.asyncio
async def test_url_validation():
    """
    Test URL validation method
    """
    scraper = WebsiteScraper("https://www.example.com")
    
    # Valid URLs
    assert scraper._is_valid_url("https://www.example.com/page") == True
    assert scraper._is_valid_url("http://www.example.com/subpage") == True
    
    # Invalid URLs
    assert scraper._is_valid_url("https://another-site.com") == False
    assert scraper._is_valid_url("https://www.example.com/page.pdf") == False
    assert scraper._is_valid_url("ftp://www.example.com") == False

@pytest.mark.asyncio
async def test_scrape_main_page():
    """
    Test main page scraping
    Note: This uses a real network call, so might need mocking in CI
    """
    url = "https://www.python.org"
    scraper = WebsiteScraper(url)
    
    await scraper.scrape_main_page()
    
    assert scraper.home_page_text != ""
    assert len(scraper.links) > 0
    assert all(link.startswith("http") for link in scraper.links)

@pytest.mark.asyncio
async def test_scrape_linked_pages():
    """
    Test linked pages scraping
    """
    url = "https://www.python.org"
    scraper = WebsiteScraper(url)
    
    # First scrape the main page to get links
    await scraper.scrape_main_page()
    
    # Then scrape linked pages
    await scraper.scrape_linked_pages()
    
    assert len(scraper.link_texts) > 0
    assert all(len(text) > 0 for text in scraper.link_texts.values())

@pytest.mark.asyncio
async def test_text_cleaning():
    """
    Test text cleaning method
    """
    scraper = WebsiteScraper("https://www.example.com")
    
    dirty_text = "   Multiple   \n\n  Whitespace   Test   "
    cleaned_text = scraper._clean_text(dirty_text)
    
    assert cleaned_text == "Multiple Whitespace Test"