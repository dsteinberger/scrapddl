from .base import BaseSpider
from settings import ED_MAIN_CLASS
from settings import ED_MAIN_ATTR_HTML
from settings import ED_DOMAIN
from settings import ED_WEBSITE
from settings import ED_URLS_MOVIES
from settings import ED_URLS_MOVIES_HD
from settings import ED_URLS_TVSHOWS
from settings import ED_URLS_MANGA

from settings import ED_ACTIVATE

from settings import ED_ACTIVATE_MOVIES, ED_ACTIVATE_MOVIES_HD, ED_ACTIVATE_TVSHOWS, ED_ACTIVATE_MANGAS


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
        return element.xpath(
            ".//span[@class='top-genre']")[0].text.strip()

    def _get_image(self, element):
        return "{}{}".format(self.domain, element.xpath(".//img/@src")[0])

    def _get_quality_language(self, element):
        return element.xpath(
            ".//span[@class='top-lasttitle']")[0].text.strip()


class EDMoviesSpider(EDBaseSpider):
    urls = ED_URLS_MOVIES

    @staticmethod
    def is_activated():
        return True if ED_ACTIVATE and ED_ACTIVATE_MOVIES else False

class EDMoviesHDSpider(EDBaseSpider):
    urls = ED_URLS_MOVIES_HD

    @staticmethod
    def is_activated():
        return True if ED_ACTIVATE and ED_ACTIVATE_MOVIES_HD else False


class EDTvShowsSpider(EDBaseSpider):
    urls = ED_URLS_TVSHOWS

    @staticmethod
    def is_activated():
        return True if ED_ACTIVATE and ED_ACTIVATE_TVSHOWS else False


class EDMangaSpider(EDBaseSpider):
    urls = ED_URLS_MANGA

    @staticmethod
    def is_activated():
        return True if ED_ACTIVATE and ED_ACTIVATE_MANGAS else False
