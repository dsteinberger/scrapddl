from .base import BaseSpider
from .factory import create_provider_spiders
from scrapddl.settings import (
    ZT_MAIN_CLASS, ZT_MAIN_ATTR_HTML, ZT_DOMAIN, ZT_WEBSITE
)


class ZTBaseSpider(BaseSpider):
    name = "Zone telechargement"
    main_attr_html = ZT_MAIN_ATTR_HTML
    main_class = ZT_MAIN_CLASS
    domain = ZT_DOMAIN
    from_website = ZT_WEBSITE

    def _get_page_url(self, element):
        return "{}{}".format(self.domain, element.xpath(
            ".//div[@class='cover_infos_title']/a")[0].items()[0][1])

    def _get_title(self, element):
        return element.xpath(".//div[@class='cover_infos_title']/a")[0].text

    def _get_genre(self, element):
        genre = element.xpath(".//div[@class='cover_infos_genre']")
        if genre:
            return genre[0].text

    def _get_image(self, element):
        image = element.xpath(".//img/@src")[0]
        if not self.is_absolute(image):
            return "{}{}".format(self.domain, image)
        return image

    def _get_quality_language(self, element):
        return element.xpath(
            ".//div[@class='cover_infos_title']/span/span/b")[0].text.strip()


# Auto-generate spider classes
_spiders = create_provider_spiders(ZTBaseSpider, 'ZT')

ZTMoviesSpider = _spiders['movies']
ZTMoviesHDSpider = _spiders['movies_hd']
ZTTvShowsSpider = _spiders['tvshows']
ZTMangaSpider = _spiders['manga']
