

class GroupItem(object):
    items = []
    per_page = 6

    def _paginate(self):
        return [
            self.items[i:i + self.per_page]
            for i in range(0, len(self.items), self.per_page)]

    def _set_unique(self):
        seen = set()
        seen_add = seen.add
        self.items = [x for x in self.items if not (x.title in seen or seen_add(x.title))]

    def renderer(self):
        self._set_unique()
        return self._paginate()


class Item(object):
    title = None
    description = None
    genre = None
    image = None
    quality_language = None
    page_url = None
    hd_page_url = None