import urllib
from collections import OrderedDict
from itertools import chain, izip_longest
from spiders.imdb import ImdbSpider


class GroupItem(object):
    per_page = 6

    def __init__(self):
        self.items = []

    def _paginate(self):
        return [
            self.items[i:i + self.per_page]
            for i in range(0, len(self.items), self.per_page)]

    def zip_items(self, items_list):
        self.items = [l for l in chain(*izip_longest(*items_list)) if l]

    def set_unique(self):
        items_processed = OrderedDict()
        for item in self.items:
            title = item.title.lower()
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
        self.items = items_processed.values()

    def set_imdb_rating(self):
        for item in self.items[:self.per_page]:
            item.rating_imdb = Item.fetch_imdb_rating(item.title)

    def renderer(self, unique=False, need_rating=False):
        if not unique:
            self.set_unique()
        if need_rating:
            self.set_imdb_rating()
        items_paginate = self._paginate()
        return items_paginate


class Item(object):
    title = None
    slug = None
    description = None
    genre = None
    image = None
    quality_language = None
    page_url = None
    rating_imdb = None

    def __init__(self, from_website):
        self.from_website = from_website
        self.items_clone = []

    @property
    def title_urlencoded(self):
        return urllib.quote_plus(self.title.encode('utf-8'))

    @staticmethod
    def fetch_imdb_rating(title):
        if title:
            imdb = ImdbSpider(title)
            imdb.process()
            return imdb

    def get_clone_property(self, field):
        for item in self.items_clone:
            if getattr(item, field):
                return getattr(item, field)

    @property
    def description(self):
        if self._description:
            return self._description
        else:
            # Get the clone one if exist
            if self.items_clone:
                return self.get_clone_property("description")

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def genre(self):
        if self._genre:
            return self._genre
        else:
            # Get the clone one if exist
            if self.items_clone:
                return self.get_clone_property("genre")

    @genre.setter
    def genre(self, value):
        self._genre = value

    @property
    def quality_language(self):
        if self._quality_language:
            return self._quality_language
        else:
            # Get the clone one if exist
            if self.items_clone:
                return self.get_clone_property("quality_language")

    @quality_language.setter
    def quality_language(self, value):
        self._quality_language = value