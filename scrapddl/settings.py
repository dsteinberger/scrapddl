IMDB_RATING_ACTIVE = True

MOVIES_SECTION_ACTIVE = True
TVSHOWS_SECTION_ACTIVE = True
MANGAS_SECTION_ACTIVE = True

TIMEOUT_REQUEST_PROVIDERS = 15


try:
    from scrapddl.local_settings import *
except ImportError:
    pass
