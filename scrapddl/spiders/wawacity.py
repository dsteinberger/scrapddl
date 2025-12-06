from .base import BaseSpider
from .factory import create_provider_spiders
from scrapddl.settings import (
    WC_MAIN_CLASS, WC_MAIN_ATTR_HTML, WC_DOMAIN, WC_WEBSITE
)


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


# Auto-generate spider classes
_spiders = create_provider_spiders(WCBaseSpider, 'WC')

WCMoviesSpider = _spiders['movies']
WCMoviesHDSpider = _spiders['movies_hd']
WCTvShowsSpider = _spiders['tvshows']
WCMangaSpider = _spiders['manga']
