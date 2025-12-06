"""
Tests for HTTP integration and error handling
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests

from scrapddl.spiders.base import BaseSpider
from scrapddl.spiders.extreme_down import EDBaseSpider, EDMoviesSpider
from scrapddl.items.items import GroupItem


class TestBaseSpiderHTTP:
    """Tests for BaseSpider HTTP handling"""

    def test_get_scraper_returns_shared_instance(self):
        """Verify get_scraper returns same instance"""
        # Reset shared scraper
        BaseSpider._shared_scraper = None

        scraper1 = BaseSpider.get_scraper()
        scraper2 = BaseSpider.get_scraper()

        assert scraper1 is scraper2

    def test_get_scraper_configures_adapters(self):
        """Verify get_scraper configures HTTP adapters"""
        BaseSpider._shared_scraper = None
        scraper = BaseSpider.get_scraper()

        # Check adapters are mounted
        assert 'http://' in scraper.adapters
        assert 'https://' in scraper.adapters

    @patch.object(BaseSpider, 'get_scraper')
    def test_init_uses_shared_scraper(self, mock_get_scraper):
        """Verify __init__ uses shared scraper"""
        mock_scraper = Mock()
        mock_get_scraper.return_value = mock_scraper

        # Create a concrete spider for testing
        class TestSpider(BaseSpider):
            domain = "https://test.com"
            main_attr_html = "div"
            main_class = "test"
            from_website = "test"

            def _get_page_url(self, element):
                return "https://test.com/page"

            def _get_title(self, element):
                return "Test Title"

            def _get_genre(self, element):
                return "Test Genre"

            def _get_image(self, element):
                return "https://test.com/image.jpg"

            def _get_quality_language(self, element):
                return "HD"

            @staticmethod
            def is_activated():
                return True

        spider = TestSpider()
        assert spider.request_scraper is mock_scraper


class TestHTTPErrorHandling:
    """Tests for HTTP error handling"""

    @patch('scrapddl.spiders.base.requests.get')
    def test_get_elements_handles_connection_error(self, mock_requests_get):
        """Verify _get_elements handles connection errors"""
        # Create a concrete spider
        class TestSpider(BaseSpider):
            domain = "https://test.com"
            main_attr_html = "div"
            main_class = "test"
            from_website = "test"

            def _get_page_url(self, e):
                return ""

            def _get_title(self, e):
                return ""

            def _get_genre(self, e):
                return ""

            def _get_image(self, e):
                return ""

            def _get_quality_language(self, e):
                return ""

            @staticmethod
            def is_activated():
                return True

        spider = TestSpider()
        spider.request_scraper = Mock()
        spider.request_scraper.get.side_effect = requests.ConnectionError("Connection refused")
        mock_requests_get.side_effect = requests.ConnectionError("Connection refused")

        result = spider._get_elements("https://test.com/page")
        assert result is None

    @patch('scrapddl.spiders.base.requests.get')
    def test_get_elements_handles_timeout(self, mock_requests_get):
        """Verify _get_elements handles timeouts"""
        class TestSpider(BaseSpider):
            domain = "https://test.com"
            main_attr_html = "div"
            main_class = "test"
            from_website = "test"

            def _get_page_url(self, e):
                return ""

            def _get_title(self, e):
                return ""

            def _get_genre(self, e):
                return ""

            def _get_image(self, e):
                return ""

            def _get_quality_language(self, e):
                return ""

            @staticmethod
            def is_activated():
                return True

        spider = TestSpider()
        spider.request_scraper = Mock()
        spider.request_scraper.get.side_effect = requests.Timeout("Request timed out")
        mock_requests_get.side_effect = requests.Timeout("Request timed out")

        result = spider._get_elements("https://test.com/page")
        assert result is None

    def test_get_elements_handles_invalid_html(self):
        """Verify _get_elements handles invalid HTML"""
        class TestSpider(BaseSpider):
            domain = "https://test.com"
            main_attr_html = "div"
            main_class = "nonexistent"
            from_website = "test"

            def _get_page_url(self, e):
                return ""

            def _get_title(self, e):
                return ""

            def _get_genre(self, e):
                return ""

            def _get_image(self, e):
                return ""

            def _get_quality_language(self, e):
                return ""

            @staticmethod
            def is_activated():
                return True

        spider = TestSpider()
        spider.request_scraper = Mock()
        mock_response = Mock()
        mock_response.content = b"<html><body><p>No matching elements</p></body></html>"
        spider.request_scraper.get.return_value = mock_response

        result = spider._get_elements("https://test.com/page")
        # Should return empty list, not None
        assert result == []


class TestParsePageErrorHandling:
    """Tests for _parse_page error handling"""

    def test_parse_page_handles_empty_elements(self):
        """Verify _parse_page handles empty elements gracefully"""
        class TestSpider(BaseSpider):
            domain = "https://test.com"
            main_attr_html = "div"
            main_class = "test"
            from_website = "test"
            urls = ["/page"]

            def _get_page_url(self, e):
                return ""

            def _get_title(self, e):
                return ""

            def _get_genre(self, e):
                return ""

            def _get_image(self, e):
                return ""

            def _get_quality_language(self, e):
                return ""

            @staticmethod
            def is_activated():
                return True

        spider = TestSpider()
        spider.request_scraper = Mock()
        mock_response = Mock()
        mock_response.content = b"<html><body></body></html>"
        spider.request_scraper.get.return_value = mock_response

        # Should not raise exception
        spider._parse_page("https://test.com/page")
        assert spider.group_items.items == []

    def test_parse_page_handles_partial_data(self):
        """Verify _parse_page handles elements with partial data"""
        class TestSpider(BaseSpider):
            domain = "https://test.com"
            main_attr_html = "div"
            main_class = "item"
            from_website = "test"

            def _get_page_url(self, e):
                return "https://test.com/item"

            def _get_title(self, e):
                raise IndexError("Title not found")

            def _get_genre(self, e):
                return "Action"

            def _get_image(self, e):
                raise AttributeError("Image not found")

            def _get_quality_language(self, e):
                return "HD"

            @staticmethod
            def is_activated():
                return True

        spider = TestSpider()
        spider.request_scraper = Mock()
        mock_response = Mock()
        mock_response.content = b'<html><body><div class="item">Test</div></body></html>'
        spider.request_scraper.get.return_value = mock_response

        # Should not raise exception, should create item with partial data
        spider._parse_page("https://test.com/page")
        assert len(spider.group_items.items) == 1
        assert spider.group_items.items[0].title == ""


class TestRetryMechanism:
    """Tests for retry mechanism"""

    @patch('scrapddl.spiders.base.requests.get')
    def test_fallback_to_requests_on_cloudscraper_failure(self, mock_requests_get):
        """Verify fallback to requests when cloudscraper fails"""
        class TestSpider(BaseSpider):
            domain = "https://test.com"
            main_attr_html = "div"
            main_class = "item"
            from_website = "test"

            def _get_page_url(self, e):
                return ""

            def _get_title(self, e):
                return ""

            def _get_genre(self, e):
                return ""

            def _get_image(self, e):
                return ""

            def _get_quality_language(self, e):
                return ""

            @staticmethod
            def is_activated():
                return True

        spider = TestSpider()
        spider.request_scraper = Mock()
        spider.request_scraper.get.side_effect = requests.RequestException("Cloudscraper failed")

        mock_response = Mock()
        mock_response.content = b'<html><body><div class="item">Test</div></body></html>'
        mock_requests_get.return_value = mock_response

        result = spider._get_elements("https://test.com/page")

        # Should have tried fallback
        mock_requests_get.assert_called_once()
        assert result is not None


class TestURLValidation:
    """Tests for URL handling"""

    def test_is_absolute_with_absolute_url(self):
        """Verify is_absolute returns True for absolute URLs"""
        assert BaseSpider.is_absolute("https://example.com/path") is True
        assert BaseSpider.is_absolute("http://example.com") is True

    def test_is_absolute_with_relative_url(self):
        """Verify is_absolute returns False for relative URLs"""
        assert BaseSpider.is_absolute("/path/to/page") is False
        assert BaseSpider.is_absolute("path/to/page") is False
        assert BaseSpider.is_absolute("") is False


class TestCleanTitle:
    """Tests for title cleaning"""

    def test_clean_title_removes_year(self):
        """Verify clean_title removes year patterns"""
        spider = EDBaseSpider()
        result = spider.clean_title("Movie Title (2023)")
        assert "(2023)" not in result

    def test_clean_title_removes_quality(self):
        """Verify clean_title removes quality patterns"""
        spider = EDBaseSpider()
        result = spider.clean_title("Movie Title VOSTFR")
        assert "VOSTFR" not in result

    def test_clean_title_removes_season(self):
        """Verify clean_title removes season patterns"""
        spider = EDBaseSpider()
        result = spider.clean_title("Show Title Saison 2")
        assert "Saison" not in result
        assert "2" not in result or "Title" in result

    def test_clean_title_preserves_actual_title(self):
        """Verify clean_title preserves the actual title"""
        spider = EDBaseSpider()
        result = spider.clean_title("The Matrix")
        assert "Matrix" in result
