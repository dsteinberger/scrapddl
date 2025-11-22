"""
Tests for BaseSpider class
"""

import pytest
from scrapddl.spiders.base import BaseSpider
from scrapddl.items.items import GroupItem


class TestBaseSpider:
    """Tests for BaseSpider"""

    def test_is_absolute_with_http(self):
        """Verify is_absolute with HTTP URL"""
        assert BaseSpider.is_absolute("http://example.com/path") is True

    def test_is_absolute_with_https(self):
        """Verify is_absolute with HTTPS URL"""
        assert BaseSpider.is_absolute("https://example.com/path") is True

    def test_is_absolute_with_relative_path(self):
        """Verify is_absolute with relative path"""
        assert BaseSpider.is_absolute("/path/to/page") is False

    def test_is_absolute_with_relative_file(self):
        """Verify is_absolute with relative file"""
        assert BaseSpider.is_absolute("page.html") is False

    def test_is_absolute_with_query_string(self):
        """Verify is_absolute with query parameters"""
        assert BaseSpider.is_absolute("?param=value") is False

    def test_is_absolute_with_anchor(self):
        """Verify is_absolute with anchor"""
        assert BaseSpider.is_absolute("#section") is False

    def test_clean_title_removes_year_in_parentheses(self):
        """Verify that clean_title removes year in parentheses"""
        spider = ConcreteSpider()
        result = spider.clean_title("Film Title (2024)")
        assert "(2024)" not in result
        assert "Film Title" in result

    def test_clean_title_removes_year_in_brackets(self):
        """Verify that clean_title removes year in brackets"""
        spider = ConcreteSpider()
        result = spider.clean_title("Film Title [2024]")
        assert "[2024]" not in result
        assert "Film Title" in result

    def test_clean_title_removes_vostfr(self):
        """Verify that clean_title removes VOSTFR"""
        spider = ConcreteSpider()
        result = spider.clean_title("Film Title VOSTFR")
        assert "VOSTFR" not in result.upper()
        assert "Film Title" in result

    def test_clean_title_removes_vf(self):
        """Verify that clean_title removes VF"""
        spider = ConcreteSpider()
        result = spider.clean_title("Film Title VF")
        assert "VF" not in result
        assert "Film Title" in result

    def test_clean_title_removes_season(self):
        """Verify that clean_title removes season"""
        spider = ConcreteSpider()
        result = spider.clean_title("Series Title Saison 2")
        assert "Saison" not in result.lower()
        assert "Series Title" in result

    def test_clean_title_removes_s01(self):
        """Verify that clean_title removes S01"""
        spider = ConcreteSpider()
        result = spider.clean_title("Series Title S01")
        assert "S01" not in result
        assert "Series Title" in result

    def test_clean_title_removes_multiple_patterns(self):
        """Verify that clean_title removes multiple patterns"""
        spider = ConcreteSpider()
        result = spider.clean_title("Film Title (2024) VOSTFR [WEB]")
        assert "(2024)" not in result
        assert "VOSTFR" not in result.upper()
        assert "[WEB]" not in result
        assert "Film Title" in result

    def test_clean_title_removes_trailing_spaces(self):
        """Verify that clean_title removes trailing spaces"""
        spider = ConcreteSpider()
        result = spider.clean_title("Film Title   ")
        assert not result.endswith(" ")

    def test_clean_title_removes_hyphens(self):
        """Verify that clean_title removes hyphens"""
        spider = ConcreteSpider()
        result = spider.clean_title("Film - Title -")
        # Hyphens should be removed according to pattern
        assert result.strip() == "Film  Title"

    def test_clean_title_case_insensitive(self):
        """Verify that clean_title is case insensitive"""
        spider = ConcreteSpider()
        result1 = spider.clean_title("Film Title vostfr")
        result2 = spider.clean_title("Film Title VOSTFR")
        result3 = spider.clean_title("Film Title VoStFr")

        # All should give same result (without VOSTFR)
        assert "vostfr" not in result1.lower()
        assert "vostfr" not in result2.lower()
        assert "vostfr" not in result3.lower()

    def test_base_spider_initialization(self):
        """Verify BaseSpider initialization"""
        spider = ConcreteSpider()
        assert isinstance(spider.group_items, GroupItem)
        assert spider.request_scraper is not None

    def test_base_spider_has_required_attributes(self):
        """Verify BaseSpider has required attributes"""
        spider = ConcreteSpider()
        assert hasattr(spider, 'urls')
        assert hasattr(spider, 'main_attr_html')
        assert hasattr(spider, 'main_class')
        assert hasattr(spider, 'from_website')
        assert hasattr(spider, 'need_quality_data_from_title')
        assert hasattr(spider, 'quality_data_regex')


# Concrete class to test BaseSpider (which is abstract)
class ConcreteSpider(BaseSpider):
    """Concrete spider for testing"""

    urls = ["/?p=test"]
    domain = "https://test.com"
    from_website = "test-site"

    @staticmethod
    def is_activated():
        return True

    def _get_page_url(self, element):
        return "https://test.com/page"

    def _get_title(self, element):
        return "Test Title"

    def _get_genre(self, element):
        return "Test Genre"

    def _get_image(self, element):
        return "https://test.com/image.jpg"

    def _get_quality_language(self, element):
        return "VOSTFR 1080p"
