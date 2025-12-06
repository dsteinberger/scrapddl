"""
Spider registry - exposes all spider classes grouped by content type.
"""
from .extreme_down import EDMoviesSpider, EDMoviesHDSpider, EDTvShowsSpider, EDMangaSpider
from .zone_telechargement import ZTMoviesSpider, ZTMoviesHDSpider, ZTTvShowsSpider, ZTMangaSpider
from .wawacity import WCMoviesSpider, WCMoviesHDSpider, WCTvShowsSpider, WCMangaSpider
from .tirexo import TRMoviesSpider, TRMoviesHDSpider, TRTvShowsSpider, TRMangaSpider
from .annuaire_telechargement import ATMoviesSpider, ATMoviesHDSpider, ATTvShowsSpider, ATMangaSpider

# Spider classes grouped by content type
MOVIES_SPIDERS = [
    EDMoviesSpider, EDMoviesHDSpider,
    ZTMoviesSpider, ZTMoviesHDSpider,
    WCMoviesSpider, WCMoviesHDSpider,
    TRMoviesSpider, TRMoviesHDSpider,
    ATMoviesSpider, ATMoviesHDSpider,
]

TVSHOWS_SPIDERS = [
    EDTvShowsSpider,
    ZTTvShowsSpider,
    WCTvShowsSpider,
    TRTvShowsSpider,
    ATTvShowsSpider,
]

MANGAS_SPIDERS = [
    EDMangaSpider,
    ZTMangaSpider,
    WCMangaSpider,
    TRMangaSpider,
    ATMangaSpider,
]
