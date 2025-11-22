"""
Tests génériques pour tous les spiders (providers).
Ces tests s'appliquent à tous les providers actifs : ED, ZT, WC
"""

import pytest
from scrapddl.spiders.extreme_down import (
    EDMoviesSpider,
    EDMoviesHDSpider,
    EDTvShowsSpider,
    EDMangaSpider
)
from scrapddl.spiders.zone_telechargement import (
    ZTMoviesSpider,
    ZTMoviesHDSpider,
    ZTTvShowsSpider,
    ZTMangaSpider
)
from scrapddl.spiders.wawacity import (
    WCMoviesSpider,
    WCMoviesHDSpider,
    WCTvShowsSpider,
    WCMangaSpider
)
from scrapddl.spiders.tirexo import (
    TRMoviesSpider,
    TRMoviesHDSpider,
    TRTvShowsSpider,
    TRMangaSpider
)


# Liste de tous les spiders actifs
ALL_SPIDERS = [
    EDMoviesSpider,
    EDMoviesHDSpider,
    EDTvShowsSpider,
    EDMangaSpider,
    ZTMoviesSpider,
    ZTMoviesHDSpider,
    ZTTvShowsSpider,
    ZTMangaSpider,
    WCMoviesSpider,
    WCMoviesHDSpider,
    WCTvShowsSpider,
    WCMangaSpider,
    TRMoviesSpider,
    TRMoviesHDSpider,
    TRTvShowsSpider,
    TRMangaSpider,
]


class TestSpidersStructure:
    """Tests de structure pour tous les spiders"""

    @pytest.mark.parametrize("spider_class", ALL_SPIDERS)
    def test_spider_can_be_instantiated(self, spider_class):
        """Vérifie que chaque spider peut être instancié sans erreur"""
        spider = spider_class()
        assert spider is not None

    @pytest.mark.parametrize("spider_class", ALL_SPIDERS)
    def test_spider_has_required_attributes(self, spider_class):
        """Vérifie que chaque spider a les attributs requis de la classe de base"""
        spider = spider_class()

        # Attributs de configuration requis
        assert hasattr(spider, 'from_website'), f"{spider_class.__name__} manque l'attribut 'from_website'"
        assert hasattr(spider, 'urls'), f"{spider_class.__name__} manque l'attribut 'urls'"
        assert hasattr(spider, 'domain'), f"{spider_class.__name__} manque l'attribut 'domain'"

        # Méthodes requises de BaseSpider
        assert hasattr(spider, 'parse'), f"{spider_class.__name__} manque la méthode 'parse'"

    @pytest.mark.parametrize("spider_class", ALL_SPIDERS)
    def test_spider_website_is_string(self, spider_class):
        """Vérifie que l'attribut from_website est une string non vide"""
        spider = spider_class()
        assert isinstance(spider.from_website, str)
        assert len(spider.from_website) > 0

    @pytest.mark.parametrize("spider_class", ALL_SPIDERS)
    def test_spider_domain_is_valid_url(self, spider_class):
        """Vérifie que le domain est une URL valide"""
        spider = spider_class()
        assert isinstance(spider.domain, str)
        assert spider.domain.startswith('http://') or spider.domain.startswith('https://')

    @pytest.mark.parametrize("spider_class", ALL_SPIDERS)
    def test_spider_urls_is_list(self, spider_class):
        """Vérifie que urls est une liste non vide"""
        spider = spider_class()
        assert isinstance(spider.urls, list)
        assert len(spider.urls) > 0

    @pytest.mark.parametrize("spider_class", ALL_SPIDERS)
    def test_spider_urls_are_strings(self, spider_class):
        """Vérifie que toutes les URLs dans la liste sont des strings"""
        spider = spider_class()
        for url in spider.urls:
            assert isinstance(url, str), f"URL invalide dans {spider_class.__name__}: {url}"


class TestSpidersMethods:
    """Tests des méthodes pour tous les spiders"""

    @pytest.mark.parametrize("spider_class", ALL_SPIDERS)
    def test_spider_parse_method_exists(self, spider_class):
        """Vérifie que la méthode parse existe et est callable"""
        spider = spider_class()
        assert callable(spider.parse)

    @pytest.mark.parametrize("spider_class", ALL_SPIDERS)
    def test_spider_is_activated_method_exists(self, spider_class):
        """Vérifie que la méthode is_activated existe et est callable"""
        assert callable(spider_class.is_activated)


class TestSpidersNaming:
    """Tests de conventions de nommage"""

    @pytest.mark.parametrize("spider_class", ALL_SPIDERS)
    def test_spider_class_name_ends_with_spider(self, spider_class):
        """Vérifie que le nom de la classe se termine par 'Spider'"""
        assert spider_class.__name__.endswith('Spider')

    @pytest.mark.parametrize("spider_class", ALL_SPIDERS)
    def test_spider_website_matches_class_prefix(self, spider_class):
        """Vérifie que le from_website correspond au préfixe de la classe"""
        spider = spider_class()
        class_name = spider_class.__name__

        # Mapping des préfixes de classe vers les noms de website
        expected_websites = {
            'ED': 'extreme-down',
            'ZT': 'zone-telechargement',
            'WC': 'wawacity',
            'TR': 'tirexo'
        }

        # Extraire le préfixe (ED, ZT, WC)
        for prefix, website in expected_websites.items():
            if class_name.startswith(prefix):
                assert spider.from_website == website, \
                    f"{class_name} devrait avoir from_website='{website}' mais a '{spider.from_website}'"
                break


class TestSpidersIntegration:
    """Tests d'intégration de base (sans vraies requêtes HTTP)"""

    @pytest.mark.parametrize("spider_class", ALL_SPIDERS)
    def test_spider_has_group_items(self, spider_class):
        """Vérifie que le spider initialise group_items correctement"""
        spider = spider_class()
        # Le spider devrait avoir un attribut group_items
        assert hasattr(spider, 'group_items')
        assert hasattr(spider.group_items, 'items')
        assert isinstance(spider.group_items.items, list)
