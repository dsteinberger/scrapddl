"""
Tests for Item and GroupItem classes
"""

import pytest
from scrapddl.items.items import Item, GroupItem


class TestItem:
    """Tests for Item class"""

    def test_item_initialization(self):
        """Verify that item initializes correctly"""
        item = Item(from_website="test-site")
        assert item.from_website == "test-site"
        assert item.items_clone == []
        assert item.title is None
        assert item.slug is None

    def test_item_title_urlencoded(self):
        """Verify URL encoding of title"""
        item = Item(from_website="test-site")
        item.title = "Film Test 2024"
        assert item.title_urlencoded == "Film+Test+2024"

    def test_item_title_urlencoded_with_special_chars(self):
        """Verify URL encoding with special characters"""
        item = Item(from_website="test-site")
        item.title = "Film & Série: L'Épisode"
        encoded = item.title_urlencoded
        assert "+" in encoded or "%20" in encoded
        assert "&" not in encoded

    def test_item_description_direct(self):
        """Verify that description returns direct value if set"""
        item = Item(from_website="test-site")
        item.description = "Description test"
        assert item.description == "Description test"

    def test_item_description_fallback_to_clone(self):
        """Verify that description falls back to clone if not set"""
        item = Item(from_website="site1")
        item.description = None

        clone = Item(from_website="site2")
        clone.description = "Clone description"
        item.items_clone.append(clone)

        assert item.description == "Clone description"

    def test_item_genre_direct(self):
        """Verify that genre returns direct value if set"""
        item = Item(from_website="test-site")
        item.genre = "Action"
        assert item.genre == "Action"

    def test_item_genre_fallback_to_clone(self):
        """Verify that genre falls back to clone if not set"""
        item = Item(from_website="site1")
        item.genre = None

        clone = Item(from_website="site2")
        clone.genre = "Drama"
        item.items_clone.append(clone)

        assert item.genre == "Drama"

    def test_item_quality_language_direct(self):
        """Verify that quality_language returns direct value if set"""
        item = Item(from_website="test-site")
        item.quality_language = "VOSTFR 1080p"
        assert item.quality_language == "VOSTFR 1080p"

    def test_item_quality_language_fallback_to_clone(self):
        """Verify that quality_language falls back to clone if not set"""
        item = Item(from_website="site1")
        item.quality_language = None

        clone = Item(from_website="site2")
        clone.quality_language = "VF 720p"
        item.items_clone.append(clone)

        assert item.quality_language == "VF 720p"

    def test_get_clone_property(self):
        """Verify retrieving property from clone"""
        item = Item(from_website="site1")

        clone1 = Item(from_website="site2")
        clone1.genre = None
        clone1.description = "Description clone1"

        clone2 = Item(from_website="site3")
        clone2.genre = "Action"
        clone2.description = None

        item.items_clone.extend([clone1, clone2])

        assert item.get_clone_property("description") == "Description clone1"
        assert item.get_clone_property("genre") == "Action"

    def test_get_clone_property_none_if_not_found(self):
        """Verify that get_clone_property returns None if property not found"""
        item = Item(from_website="site1")

        clone = Item(from_website="site2")
        clone.genre = None
        item.items_clone.append(clone)

        assert item.get_clone_property("genre") is None


class TestGroupItem:
    """Tests for GroupItem class"""

    def test_group_item_initialization(self):
        """Verify that GroupItem initializes with empty list"""
        group = GroupItem()
        assert group.items == []
        assert group.per_page == 6

    def test_paginate_empty_list(self):
        """Verify pagination of empty list"""
        group = GroupItem()
        result = group._paginate()
        assert result == []

    def test_paginate_less_than_per_page(self):
        """Verify pagination with fewer items than per_page"""
        group = GroupItem()
        group.items = [Item(f"site{i}") for i in range(3)]
        result = group._paginate()
        assert len(result) == 1
        assert len(result[0]) == 3

    def test_paginate_exactly_per_page(self):
        """Verify pagination with exactly per_page items"""
        group = GroupItem()
        group.items = [Item(f"site{i}") for i in range(6)]
        result = group._paginate()
        assert len(result) == 1
        assert len(result[0]) == 6

    def test_paginate_multiple_pages(self):
        """Verify pagination across multiple pages"""
        group = GroupItem()
        group.items = [Item(f"site{i}") for i in range(15)]
        result = group._paginate()
        assert len(result) == 3
        assert len(result[0]) == 6
        assert len(result[1]) == 6
        assert len(result[2]) == 3

    def test_zip_items_empty_lists(self):
        """Verify zip_items with empty lists"""
        group = GroupItem()
        group.zip_items([[], []])
        assert group.items == []

    def test_zip_items_single_list(self):
        """Verify zip_items with single list"""
        group = GroupItem()
        items1 = [Item(f"site1-{i}") for i in range(3)]
        group.zip_items([items1])
        assert len(group.items) == 3

    def test_zip_items_two_equal_lists(self):
        """Verify zip_items interleaves two lists of same size"""
        group = GroupItem()
        items1 = [Item(f"site1-{i}") for i in range(3)]
        items2 = [Item(f"site2-{i}") for i in range(3)]

        group.zip_items([items1, items2])

        assert len(group.items) == 6
        assert group.items[0].from_website == "site1-0"
        assert group.items[1].from_website == "site2-0"
        assert group.items[2].from_website == "site1-1"
        assert group.items[3].from_website == "site2-1"

    def test_zip_items_different_sizes(self):
        """Verify zip_items with lists of different sizes"""
        group = GroupItem()
        items1 = [Item(f"site1-{i}") for i in range(3)]
        items2 = [Item(f"site2-{i}") for i in range(2)]

        group.zip_items([items1, items2])

        assert len(group.items) == 5

    def test_set_unique_no_duplicates(self):
        """Verify set_unique with unique items"""
        group = GroupItem()
        item1 = Item("site1")
        item1.title = "Film A"
        item2 = Item("site2")
        item2.title = "Film B"

        group.items = [item1, item2]
        group.set_unique()

        assert len(group.items) == 2

    def test_set_unique_with_duplicates_same_website(self):
        """Verify set_unique ignores duplicates from same website"""
        group = GroupItem()
        item1 = Item("site1")
        item1.title = "Film A"
        item2 = Item("site1")
        item2.title = "Film A"

        group.items = [item1, item2]
        group.set_unique()

        assert len(group.items) == 1
        assert len(group.items[0].items_clone) == 0

    def test_set_unique_with_duplicates_different_websites(self):
        """Verify set_unique adds duplicates as clones"""
        group = GroupItem()
        item1 = Item("site1")
        item1.title = "Film A"
        item2 = Item("site2")
        item2.title = "film a"  # Same title in lowercase

        group.items = [item1, item2]
        group.set_unique()

        assert len(group.items) == 1
        assert len(group.items[0].items_clone) == 1
        assert group.items[0].items_clone[0].from_website == "site2"

    def test_set_unique_preserves_order(self):
        """Verify that set_unique preserves order of first item"""
        group = GroupItem()
        item1 = Item("site1")
        item1.title = "Film A"
        item2 = Item("site2")
        item2.title = "Film B"
        item3 = Item("site3")
        item3.title = "Film A"

        group.items = [item1, item2, item3]
        group.set_unique()

        assert len(group.items) == 2
        assert group.items[0].from_website == "site1"
        assert group.items[1].from_website == "site2"

    def test_set_unique_multiple_clones_different_websites(self):
        """Verify set_unique with multiple clones from different websites"""
        group = GroupItem()
        item1 = Item("site1")
        item1.title = "Film A"
        item2 = Item("site2")
        item2.title = "Film A"
        item3 = Item("site3")
        item3.title = "Film A"

        group.items = [item1, item2, item3]
        group.set_unique()

        assert len(group.items) == 1
        assert len(group.items[0].items_clone) == 2

    def test_set_unique_does_not_duplicate_clone_from_same_website(self):
        """Verify that we don't add two clones from same website"""
        group = GroupItem()
        item1 = Item("site1")
        item1.title = "Film A"
        item2 = Item("site2")
        item2.title = "Film A"
        item3 = Item("site2")
        item3.title = "Film A"

        group.items = [item1, item2, item3]
        group.set_unique()

        assert len(group.items) == 1
        assert len(group.items[0].items_clone) == 1

    def test_renderer_calls_set_unique_by_default(self):
        """Verify that renderer calls set_unique by default"""
        group = GroupItem()
        item1 = Item("site1")
        item1.title = "Film A"
        item2 = Item("site2")
        item2.title = "Film A"

        group.items = [item1, item2]
        result = group.renderer()

        # Should have deduplicated
        assert len(group.items) == 1

    def test_renderer_returns_paginated_list(self):
        """Verify that renderer returns paginated list"""
        group = GroupItem()
        for i in range(10):
            item = Item(f"site{i}")
            item.title = f"Film {i}"
            group.items.append(item)

        result = group.renderer()

        assert isinstance(result, list)
        assert len(result) == 2  # 2 pages (6 + 4)
        assert len(result[0]) == 6
        assert len(result[1]) == 4
