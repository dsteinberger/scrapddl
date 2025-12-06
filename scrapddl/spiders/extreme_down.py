from .base import BaseSpider
from .factory import create_provider_spiders
from scrapddl.settings import (
    ED_MAIN_CLASS, ED_MAIN_ATTR_HTML, ED_DOMAIN, ED_WEBSITE
)


class EDBaseSpider(BaseSpider):
    name = "Extreme Download"
    main_attr_html = ED_MAIN_ATTR_HTML
    main_class = ED_MAIN_CLASS
    domain = ED_DOMAIN
    from_website = ED_WEBSITE

    def _get_page_url(self, element):
        return "{}{}".format(self.domain, element.items()[1][1])

    def _get_title(self, element):
        return element.xpath(".//span[@class='top-title']")[0].text

    def _get_genre(self, element):
        return element.xpath(".//span[@class='top-genre']")[0].text.strip()

    def _get_image(self, element):
        return "{}{}".format(self.domain, element.xpath(".//img/@src")[0])

    def _get_quality_language(self, element):
        return element.xpath(".//span[@class='top-lasttitle']")[0].text.strip()


# Auto-generate spider classes
_spiders = create_provider_spiders(EDBaseSpider, 'ED')

EDMoviesSpider = _spiders['movies']
EDMoviesHDSpider = _spiders['movies_hd']
EDTvShowsSpider = _spiders['tvshows']
EDMangaSpider = _spiders['manga']
