MOVIES_SECTION_ACTIVE = True
TVSHOWS_SECTION_ACTIVE = True
MANGAS_SECTION_ACTIVE = True

IMDB_RATING_ACTIVE = True

TIMEOUT_REQUEST_PROVIDERS = 15

# Extrem down
ED_ACTIVATE = True
ED_ACTIVATE_MOVIES = True
ED_ACTIVATE_MOVIES_HD = False
ED_ACTIVATE_TVSHOWS = True
ED_ACTIVATE_MANGAS = True

ED_WEBSITE = "extreme-down"
ED_DOMAIN = "https://www.extreme-down.cam"
ED_MAIN_ATTR_HTML = "a"
ED_MAIN_CLASS = "top-last thumbnails"
ED_URLS_MOVIES = ['/?p=films&no-bluray']
ED_URLS_MOVIES_HD = ['/?p=films&s=ultra-hd-4k']
ED_URLS_TVSHOWS = ['/?p=films&s=ultra-hd-4k']
ED_URLS_MANGA = ['/?p=mangas']

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
ZT_DOMAIN = "https://www.zone-telechargement.hair/"
ZT_MAIN_ATTR_HTML = "div"
ZT_MAIN_CLASS = "cover_global"
ZT_URLS_MOVIES = ['?p=films&no-bluray']
ZT_URLS_MOVIES_HD = ['?p=films&s=ultra-hd-4k']
ZT_URLS_TVSHOWS = ['?p=series&s=vostfr']
ZT_URLS_MANGA = ['?p=mangas&s=vostfr']

# WawaCity
WC_ACTIVATE = True
WC_ACTIVATE_MOVIES = True
WC_ACTIVATE_MOVIES_HD = False
WC_ACTIVATE_TVSHOWS = True
WC_ACTIVATE_MANGAS = True

WC_WEBSITE = "wawacity"
WC_DOMAIN = "https://www.wawacity.hair/"
WC_MAIN_ATTR_HTML = "div"
WC_MAIN_CLASS = "wa-sub-block wa-post-detail-item"
WC_URLS_MOVIES = ['?p=films&no-bluray']
WC_URLS_MOVIES_HD = ['?p=films&s=ultra-hd-4k']
WC_URLS_TVSHOWS = ['?p=series&s=vostfr']
WC_URLS_MANGA = ['?p=mangas&s=vostfr']

# --- OBSOLETE

# Tirexo
TO_ACTIVATE = False
TO_ACTIVATE_MOVIES = False
TO_ACTIVATE_MOVIES_HD = False
TO_ACTIVATE_TVSHOWS = False
TO_ACTIVATE_MANGAS = False

TO_WEBSITE = "tirexo"
TO_DOMAIN = "https://www2.palixi.com/"
TO_MAIN_ATTR_HTML = "div"
TO_MAIN_CLASS = "mov clearfix"
TO_URLS_MOVIES = ['?do=cat&category=last-films']
TO_URLS_MOVIES_HD = ['?do=cat&category=films-bluray-hd-1080']
TO_URLS_TVSHOWS = ['?do=cat&category=series-vostfr']
TO_URLS_MANGA = ['?do=cat&category=animes-vostfr']

# DDL ISLAND
DDLI_ACTIVATE = False
DDLI_ACTIVATE_MOVIES = False
DDLI_ACTIVATE_MOVIES_HD = False
DDLI_ACTIVATE_TVSHOWS = False

DDLI_WEBSITE = "ddl-island"
DDLI_DOMAIN = "http://www.ddl-is.land"
DDLI_MAIN_ATTR_HTML = "div"
DDLI_MAIN_CLASS = "fiche_listing"
DDLI_URLS_MOVIES = ['/emule-telecharger/films-1.html&order=2']
DDLI_URLS_MOVIES_HD = ['/emule-telecharger/films-hd-13.html&order=2']
DDLI_URLS_TVSHOWS = ['/emule-telecharger/series-tv-6.html&order=2']

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
