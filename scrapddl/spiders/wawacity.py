from .base import BaseSpider
from scrapddl.settings import WC_MAIN_CLASS
from scrapddl.settings import WC_MAIN_ATTR_HTML
from scrapddl.settings import WC_DOMAIN
from scrapddl.settings import WC_WEBSITE
from scrapddl.settings import WC_URLS_MOVIES
from scrapddl.settings import WC_URLS_MOVIES_HD
from scrapddl.settings import WC_URLS_TVSHOWS
from scrapddl.settings import WC_URLS_MANGA

from scrapddl.settings import WC_ACTIVATE, WC_ACTIVATE_MOVIES, WC_ACTIVATE_MOVIES_HD, WC_ACTIVATE_TVSHOWS, WC_ACTIVATE_MANGAS


class WCBaseSpider(BaseSpider):
    name = "Wawa city"
    main_attr_html = WC_MAIN_ATTR_HTML
    main_class = WC_MAIN_CLASS
    domain = WC_DOMAIN
    from_website = WC_WEBSITE

    def _get_page_url(self, element):
        url = element.xpath(".//div[@class='wa-sub-block-title']/a")[0].items()[0][1]
        if not self.is_absolute(url):
            return "{}{}".format(self.domain, url)
        return url

    def _get_title(self, element):
        return element.xpath(".//div[@class='wa-sub-block-title']/a/text()")[0].strip()

    def _get_genre(self, element):
        return ""

    def _get_image(self, element):
        image = element.xpath(".//div[@class='cover col-md-2']/a/img/@src")[0]
        if not self.is_absolute(image):
            return "{}{}".format(self.domain, image)
        return image

    def _get_quality_language(self, element):
        return element.xpath(
            ".//div[@class='wa-sub-block-title']/a/i")[1].text.strip()


class WCMoviesSpider(WCBaseSpider):
    urls = WC_URLS_MOVIES

    @staticmethod
    def is_activated():
        return True if WC_ACTIVATE and WC_ACTIVATE_MOVIES else False


class WCMoviesHDSpider(WCBaseSpider):
    urls = WC_URLS_MOVIES_HD

    @staticmethod
    def is_activated():
        return True if WC_ACTIVATE and WC_ACTIVATE_MOVIES_HD else False


class WCTvShowsSpider(WCBaseSpider):
    urls = WC_URLS_TVSHOWS

    @staticmethod
    def is_activated():
        return True if WC_ACTIVATE and WC_ACTIVATE_TVSHOWS else False


class WCMangaSpider(WCBaseSpider):
    urls = WC_URLS_MANGA

    @staticmethod
    def is_activated():
        return True if WC_ACTIVATE and WC_ACTIVATE_MANGAS else False