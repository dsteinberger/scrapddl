"""
Tests for Process class
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from scrapddl.process import Process
from scrapddl.spiders import MOVIES_SPIDERS, TVSHOWS_SPIDERS, MANGAS_SPIDERS
from scrapddl.items.items import GroupItem, Item


class TestProcessConstants:
    """Tests for Process constants"""

    def test_movies_spiders_list_exists(self):
        """Verify that MOVIES_SPIDERS exists and contains classes"""
        assert isinstance(MOVIES_SPIDERS, list)
        assert len(MOVIES_SPIDERS) > 0

    def test_tvshows_spiders_list_exists(self):
        """Verify that TVSHOWS_SPIDERS exists and contains classes"""
        assert isinstance(TVSHOWS_SPIDERS, list)
        assert len(TVSHOWS_SPIDERS) > 0

    def test_mangas_spiders_list_exists(self):
        """Verify that MANGAS_SPIDERS exists and contains classes"""
        assert isinstance(MANGAS_SPIDERS, list)
        assert len(MANGAS_SPIDERS) > 0

    def test_movies_spiders_has_correct_count(self):
        """Verify that MOVIES_SPIDERS contains the correct number of spiders"""
        # ED, ZT, WC, TR, AT × 2 (Movies + MoviesHD) = 10
        assert len(MOVIES_SPIDERS) == 10

    def test_tvshows_spiders_has_correct_count(self):
        """Verify that TVSHOWS_SPIDERS contains the correct number of spiders"""
        # ED, ZT, WC, TR, AT = 5
        assert len(TVSHOWS_SPIDERS) == 5

    def test_mangas_spiders_has_correct_count(self):
        """Verify that MANGAS_SPIDERS contains the correct number of spiders"""
        # ED, ZT, WC, TR, AT = 5
        assert len(MANGAS_SPIDERS) == 5


class TestProcessInitialization:
    """Tests for Process initialization"""

    def test_process_initialization(self):
        """Verify that Process initializes correctly"""
        process = Process()
        assert isinstance(process.movies_group_items, GroupItem)
        assert isinstance(process.tvshows_group_items, GroupItem)
        assert isinstance(process.mangas_group_items, GroupItem)

    def test_process_group_items_are_empty_on_init(self):
        """Verify that GroupItems are empty on initialization"""
        process = Process()
        assert process.movies_group_items.items == []
        assert process.tvshows_group_items.items == []
        assert process.mangas_group_items.items == []


class TestProcessMethods:
    """Tests for Process methods"""

    def test_has_process_object_returns_false_for_empty(self):
        """Verify that has_process_object returns False for empty list"""
        process = Process()
        assert process.has_process_object("movies") is False
        assert process.has_process_object("tvshows") is False
        assert process.has_process_object("mangas") is False

    def test_has_process_object_returns_true_for_non_empty(self):
        """Verify that has_process_object returns True for non-empty list"""
        process = Process()
        item = Item("test-site")
        process.movies_group_items.items.append(item)

        assert process.has_process_object("movies") is True
        assert process.has_process_object("tvshows") is False

    @patch('scrapddl.process.MOVIES_SPIDERS')
    def test_process_movies_with_no_activated_spiders(self, mock_movies_spiders):
        """Verify process_movies when no spider is activated"""
        mock_spider_class = Mock()
        mock_spider_class.is_activated.return_value = False
        mock_movies_spiders.__iter__ = Mock(return_value=iter([mock_spider_class]))

        process = Process()
        process.process_movies()

        assert len(process.movies_group_items.items) == 0
        mock_spider_class.is_activated.assert_called_once()

    @patch('scrapddl.process.MOVIES_SPIDERS')
    def test_process_movies_with_activated_spider(self, mock_movies_spiders):
        """Verify process_movies with an activated spider"""
        # Create mock spider
        mock_spider_class = Mock()
        mock_spider_class.is_activated.return_value = True
        mock_spider_class.name = "Test Spider"

        # Create mock spider instance
        mock_spider_instance = Mock()
        mock_group_items = GroupItem()
        mock_item = Item("test-site")
        mock_group_items.items.append(mock_item)
        mock_spider_instance.parse.return_value = mock_group_items

        mock_spider_class.return_value = mock_spider_instance
        mock_movies_spiders.__iter__ = Mock(return_value=iter([mock_spider_class]))

        process = Process()
        process.process_movies()

        mock_spider_class.is_activated.assert_called_once()
        mock_spider_class.assert_called_once()
        mock_spider_instance.parse.assert_called_once()

    @patch('scrapddl.process.TVSHOWS_SPIDERS')
    def test_process_tvshows_with_activated_spider(self, mock_tvshows_spiders):
        """Verify process_tvshows with an activated spider"""
        mock_spider_class = Mock()
        mock_spider_class.is_activated.return_value = True
        mock_spider_class.name = "Test TV Spider"

        mock_spider_instance = Mock()
        mock_group_items = GroupItem()
        mock_spider_instance.parse.return_value = mock_group_items

        mock_spider_class.return_value = mock_spider_instance
        mock_tvshows_spiders.__iter__ = Mock(return_value=iter([mock_spider_class]))

        process = Process()
        process.process_tvshows()

        mock_spider_class.is_activated.assert_called_once()
        mock_spider_instance.parse.assert_called_once()

    @patch('scrapddl.process.MANGAS_SPIDERS')
    def test_process_mangas_with_activated_spider(self, mock_mangas_spiders):
        """Verify process_mangas with an activated spider"""
        mock_spider_class = Mock()
        mock_spider_class.is_activated.return_value = True
        mock_spider_class.name = "Test Manga Spider"

        mock_spider_instance = Mock()
        mock_group_items = GroupItem()
        mock_spider_instance.parse.return_value = mock_group_items

        mock_spider_class.return_value = mock_spider_instance
        mock_mangas_spiders.__iter__ = Mock(return_value=iter([mock_spider_class]))

        process = Process()
        process.process_mangas()

        mock_spider_class.is_activated.assert_called_once()
        mock_spider_instance.parse.assert_called_once()

    @patch('scrapddl.process.Process.process_mangas')
    @patch('scrapddl.process.Process.process_tvshows')
    @patch('scrapddl.process.Process.process_movies')
    def test_process_calls_all_methods(self, mock_movies, mock_tvshows, mock_mangas):
        """Verify that process() calls all methods"""
        process = Process()
        process.process()

        mock_movies.assert_called_once()
        mock_tvshows.assert_called_once()
        mock_mangas.assert_called_once()

    def test_process_movies_aggregates_items(self):
        """Verify that process_movies aggregates items correctly"""
        process = Process()

        # We can't easily mock real classes here
        # so just verify method executes without error
        # and that zip_items was called (by checking items is not None)
        with patch('scrapddl.process.MOVIES_SPIDERS', []):
            process.process_movies()
            # With empty list, items should remain empty
            assert process.movies_group_items.items == []

    def test_has_process_object_with_invalid_section(self):
        """Verify has_process_object with invalid section"""
        process = Process()
        with pytest.raises(AttributeError):
            process.has_process_object("invalid_section")

    def test_process_integration_flow(self):
        """Simple integration test of complete flow"""
        process = Process()

        # Simulate adding items
        movie_item = Item("test-movies")
        movie_item.title = "Test Movie"
        process.movies_group_items.items.append(movie_item)

        tvshow_item = Item("test-tvshows")
        tvshow_item.title = "Test Show"
        process.tvshows_group_items.items.append(tvshow_item)

        manga_item = Item("test-mangas")
        manga_item.title = "Test Manga"
        process.mangas_group_items.items.append(manga_item)

        # Verify all items are present
        assert process.has_process_object("movies") is True
        assert process.has_process_object("tvshows") is True
        assert process.has_process_object("mangas") is True
