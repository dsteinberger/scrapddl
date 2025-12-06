import urllib.parse
from collections import OrderedDict
from itertools import chain
from itertools import zip_longest
from typing import Any

from scrapddl.settings import ITEMS_PER_PAGE


class GroupItem:
    per_page: int = ITEMS_PER_PAGE

    def __init__(self) -> None:
        self.items: list[Item] = []

    def _paginate(self) -> list[list["Item"]]:
        return [
            self.items[i:i + self.per_page]
            for i in range(0, len(self.items), self.per_page)]

    def zip_items(self, items_list: list[list["Item"]]) -> None:
        self.items = [item for item in chain(*zip_longest(*items_list)) if item]

    def set_unique(self) -> None:
        items_processed: OrderedDict[str, Item] = OrderedDict()
        for item in self.items:
            title = item.title.lower() if item.title else ""
            if title in items_processed:
                # Manage clone
                item_from = items_processed[title]
                # Check item from has not same "from website" before add it
                if item.from_website != item_from.from_website:
                    # First added clone
                    if not item_from.items_clone:
                        item_from.items_clone.append(item)
                    # Check items clone has not same "from website" before add it
                    elif item.from_website not in [it.from_website
                                                   for it in item_from.items_clone]:
                        item_from.items_clone.append(item)
                items_processed[title] = item_from
            else:
                # Unique item
                items_processed[title] = item
        self.items = list(items_processed.values())

    def set_imdb_rating(self) -> None:
        for item in self.items[:self.per_page]:
            item.rating_imdb = Item.fetch_imdb_rating(item.title)

    def renderer(self, unique: bool = False, need_rating: bool = False) -> list[list["Item"]]:
        if not unique:
            self.set_unique()
        if need_rating:
            self.set_imdb_rating()
        items_paginate = self._paginate()
        return items_paginate


class Item:
    title: str | None = None
    slug: str | None = None
    _description: str | None = None
    _genre: str | None = None
    image: str | None = None
    _quality_language: str | None = None
    page_url: str | None = None
    rating_imdb: str | None = None

    def __init__(self, from_website: str) -> None:
        self.from_website = from_website
        self.items_clone: list[Item] = []

    @staticmethod
    def fetch_imdb_rating(title: str | None) -> str | None:
        # Placeholder - actual implementation would fetch from IMDB
        return None

    @property
    def title_urlencoded(self) -> str:
        if self.title:
            return urllib.parse.quote_plus(self.title.encode('utf-8'))
        return ""

    def get_clone_property(self, field: str) -> Any:
        for item in self.items_clone:
            if getattr(item, field):
                return getattr(item, field)
        return None

    @property
    def description(self) -> str | None:
        if self._description:
            return self._description
        else:
            # Get the clone one if exist
            if self.items_clone:
                return self.get_clone_property("description")
        return None

    @description.setter
    def description(self, value: str | None) -> None:
        self._description = value

    @property
    def genre(self) -> str | None:
        if self._genre:
            return self._genre
        else:
            # Get the clone one if exist
            if self.items_clone:
                return self.get_clone_property("genre")
        return None

    @genre.setter
    def genre(self, value: str | None) -> None:
        self._genre = value

    @property
    def quality_language(self) -> str | None:
        if self._quality_language:
            return self._quality_language
        else:
            # Get the clone one if exist
            if self.items_clone:
                return self.get_clone_property("quality_language")
        return None

    @quality_language.setter
    def quality_language(self, value: str | None) -> None:
        self._quality_language = value
