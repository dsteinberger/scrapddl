

class GroupItem(object):
    movies = []
    tvshows = []
    per_page = 6

    def _paginate(self, items):
        return [
            items[i:i + self.per_page]
            for i in range(0, len(items), self.per_page)]

    def paginate_movies(self):
        return self._paginate(self.movies)

    def paginate_tvshows(self):
        return self._paginate(self.tvshows)


class Item(object):
    title = None
    description = None
    genre = None
    image = None
    quality_language = None
    page_url = None