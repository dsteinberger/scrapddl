from scrapddl.spiders import MOVIES_SPIDERS, TVSHOWS_SPIDERS, MANGAS_SPIDERS
from scrapddl.items.items import GroupItem


class Process(object):

    def __init__(self):
        self.movies_group_items = GroupItem()
        self.tvshows_group_items = GroupItem()
        self.mangas_group_items = GroupItem()

    def _process_content(self, content_type, spider_classes):
        """Generic method to process any content type."""
        items_to_process = []
        for spider_class in spider_classes:
            if spider_class.is_activated():
                print(f"## {content_type.upper()} {spider_class.name}")
                spider = spider_class()
                group_items = spider.parse()
                items_to_process.append(group_items.items)

        getattr(self, f"{content_type}_group_items").zip_items(items_to_process)

    def process_movies(self):
        self._process_content('movies', MOVIES_SPIDERS)

    def process_tvshows(self):
        self._process_content('tvshows', TVSHOWS_SPIDERS)

    def process_mangas(self):
        self._process_content('mangas', MANGAS_SPIDERS)

    def has_process_object(self, section):
        return len(getattr(self, f"{section}_group_items").items) > 0

    def process(self):
        self.process_movies()
        self.process_tvshows()
        self.process_mangas()
