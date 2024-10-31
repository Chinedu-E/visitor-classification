import pytest
import httpx
from unittest.mock import AsyncMock, patch
from asgiref.wsgi import WsgiToAsgi
from src.app import app  

app = WsgiToAsgi(app)

@pytest.mark.asyncio
async def test_generate_content_endpoint():
    """
    Test the generate-content endpoint
    - Verify successful response
    - Check session ID generation
    - Validate returned links
    """
    url = "https://www.example.com"
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        with patch('src.app.WebsiteScraper') as MockScraper:
            # Mock the scraper to return predictable results
            mock_scraper_instance = AsyncMock()
            mock_scraper_instance.scrape_all = AsyncMock()
            mock_scraper_instance.links = [
                "https://www.example.com/page1",
                "https://www.example.com/page2"
            ]
            MockScraper.return_value = mock_scraper_instance

            response = await client.get(f"/generate-content/?url={url}")
            
            assert response.status_code == 200
            data = response.json()
            
            # Check for session ID
            assert "session_id" in data
            assert len(data["session_id"]) > 0
            
            # Verify links
            assert "links" in data
            assert len(data["links"]) > 0

@pytest.mark.asyncio
async def test_preview_image_endpoint():
    """
    Test the preview image endpoint
    - Verify successful image generation
    - Check S3 URL return
    """
    url = "https://www.example.com"
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        with patch('src.app.capture_screenshot') as mock_capture, \
             patch('src.app.upload_to_s3') as mock_upload:
            
            # Mock screenshot capture
            mock_capture.return_value = "/tmp/screenshot.png"
            
            # Mock S3 upload
            mock_upload.return_value = "https://bucket.s3.amazonaws.com/screenshot.png"

            response = await client.get(f"/preview-img/?url={url}")
            
            assert response.status_code == 200
            data = response.json()
            
            assert "image" in data
            assert data["image"].startswith("https://")


@pytest.mark.asyncio
async def test_invalid_url_handling():
    """
    Test handling of invalid URLs
    """
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Test invalid URL
        response = await client.get("/generate-content/?url=not-a-url")
        assert response.status_code == 400

        # Test empty URL
        response = await client.get("/generate-content/?url=")
        assert response.status_code == 400