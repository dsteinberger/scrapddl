from itertools import chain
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
        self.items = [l for l in chain(*zip(*items_list))]

    def set_unique(self):
        seen = set()
        seen_add = seen.add
        self.items = [
            x for x in self.items
            if not (x.title.lower() in seen or seen_add(
                x.title.lower()))]

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

    @staticmethod
    def fetch_imdb_rating(title):
        if title:
            imdb = ImdbSpider(title)
            imdb.process()
            return imdb.rating