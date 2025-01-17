import pytest
from unittest.mock import patch, Mock
import os
import json
from src.scraping.site_scraper import scrape_website

@pytest.fixture
def mock_html():
    """Fixture to provide mock HTML content."""
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Main Header</h1>
            <h2>Sub Header</h2>
            <p>First paragraph.</p>
            <p>Second paragraph.</p>
        </body>
    </html>
    """

def test_scrape_website(mock_html, tmp_path):
    """Test scrape_website function."""
    url = "https://example.com"
    output_file = tmp_path / "website_content.json"

    # Mock requests.get to return the mock HTML
    with patch("src.scraping.site_scraper.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = mock_html
        mock_get.return_value = mock_response

        scrape_website(url, output_file=str(output_file))

    # Check if output file is created
    assert os.path.exists(output_file)

    # Validate scraped content
    with open(output_file, "r", encoding="utf-8") as f:
        scraped_content = json.load(f)
    
    assert scraped_content["url"] == url
    assert scraped_content["headers"] == ["Main Header", "Sub Header"]
    assert scraped_content["paragraphs"] == ["First paragraph.", "Second paragraph."]

def test_scrape_website_http_error():
    """Test scrape_website function with HTTP error."""
    url = "https://example.com"
    with patch("src.scraping.site_scraper.requests.get") as mock_get:
        mock_get.side_effect = Exception("HTTP Error")
        scrape_website(url)
