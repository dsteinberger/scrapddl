MOVIES_SECTION_ACTIVE = True
TVSHOWS_SECTION_ACTIVE = True
MANGAS_SECTION_ACTIVE = True

IMDB_RATING_ACTIVE = True
IMDB_RATING_MINIMAL_TOP = 8

TIMEOUT_REQUEST_PROVIDERS = 15

# Extrem down
ED_ACTIVATE = True
ED_ACTIVATE_MOVIES = True
ED_ACTIVATE_MOVIES_HD = False
ED_ACTIVATE_TVSHOWS = True
ED_ACTIVATE_MANGAS = True

ED_WEBSITE = "extreme-down"
ED_DOMAIN = "https://www.extrem-down.live/"
ED_MAIN_ATTR_HTML = "a"
ED_MAIN_CLASS = "top-last thumbnails"
ED_URLS_MOVIES = ['/?p=films&no-bluray']
ED_URLS_MOVIES_HD = ['/?p=films&s=ultra-hd-4k']
ED_URLS_TVSHOWS = ['/?p=series&s=vostfr']
ED_URLS_MANGA = ['/?p=mangas']

# Zone telechargement
ZT_ACTIVATE = True
ZT_ACTIVATE_MOVIES = True
ZT_ACTIVATE_MOVIES_HD = False
ZT_ACTIVATE_TVSHOWS = True
ZT_ACTIVATE_MANGAS = True

ZT_WEBSITE = "zone-telechargement"
ZT_DOMAIN = "https://www.zone-telechargement.irish/"
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
WC_DOMAIN = "https://www.wawacity.irish/"
WC_MAIN_ATTR_HTML = "div"
WC_MAIN_CLASS = "wa-sub-block wa-post-detail-item"
WC_URLS_MOVIES = ['?p=films&no-bluray']
WC_URLS_MOVIES_HD = ['?p=films&s=ultra-hd-4k']
WC_URLS_TVSHOWS = ['?p=series&s=vostfr']
WC_URLS_MANGA = ['?p=mangas&s=vostfr']

# Tirexo
TR_ACTIVATE = True
TR_ACTIVATE_MOVIES = True
TR_ACTIVATE_MOVIES_HD = False
TR_ACTIVATE_TVSHOWS = True
TR_ACTIVATE_MANGAS = True

TR_WEBSITE = "tirexo"
TR_DOMAIN = "https://www.tirexo.live/"
TR_MAIN_ATTR_HTML = "div"
TR_MAIN_CLASS = "mov clearfix"
TR_URLS_MOVIES = ['?p=films&no-bluray']
TR_URLS_MOVIES_HD = ['?p=films&s=ultra-hd-4k']
TR_URLS_TVSHOWS = ['?p=series&s=vostfr']
TR_URLS_MANGA = ['?p=mangas&s=vostfr']

# Annuaire Telechargement
AT_ACTIVATE = True
AT_ACTIVATE_MOVIES = True
AT_ACTIVATE_MOVIES_HD = False
AT_ACTIVATE_TVSHOWS = True
AT_ACTIVATE_MANGAS = True

AT_WEBSITE = "annuaire-telechargement"
AT_DOMAIN = "https://www.annuaire-telechargement.live/"
AT_MAIN_ATTR_HTML = "div"
AT_MAIN_CLASS = "statcard statcard-fiche"
AT_URLS_MOVIES = ['?p=films&no-bluray']
AT_URLS_MOVIES_HD = ['?p=films&s=ultra-hd-4k']
AT_URLS_TVSHOWS = ['?p=series']
AT_URLS_MANGA = ['?p=mangas']

CLEAN_PATTERN_TITLE = [
    r"(?i)\(([^\)]+)\)",  # (2018), (WEB)
    r"(?i)\[([^\)]+)\]",  # [WEB], [2012]
    r"(?i)(\d\D+? Season)",  # 2nd Season, 3th season
    r"(?i)(S\d+)",  # S1, S2
    r"(?i)VOSTFR(\w+)?",  # VOSTFR, VOSTFR, VOSTFR WEB
    r"(?i)saison( )?(\d+)?",  # Saison, Saison 2
    r"(?i)episode( )?(\d+)?",  # Episode, episode 2
    r"(?i)VF",  # VF
    r"(-)?",  # remove all -
    r"[ \t]+$",  # removing trailing spaces and tabs at the end
]

try:
    from scrapddl.local_settings import *
except ImportError:
    pass
