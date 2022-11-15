from .base import BaseSpider
from settings import WC_MAIN_CLASS
from settings import WC_MAIN_ATTR_HTML
from settings import WC_DOMAIN
from settings import WC_WEBSITE
from settings import WC_URLS_MOVIES
from settings import WC_URLS_MOVIES_HD
from settings import WC_URLS_TVSHOWS
from settings import WC_URLS_MANGA


class WCBaseSpider(BaseSpider):
    main_attr_html = WC_MAIN_ATTR_HTML
    main_class = WC_MAIN_CLASS
    domain = WC_DOMAIN
    from_website = WC_WEBSITE

    def _get_page_url(self, element):
        return element.xpath(".//div[@class='wa-sub-block-title']/a")[0].items()[0][1]

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


class WCMoviesHDSpider(WCBaseSpider):
    urls = WC_URLS_MOVIES_HD


class WCTvShowsSpider(WCBaseSpider):
    urls = WC_URLS_TVSHOWS


class WCMangaSpider(WCBaseSpider):
    urls = WC_URLS_MANGA
