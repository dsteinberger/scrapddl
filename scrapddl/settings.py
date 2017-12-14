IMDB_RATING_ACTIVE = False

MOVIES_SECTION_ACTIVE = True
TVSHOWS_SECTION_ACTIVE = False
MANGAS_SECTION_ACTIVE = False

TIMEOUT_REQUEST_PROVIDERS = 2


try:
    from scrapddl.local_settings import *
except ImportError:
    pass
