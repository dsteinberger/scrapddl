"""
Tests for Flask routes
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from scrapddl.main import app, create_app, simplecache
from scrapddl.process import Process
from scrapddl.items.items import GroupItem, Item


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def clean_cache():
    """Clean cache before each test."""
    simplecache.clear()
    yield
    simplecache.clear()


class TestHomeRoutes:
    """Tests for home routes"""

    def test_home_returns_200(self, client):
        """Verify home page returns 200"""
        response = client.get('/')
        assert response.status_code == 200

    def test_home_contains_html(self, client):
        """Verify home page contains HTML content"""
        response = client.get('/')
        assert b'html' in response.data.lower()


class TestRefreshRoutes:
    """Tests for refresh routes"""

    def test_refresh_redirects_to_home(self, client, clean_cache):
        """Verify /refresh redirects to home"""
        response = client.get('/refresh')
        assert response.status_code == 302
        assert '/' in response.location

    def test_refresh_clears_cache(self, client, clean_cache):
        """Verify /refresh clears the process cache"""
        # Set something in cache
        simplecache.set("process", Process())
        assert simplecache.get("process") is not None

        # Call refresh
        client.get('/refresh')

        # Cache should be cleared
        assert simplecache.get("process") is None


class TestSectionHomeRoutes:
    """Tests for section home routes (movies-home, tvshows-home, mangas-home)"""

    @patch('scrapddl.main.MOVIES_SECTION_ACTIVE', True)
    @patch('scrapddl.main.process_section')
    def test_movies_home_returns_200_when_active(self, mock_process_section, client):
        """Verify /movies-home returns 200 when section is active"""
        mock_process = Mock()
        mock_process.movies_group_items = GroupItem()
        mock_process_section.return_value = mock_process

        response = client.get('/movies-home')
        assert response.status_code == 200

    @patch('scrapddl.main.MOVIES_SECTION_ACTIVE', False)
    def test_movies_home_returns_empty_when_inactive(self, client):
        """Verify /movies-home returns empty when section is inactive"""
        response = client.get('/movies-home')
        assert response.status_code == 200
        assert response.data == b''

    @patch('scrapddl.main.TVSHOWS_SECTION_ACTIVE', True)
    @patch('scrapddl.main.process_section')
    def test_tvshows_home_returns_200_when_active(self, mock_process_section, client):
        """Verify /tvshows-home returns 200 when section is active"""
        mock_process = Mock()
        mock_process.tvshows_group_items = GroupItem()
        mock_process_section.return_value = mock_process

        response = client.get('/tvshows-home')
        assert response.status_code == 200

    @patch('scrapddl.main.MANGAS_SECTION_ACTIVE', True)
    @patch('scrapddl.main.process_section')
    def test_mangas_home_returns_200_when_active(self, mock_process_section, client):
        """Verify /mangas-home returns 200 when section is active"""
        mock_process = Mock()
        mock_process.mangas_group_items = GroupItem()
        mock_process_section.return_value = mock_process

        response = client.get('/mangas-home')
        assert response.status_code == 200


class TestSectionRefreshRoutes:
    """Tests for section refresh routes"""

    def test_movies_refresh_redirects(self, client, clean_cache):
        """Verify /movies-refresh redirects"""
        response = client.get('/movies-refresh')
        assert response.status_code == 302

    def test_tvshows_refresh_redirects(self, client, clean_cache):
        """Verify /tvshows-refresh redirects"""
        response = client.get('/tvshows-refresh')
        assert response.status_code == 302

    def test_mangas_refresh_redirects(self, client, clean_cache):
        """Verify /mangas-refresh redirects"""
        response = client.get('/mangas-refresh')
        assert response.status_code == 302

    def test_movies_refresh_clears_movies_items(self, client, clean_cache):
        """Verify /movies-refresh clears movies items"""
        # Setup process with items
        process = Process()
        item = Item("test")
        item.title = "Test Movie"
        process.movies_group_items.items.append(item)
        simplecache.set("process", process)

        # Call refresh
        client.get('/movies-refresh')

        # Items should be cleared
        cached_process = simplecache.get("process")
        assert cached_process.movies_group_items.items == []


class TestSectionRoutes:
    """Tests for section pages (/movies, /tvshows, /mangas)"""

    @patch('scrapddl.main.process_section')
    def test_movies_page_returns_200(self, mock_process_section, client):
        """Verify /movies returns 200"""
        mock_process = Mock()
        mock_process.movies_group_items = GroupItem()
        mock_process_section.return_value = mock_process

        response = client.get('/movies')
        assert response.status_code == 200

    @patch('scrapddl.main.process_section')
    def test_tvshows_page_returns_200(self, mock_process_section, client):
        """Verify /tvshows returns 200"""
        mock_process = Mock()
        mock_process.tvshows_group_items = GroupItem()
        mock_process_section.return_value = mock_process

        response = client.get('/tvshows')
        assert response.status_code == 200

    @patch('scrapddl.main.process_section')
    def test_mangas_page_returns_200(self, mock_process_section, client):
        """Verify /mangas returns 200"""
        mock_process = Mock()
        mock_process.mangas_group_items = GroupItem()
        mock_process_section.return_value = mock_process

        response = client.get('/mangas')
        assert response.status_code == 200


class TestImdbRoute:
    """Tests for IMDB route"""

    @patch('scrapddl.main.IMDB_RATING_ACTIVE', False)
    def test_imdb_returns_empty_when_inactive(self, client):
        """Verify /imdb returns empty when IMDB is inactive"""
        response = client.get('/imdb/test-slug/?title=Test')
        assert response.status_code == 200
        assert response.data == b''

    @patch('scrapddl.main.IMDB_RATING_ACTIVE', True)
    def test_imdb_returns_empty_without_title(self, client):
        """Verify /imdb returns empty without title parameter"""
        response = client.get('/imdb/test-slug/')
        assert response.status_code == 200
        assert response.data == b''

    @patch('scrapddl.main.IMDB_RATING_ACTIVE', True)
    @patch('scrapddl.main.ImdbSpider')
    def test_imdb_with_valid_title(self, mock_imdb_spider, client, clean_cache):
        """Verify /imdb works with valid title"""
        mock_spider = Mock()
        mock_spider.get_rating.return_value = "8.5"
        mock_spider.get_link.return_value = "https://imdb.com/title/tt123"
        mock_imdb_spider.return_value = mock_spider

        response = client.get('/imdb/test-slug/?title=Test%20Movie')
        assert response.status_code == 200

    @patch('scrapddl.main.IMDB_RATING_ACTIVE', True)
    @patch('scrapddl.main.ImdbSpider')
    def test_imdb_handles_spider_exception(self, mock_imdb_spider, client, clean_cache):
        """Verify /imdb handles spider exception gracefully"""
        mock_imdb_spider.side_effect = Exception("API Error")

        response = client.get('/imdb/test-slug/?title=Test%20Movie')
        assert response.status_code == 200
        assert response.data == b''


class TestContextProcessor:
    """Tests for context processor"""

    def test_settings_in_context(self, client):
        """Verify settings are available in template context"""
        response = client.get('/')
        # If the page renders without error, context processor works
        assert response.status_code == 200


class TestCreateApp:
    """Tests for app factory"""

    def test_create_app_returns_flask_app(self):
        """Verify create_app returns a Flask app"""
        from flask import Flask
        test_app = create_app()
        assert isinstance(test_app, Flask)
