"""
Factory to dynamically generate Spider classes.

Instead of having 20 nearly identical classes, we generate spiders
from configuration.
"""
from scrapddl import settings


# Content types configuration
CONTENT_TYPES = {
    'movies': {
        'urls_suffix': 'URLS_MOVIES',
        'activate_suffix': 'ACTIVATE_MOVIES',
    },
    'movies_hd': {
        'urls_suffix': 'URLS_MOVIES_HD',
        'activate_suffix': 'ACTIVATE_MOVIES_HD',
    },
    'tvshows': {
        'urls_suffix': 'URLS_TVSHOWS',
        'activate_suffix': 'ACTIVATE_TVSHOWS',
        'need_quality_data_from_title': True,
        'quality_data_regex': [r"(?i)saison( )?(\d+)?"],
    },
    'manga': {
        'urls_suffix': 'URLS_MANGA',
        'activate_suffix': 'ACTIVATE_MANGAS',
        'need_quality_data_from_title': True,
        'quality_data_regex': [r"(?i)saison( )?(\d+)?"],
    },
}


def create_spider_class(base_class, prefix: str, content_type: str):
    """
    Dynamically create a Spider class for a provider and content type.

    Args:
        base_class: The provider's base class (e.g., EDBaseSpider)
        prefix: The settings prefix (e.g., 'ED')
        content_type: The content type (movies, movies_hd, tvshows, manga)

    Returns:
        A new configured Spider class
    """
    config = CONTENT_TYPES[content_type]

    # Get settings
    urls_key = f"{prefix}_{config['urls_suffix']}"
    activate_key = f"{prefix}_{config['activate_suffix']}"
    main_activate_key = f"{prefix}_ACTIVATE"

    urls = getattr(settings, urls_key)
    activate = getattr(settings, activate_key)
    main_activate = getattr(settings, main_activate_key)

    # Class attributes
    class_attrs = {
        'urls': urls,
        '_activate': activate,
        '_main_activate': main_activate,
    }

    # Add optional attributes
    if config.get('need_quality_data_from_title'):
        class_attrs['need_quality_data_from_title'] = True
        class_attrs['quality_data_regex'] = config['quality_data_regex']

    # is_activated method
    class_attrs['is_activated'] = classmethod(lambda cls: cls._main_activate and cls._activate)

    # Generate class name
    type_name = content_type.replace('_', '').title()  # movies_hd -> Movieshd
    class_name = f"{prefix}{type_name}Spider"

    # Create class dynamically
    return type(class_name, (base_class,), class_attrs)


def create_provider_spiders(base_class, prefix: str) -> dict:
    """
    Create all spiders for a provider.

    Args:
        base_class: The provider's base class
        prefix: The settings prefix (e.g., 'ED', 'ZT')

    Returns:
        Dict with keys: movies, movies_hd, tvshows, manga
    """
    return {
        content_type: create_spider_class(base_class, prefix, content_type)
        for content_type in CONTENT_TYPES
    }
