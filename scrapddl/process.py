from scrapddl.spiders.wawacity import WCMoviesSpider, WCMoviesHDSpider, WCTvShowsSpider, WCMangaSpider
from scrapddl.spiders.extreme_down import EDMoviesSpider, EDMoviesHDSpider, EDTvShowsSpider, EDMangaSpider
from scrapddl.spiders.zone_telechargement import ZTMoviesSpider, ZTMoviesHDSpider, ZTTvShowsSpider, ZTMangaSpider
from scrapddl.spiders.tirexo import TRMoviesSpider, TRMoviesHDSpider, TRTvShowsSpider, TRMangaSpider

from scrapddl.items.items import GroupItem

MOVIES_CLASS = [EDMoviesSpider, EDMoviesHDSpider,
                ZTMoviesSpider, ZTMoviesHDSpider,
                WCMoviesSpider, WCMoviesHDSpider,
                TRMoviesSpider, TRMoviesHDSpider]
TVSHOWS_CLASS = [EDTvShowsSpider, ZTTvShowsSpider, WCTvShowsSpider, TRTvShowsSpider]
MANGAS_CLASS = [ZTMangaSpider, EDMangaSpider, WCMangaSpider, TRMangaSpider]


class Process(object):

    def __init__(self):
        self.movies_group_items = GroupItem()
        self.tvshows_group_items = GroupItem()
        self.mangas_group_items = GroupItem()

    def process_movies(self):
        items_to_process = []

        for movie_class in MOVIES_CLASS:
            if movie_class.is_activated():
                print(f"## MOVIE {movie_class.name}")
                movies_spider = movie_class()
                movies_group_items = movies_spider.parse()
                items_to_process.append(movies_group_items.items)

        self.movies_group_items.zip_items(items_to_process)

    def process_tvshows(self):
        items_to_process = []

        for tvshows_class in TVSHOWS_CLASS:
            if tvshows_class.is_activated():
                print(f"## TVSHOWS {tvshows_class.name}")
                tvshows_spider = tvshows_class()
                tvshows_group_items = tvshows_spider.parse()
                items_to_process.append(tvshows_group_items.items)

        self.tvshows_group_items.zip_items(items_to_process)

    def process_mangas(self):
        items_to_process = []

        for mangas_class in MANGAS_CLASS:
            if mangas_class.is_activated():
                print(f"## MANGAS {mangas_class.name}")
                mangas_spider = mangas_class()
                mangas_group_items = mangas_spider.parse()
                items_to_process.append(mangas_group_items.items)

        self.mangas_group_items.zip_items(items_to_process)

    def has_process_object(self, section):
        if len((getattr(self, f"{section}_group_items")).items) > 0:
            return True
        return False

    def process(self):
        self.process_movies()
        self.process_tvshows()
        self.process_mangas()
