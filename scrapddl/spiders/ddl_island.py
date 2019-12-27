from .base import BaseSpider
from settings import DDLI_MAIN_ATTR_HTML
from settings import DDLI_MAIN_CLASS
from settings import DDLI_DOMAIN
from settings import DDLI_WEBSITE
from settings import DDLI_URLS_MOVIES
from settings import DDLI_URLS_MOVIES_HD
from settings import DDLI_URLS_TVSHOWS


class DDLIBaseSpider(BaseSpider):
    main_attr_html = DDLI_MAIN_ATTR_HTML
    main_class = DDLI_MAIN_CLASS
    domain = DDLI_DOMAIN
    from_website = DDLI_WEBSITE

    def _get_page_url(self, element):
        return element.xpath(".//a")[0].items()[0][1]

    def _get_title(self, element):
        title = element.xpath(".//a[@class='f titre_fiche']")[0].text_content()
        return self.clean_title(title)

    def _get_genre(self, element):
        return None

    def _get_image(self, element):
        return element.xpath(".//a/img[@class='thumb']/@src")[0]

    def _get_quality_language(self, element):
        return None


class DDLIMoviesSpider(DDLIBaseSpider):
    urls = DDLI_URLS_MOVIES
    clean_pattern_title = ["- VOSTFR"]


class DDLIMoviesHDSpider(DDLIBaseSpider):
    urls = DDLI_URLS_MOVIES_HD
    clean_pattern_title = ["- VOSTFR"]


class DDLITvShowsSpider(DDLIBaseSpider):
    urls = DDLI_URLS_TVSHOWS
    clean_pattern_title = ["(2014)", "(2015)", "(2016)", "(2017)", "- Saison "]
