import re

from .base import BaseSpider
from settings import TO_MAIN_CLASS, TO_MAIN_ATTR_HTML, TO_DOMAIN, TO_WEBSITE, TO_URLS_MOVIES, \
    TO_URLS_MOVIES_HD, TO_URLS_TVSHOWS, TO_URLS_MANGA


class TOBaseSpider(BaseSpider):
    main_attr_html = TO_MAIN_ATTR_HTML
    main_class = TO_MAIN_CLASS
    domain = TO_DOMAIN
    from_website = TO_WEBSITE

    def _get_page_url(self, element):
        return element.xpath(".//a")[0].items()[1][1]

    def _get_title(self, element):
        return element.xpath(".//a")[2].text.strip()

    def _get_genre(self, element):
        return element.xpath(".//a")[4].text

    def _get_image(self, element):
        image = element.xpath(".//img/@src")[0]
        if not self.is_absolute(image):
            return "{}{}".format(self.domain, image)
        return image

    def _get_quality_language(self, element):
        genre = element.xpath(".//span[@class='qualite']/b")[0].text.strip()
        language = element.xpath(".//span[@class='langue']/b")[0].text.strip()
        return f"{genre} {language}"


class TOMoviesSpider(TOBaseSpider):
    urls = TO_URLS_MOVIES


class TOMoviesHDSpider(TOBaseSpider):
    urls = TO_URLS_MOVIES_HD


class TOTvShowsSpider(TOBaseSpider):
    urls = TO_URLS_TVSHOWS

    need_quality_data_from_title = True
    quality_data_regex = [r"(?i)saison( )?(\d+)?"]


class TOMangaSpider(TOBaseSpider):
    urls = TO_URLS_MANGA

    need_quality_data_from_title = True
    quality_data_regex = [r"(?i)saison( )?(\d+)?"]
