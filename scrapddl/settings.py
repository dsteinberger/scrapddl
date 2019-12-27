IMDB_RATING_ACTIVE = True

MOVIES_SECTION_ACTIVE = True
TVSHOWS_SECTION_ACTIVE = True
MANGAS_SECTION_ACTIVE = True

TIMEOUT_REQUEST_PROVIDERS = 15

# DDL ISLAND
DDLI_WEBSITE = "ddl-island"
DDLI_DOMAIN = "http://www.ddl-island.su"
DDLI_MAIN_ATTR_HTML = "div"
DDLI_MAIN_CLASS = "fiche_listing"
DDLI_URLS_MOVIES = ['/emule-telecharger/films-1.html&order=2']
DDLI_URLS_MOVIES_HD = ['/emule-telecharger/films-hd-13.html&order=2']
DDLI_URLS_TVSHOWS = ['/emule-telecharger/series-tv-6.html&order=2']

# Extrem down
ED_WEBSITE = "extreme-down"
ED_DOMAIN = "https://wvw.extreme-down.xyz"
ED_MAIN_ATTR_HTML = "a"
ED_MAIN_CLASS = "top-last thumbnails"
ED_URLS_MOVIES = ['/films-sd/']
ED_URLS_MOVIES_HD = ['/films-hd/ultrahd-4k']
ED_URLS_TVSHOWS = ['/series/vostfr/']

# Univers Anime
UA_WEBSITE = "univers-anime"
UA_DOMAIN = "https://www.universanimeiz.com/"
UA_MAIN_ATTR_HTML = "ul"
UA_MAIN_CLASS = "recent-posts"
UA_URLS = ['/', '/page/2']

# Zone telecharment
ZT_WEBSITE = "zone-telechargement"
ZT_DOMAIN = "https://zone-telechargement2.org/"
ZT_MAIN_ATTR_HTML = "div"
ZT_MAIN_CLASS = "cover_global"
ZT_URLS_MOVIES = ['?p=films&no-bluray']
ZT_URLS_MOVIES_HD = ['?p=films&s=ultra-hd-4k']
ZT_URLS_TVSHOWS = ['?p=series&s=vostfr']
ZT_URLS_MANGA = ['?p=mangas&s=vostfr']


try:
    from scrapddl.local_settings import *
except ImportError:
    pass
