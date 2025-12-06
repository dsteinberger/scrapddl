from scrapddl.spiders.wawacity import WCMoviesSpider, WCMoviesHDSpider, WCTvShowsSpider, WCMangaSpider
from scrapddl.spiders.extreme_down import EDMoviesSpider, EDMoviesHDSpider, EDTvShowsSpider, EDMangaSpider
from scrapddl.spiders.zone_telechargement import ZTMoviesSpider, ZTMoviesHDSpider, ZTTvShowsSpider, ZTMangaSpider
from scrapddl.spiders.tirexo import TRMoviesSpider, TRMoviesHDSpider, TRTvShowsSpider, TRMangaSpider
from scrapddl.spiders.annuaire_telechargement import ATMoviesSpider, ATMoviesHDSpider, ATTvShowsSpider, ATMangaSpider

from scrapddl.items.items import GroupItem

MOVIES_CLASS = [EDMoviesSpider, EDMoviesHDSpider,
                ZTMoviesSpider, ZTMoviesHDSpider,
                WCMoviesSpider, WCMoviesHDSpider,
                TRMoviesSpider, TRMoviesHDSpider,
                ATMoviesSpider, ATMoviesHDSpider]
TVSHOWS_CLASS = [EDTvShowsSpider, ZTTvShowsSpider, WCTvShowsSpider, TRTvShowsSpider, ATTvShowsSpider]
MANGAS_CLASS = [ZTMangaSpider, EDMangaSpider, WCMangaSpider, TRMangaSpider, ATMangaSpider]


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
        self._process_content('movies', MOVIES_CLASS)

    def process_tvshows(self):
        self._process_content('tvshows', TVSHOWS_CLASS)

    def process_mangas(self):
        self._process_content('mangas', MANGAS_CLASS)

    def has_process_object(self, section):
        return len(getattr(self, f"{section}_group_items").items) > 0

    def process(self):
        self.process_movies()
        self.process_tvshows()
        self.process_mangas()
