from .base import BaseSpider
from settings import ED_MAIN_CLASS
from settings import ED_MAIN_ATTR_HTML
from settings import ED_DOMAIN
from settings import ED_WEBSITE
from settings import ED_URLS_MOVIES
from settings import ED_URLS_MOVIES_HD
from settings import ED_URLS_TVSHOWS


class EDBaseSpider(BaseSpider):
    main_attr_html = ED_MAIN_CLASS
    main_class = ED_MAIN_ATTR_HTML
    domain = ED_DOMAIN
    from_website = ED_WEBSITE

    def _get_page_url(self, element):
        return element.items()[1][1]

    def _get_title(self, element):
        title = element.xpath(
            ".//span[@class='top-title']")[0].text
        return self.clean_title(title)

    def _get_genre(self, element):
        return element.xpath(
            ".//span[@class='top-genre']")[0].text.strip()

    def _get_image(self, element):
        return element.xpath(".//img/@src")[0]

    def _get_quality_language(self, element):
        return element.xpath(
            ".//span[@class='top-lasttitle']")[0].text.strip()


class EDMoviesSpider(EDBaseSpider):
    urls = ED_URLS_MOVIES
    clean_pattern_title = ["- VOSTFR WEB"]


class EDMoviesHDSpider(EDBaseSpider):
    urls = ED_URLS_MOVIES_HD
    clean_pattern_title = ["- VOSTFR WEB"]


class EDTvShowsSpider(EDBaseSpider):
    urls = ED_URLS_TVSHOWS
    clean_pattern_title = ["(2014)", "(2015)", "(2016)", "(2017)", "(2018)",
                           "(2019)", "(2020)"]
