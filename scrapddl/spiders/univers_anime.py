from .base import BaseSpider
from settings import UA_MAIN_ATTR_HTML
from settings import UA_MAIN_CLASS
from settings import UA_DOMAIN
from settings import UA_WEBSITE
from settings import UA_URLS

from settings import UA_ACTIVATE


class UniversAnimeMangaSpider(BaseSpider):
    name = "Univers Anime"
    urls = UA_URLS
    main_attr_html = UA_MAIN_ATTR_HTML
    main_class = UA_MAIN_CLASS
    domain = UA_DOMAIN
    from_website = UA_WEBSITE

    def _get_root(self, tree):
        return tree.xpath("//{}[@class='{}']/li".format(
            self.main_attr_html, self.main_class))

    def _get_page_url(self, element):
        return element.xpath(".//div[@class='post-thumb']/a")[0].items()[0][1]

    def _get_title(self, element):
        return element.xpath(".//h2/a/@title")[0].strip()

    def _get_genre(self, element):
        genre = element.xpath(".//p")
        if genre:
            return genre[0].text.strip()

    def _get_image(self, element):
        return element.xpath(".//img/@src")[0]

    def _get_quality_language(self, element):
        return None

    @staticmethod
    def is_activated():
        return True if UA_ACTIVATE else False