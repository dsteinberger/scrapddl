from spiders.extreme_down import EDMoviesSpider, EDMoviesHDSpider, EDTvShowsSpider
from spiders.zone_telechargement import ZTMoviesSpider, ZTMoviesHDSpider, ZTTvShowsSpider, ZTMangaSpider
from spiders.ddl_island import DDLIMoviesSpider, DDLIMoviesHDSpider, DDLITvShowsSpider
from spiders.golden_kai import GoldenKMangaSpider
from spiders.univers_anime import UniversAnimeMangaSpider

from items.items import GroupItem


class Process(object):

    def __init__(self):
        self.movies_group_items = GroupItem()
        self.tvshows_group_items = GroupItem()
        self.mangas_group_items = GroupItem()

    def process_movies(self):
        ed_movies_spider = EDMoviesSpider()
        ed_movies_group_items = ed_movies_spider.parse()

        ed_movies_hd_spider = EDMoviesHDSpider()
        ed_movies_hd_group_items = ed_movies_hd_spider.parse()

        zt_movies_spider = ZTMoviesSpider()
        zt_movies_group_items = zt_movies_spider.parse()

        zt_movies_hd_spider = ZTMoviesHDSpider()
        zt_movies_hd_group_items = zt_movies_hd_spider.parse()

        ddli_movies_spider = DDLIMoviesSpider()
        ddli_movies_group_items = ddli_movies_spider.parse()

        ddli_movies_hd_spider = DDLIMoviesHDSpider()
        ddli_movies_hd_group_items = ddli_movies_hd_spider.parse()

        self.movies_group_items.zip_items([
            ed_movies_group_items.items,
            ed_movies_hd_group_items.items,
            zt_movies_group_items.items,
            zt_movies_hd_group_items.items,
            ddli_movies_group_items.items,
            ddli_movies_hd_group_items.items])

    def process_tvshows(self):
        ed_tvshows_spider = EDTvShowsSpider()
        ed_tvshows_group_items = ed_tvshows_spider.parse()

        zt_tvshows_spider = ZTTvShowsSpider()
        zt_tvshows_group_items = zt_tvshows_spider.parse()

        ddli_tvshows_spider = DDLITvShowsSpider()
        ddli_tvshows_group_items = ddli_tvshows_spider.parse()

        self.tvshows_group_items.zip_items([
            ed_tvshows_group_items.items,
            zt_tvshows_group_items.items,
            ddli_tvshows_group_items.items])

    def process_mangas(self):
        gk_manga_spider = GoldenKMangaSpider()
        gk_mangas_group_items = gk_manga_spider.parse()

        ua_manga_spider = UniversAnimeMangaSpider()
        ua_mangas_group_items = ua_manga_spider.parse()

        zt_manga_spider = ZTMangaSpider()
        zt_mangas_group_items = zt_manga_spider.parse()

        self.mangas_group_items.zip_items([
            gk_mangas_group_items.items,
            ua_mangas_group_items.items,
            zt_mangas_group_items.items
        ])

    def has_process_object(self, section):
        if len((getattr(self, "{}_group_items".format(section))).items) > 0:
            return True
        return False

    def process(self):
        self.process_movies()
        self.process_tvshows()
        self.process_mangas()
