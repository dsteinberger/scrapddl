from itertools import chain


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
        self.items = [x for x in self.items if not (x.title in seen or seen_add(x.title))]

    def renderer(self, unique=False):
        if not unique:
            self.set_unique()
        return self._paginate()


class Item(object):
    title = None
    description = None
    genre = None
    image = None
    quality_language = None
    page_url = None
