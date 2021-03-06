MOVIES_SECTION_ACTIVE = True
TVSHOWS_SECTION_ACTIVE = True
MANGAS_SECTION_ACTIVE = True

IMDB_RATING_ACTIVE = True

TIMEOUT_REQUEST_PROVIDERS = 15

# DDL ISLAND
DDLI_ACTIVATE = True
DDLI_ACTIVATE_MOVIES = True
DDLI_ACTIVATE_MOVIES_HD = False
DDLI_ACTIVATE_TVSHOWS = True

DDLI_WEBSITE = "ddl-island"
DDLI_DOMAIN = "http://www.ddl-is.land"
DDLI_MAIN_ATTR_HTML = "div"
DDLI_MAIN_CLASS = "fiche_listing"
DDLI_URLS_MOVIES = ['/emule-telecharger/films-1.html&order=2']
DDLI_URLS_MOVIES_HD = ['/emule-telecharger/films-hd-13.html&order=2']
DDLI_URLS_TVSHOWS = ['/emule-telecharger/series-tv-6.html&order=2']

# Extrem down
ED_ACTIVATE = True
ED_ACTIVATE_MOVIES = True
ED_ACTIVATE_MOVIES_HD = False
ED_ACTIVATE_TVSHOWS = True
ED_ACTIVATE_MANGAS = True

ED_WEBSITE = "extreme-down"
ED_DOMAIN = "https://www.extreme-down.video"
ED_MAIN_ATTR_HTML = "a"
ED_MAIN_CLASS = "top-last thumbnails"
ED_URLS_MOVIES = ['/films-new-sd/']
ED_URLS_MOVIES_HD = ['/films-hd/ultrahd-4k']
ED_URLS_TVSHOWS = ['/series/vostfr/']
ED_URLS_MANGA = ['/mangas/series-vostfr/']

# Univers Anime
UA_ACTIVATE = True
UA_WEBSITE = "univers-anime"
UA_DOMAIN = "https://www.universanimeiz.com/"
UA_MAIN_ATTR_HTML = "ul"
UA_MAIN_CLASS = "recent-posts"
UA_URLS = ['/', '/page/2']

# Zone telechargement
ZT_ACTIVATE = True
ZT_ACTIVATE_MOVIES = True
ZT_ACTIVATE_MOVIES_HD = False
ZT_ACTIVATE_TVSHOWS = True
ZT_ACTIVATE_MANGAS = True

ZT_WEBSITE = "zone-telechargement"
ZT_DOMAIN = "https://www.zone-telechargement.pro/"
ZT_MAIN_ATTR_HTML = "div"
ZT_MAIN_CLASS = "cover_global"
ZT_URLS_MOVIES = ['?p=films&no-bluray']
ZT_URLS_MOVIES_HD = ['?p=films&s=ultra-hd-4k']
ZT_URLS_TVSHOWS = ['?p=series&s=vostfr']
ZT_URLS_MANGA = ['?p=mangas&s=vostfr']

CLEAN_PATTERN_TITLE = [
    "(?i)\(([^\)]+)\)",  # (2018), (WEB)
    "(?i)\[([^\)]+)\]",  # [WEB], [2012]
    "(?i)(\d\D+? Season)",  # 2nd Season, 3th season
    "(?i)(S\d+)",  # S1, S2
    "(?i)VOSTFR(\w+)?",  # VOSTFR, VOSTFR, VOSTFR WEB
    "(?i)saison( )?(\d+)?",  # Saison, Saison 2
    "(?i)episode( )?(\d+)?",  # Episode, episode 2
    "(?i)VF",  # VF
    "(-)?",  # remove all -
    "[ \t]+$",  # removing trailing spaces and tabs at the end
]

try:
    from scrapddl.local_settings import *
except ImportError:
    pass
