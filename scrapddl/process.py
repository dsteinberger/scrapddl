from scrapddl.spiders.wawacity import WCMoviesSpider, WCMoviesHDSpider, WCTvShowsSpider, WCMangaSpider
from spiders.extreme_down import EDMoviesSpider, EDMoviesHDSpider, EDTvShowsSpider, EDMangaSpider
from spiders.zone_telechargement import ZTMoviesSpider, ZTMoviesHDSpider, ZTTvShowsSpider, ZTMangaSpider
from spiders.ddl_island import DDLIMoviesSpider, DDLIMoviesHDSpider, DDLITvShowsSpider
from spiders.univers_anime import UniversAnimeMangaSpider
from spiders.tirexo import TOMoviesSpider, TOTvShowsSpider, TOMangaSpider, TOMoviesHDSpider

from items.items import GroupItem

from scrapddl.settings import DDLI_ACTIVATE, DDLI_ACTIVATE_MOVIES, \
    DDLI_ACTIVATE_MOVIES_HD, ED_ACTIVATE, ED_ACTIVATE_MOVIES, \
    ED_ACTIVATE_MOVIES_HD, ZT_ACTIVATE, ZT_ACTIVATE_MOVIES, \
    ZT_ACTIVATE_MOVIES_HD, ED_ACTIVATE_TVSHOWS, ZT_ACTIVATE_TVSHOWS, \
    DDLI_ACTIVATE_TVSHOWS, UA_ACTIVATE, ZT_ACTIVATE_MANGAS, ED_ACTIVATE_MANGAS, \
    TO_ACTIVATE, TO_ACTIVATE_MOVIES, TO_ACTIVATE_MOVIES_HD, TO_ACTIVATE_TVSHOWS, TO_ACTIVATE_MANGAS, WC_ACTIVATE, \
    WC_ACTIVATE_MOVIES, WC_ACTIVATE_MOVIES_HD, WC_ACTIVATE_TVSHOWS, WC_ACTIVATE_MANGAS


class Process(object):

    def __init__(self):
        self.movies_group_items = GroupItem()
        self.tvshows_group_items = GroupItem()
        self.mangas_group_items = GroupItem()

    def process_movies(self):
        items_to_process = []

        if ED_ACTIVATE:
            if ED_ACTIVATE_MOVIES:
                print(f"##  Extreme Download")
                ed_movies_spider = EDMoviesSpider()
                ed_movies_group_items = ed_movies_spider.parse()
                items_to_process.append(ed_movies_group_items.items)
            if ED_ACTIVATE_MOVIES_HD:
                print(f"##  Extreme Download Hd")
                ed_movies_hd_spider = EDMoviesHDSpider()
                ed_movies_hd_group_items = ed_movies_hd_spider.parse()
                items_to_process.append(ed_movies_hd_group_items.items)

        if WC_ACTIVATE:
            if WC_ACTIVATE_MOVIES:
                print(f"##  WawaCity")
                wc_movies_spider = WCMoviesSpider()
                wc_movies_group_items = wc_movies_spider.parse()
                items_to_process.append(wc_movies_group_items.items)
            if WC_ACTIVATE_MOVIES_HD:
                print(f"##  WawaCity Hd")
                wc_movies_hd_spider = WCMoviesHDSpider()
                wc_movies_hd_group_items = wc_movies_hd_spider.parse()
                items_to_process.append(wc_movies_hd_group_items.items)

        if DDLI_ACTIVATE:
            if DDLI_ACTIVATE_MOVIES:
                print("##  Ddl Island")
                ddli_movies_spider = DDLIMoviesSpider()
                ddli_movies_group_items = ddli_movies_spider.parse()
                items_to_process.append(ddli_movies_group_items.items)
            if DDLI_ACTIVATE_MOVIES_HD:
                print("##  Ddl Island Hd")
                ddli_movies_hd_spider = DDLIMoviesHDSpider()
                ddli_movies_hd_group_items = ddli_movies_hd_spider.parse()
                items_to_process.append(ddli_movies_hd_group_items.items)

        if TO_ACTIVATE:
            if TO_ACTIVATE_MOVIES:
                print("##  Tirexo")
                to_movies_spider = TOMoviesSpider()
                to_movies_group_items = to_movies_spider.parse()
                items_to_process.append(to_movies_group_items.items)
            if TO_ACTIVATE_MOVIES_HD:
                print("##  Tirexo")
                to_movies_hd_spider = TOMoviesHDSpider()
                to_movies_hd_group_items = to_movies_hd_spider.parse()
                items_to_process.append(to_movies_hd_group_items.items)

        self.movies_group_items.zip_items(items_to_process)

    def process_tvshows(self):
        items_to_process = []

        if ED_ACTIVATE_TVSHOWS:
            print("##  Extreme Download tvshows")
            ed_tvshows_spider = EDTvShowsSpider()
            ed_tvshows_group_items = ed_tvshows_spider.parse()
            items_to_process.append(ed_tvshows_group_items.items)

        if ZT_ACTIVATE_TVSHOWS:
            print("##  Zone Telechargement tvshows")
            zt_tvshows_spider = ZTTvShowsSpider()
            zt_tvshows_group_items = zt_tvshows_spider.parse()
            items_to_process.append(zt_tvshows_group_items.items)

        if DDLI_ACTIVATE_TVSHOWS:
            print("##  Ddl Island tvshows")
            ddli_tvshows_spider = DDLITvShowsSpider()
            ddli_tvshows_group_items = ddli_tvshows_spider.parse()
            items_to_process.append(ddli_tvshows_group_items.items)

        if WC_ACTIVATE_TVSHOWS:
            print(f"##  WawaCity tvshows")
            wc_tvshows_spider = WCTvShowsSpider()
            wc_tvshows_group_items = wc_tvshows_spider.parse()
            items_to_process.append(wc_tvshows_group_items.items)

        if TO_ACTIVATE_TVSHOWS:
            print("##  Zone Telechargement tvshows")
            to_tvshows_spider = TOTvShowsSpider()
            to_tvshows_group_items = to_tvshows_spider.parse()
            items_to_process.append(to_tvshows_group_items.items)

        self.tvshows_group_items.zip_items(items_to_process)

    def process_mangas(self):
        items_to_process = []

        if UA_ACTIVATE:
            print("##  Univers Anime mangas")
            ua_manga_spider = UniversAnimeMangaSpider()
            ua_mangas_group_items = ua_manga_spider.parse()
            items_to_process.append(ua_mangas_group_items.items)

        if ZT_ACTIVATE_MANGAS:
            print("##  Zone Telechargement mangas")
            zt_manga_spider = ZTMangaSpider()
            zt_mangas_group_items = zt_manga_spider.parse()
            items_to_process.append(zt_mangas_group_items.items)

        if ED_ACTIVATE_MANGAS:
            print("##  Extreme Download mangas")
            ed_manga_spider = EDMangaSpider()
            ed_mangas_group_items = ed_manga_spider.parse()
            items_to_process.append(ed_mangas_group_items.items)

        if TO_ACTIVATE_MANGAS:
            print("##  Zone Telechargement mangas")
            to_manga_spider = TOMangaSpider()
            to_mangas_group_items = to_manga_spider.parse()
            items_to_process.append(to_mangas_group_items.items)

        if WC_ACTIVATE_MANGAS:
            print(f"##  WawaCity tvshows mangas")
            wc_manga_spider = WCMangaSpider()
            wc_manga_group_items = wc_manga_spider.parse()
            items_to_process.append(wc_manga_group_items.items)

        self.mangas_group_items.zip_items(items_to_process)

    def has_process_object(self, section):
        if len((getattr(self, f"{section}_group_items")).items) > 0:
            return True
        return False

    def process(self):
        self.process_movies()
        self.process_tvshows()
        self.process_mangas()
