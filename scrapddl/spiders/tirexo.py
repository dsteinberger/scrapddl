import re

from .base import BaseSpider
from settings import TO_MAIN_CLASS, TO_MAIN_ATTR_HTML, TO_DOMAIN, TO_WEBSITE, TO_URLS_MOVIES, \
    TO_URLS_MOVIES_HD, TO_URLS_TVSHOWS, TO_URLS_MANGA

from settings import TO_ACTIVATE

from settings import TO_ACTIVATE_MOVIES, TO_ACTIVATE_MOVIES_HD, TO_ACTIVATE_TVSHOWS, TO_ACTIVATE_MANGAS



class TOBaseSpider(BaseSpider):
    name = "Tirexo"
    main_attr_html = TO_MAIN_ATTR_HTML
    main_class = TO_MAIN_CLASS
    domain = TO_DOMAIN
    from_website = TO_WEBSITE

    def _get_page_url(self, element):
        return "{}{}".format(self.domain,
                             element.xpath(".//a")[0].items()[1][1])

    def _get_title(self, element):
        import ipdb
        ipdb.set_trace()
        return element.xpath(".//a")[2].text.strip()

    def _get_genre(self, element):
        return element.xpath(".//div[@class='cover_infos_genre']")[0].text

    def _get_image(self, element):
        image = element.xpath(".//img/@src")[0]
        if not self.is_absolute(image):
            return "{}{}".format(self.domain, image)
        return image

    def _get_quality_language(self, element):
        # hard to discover now...
        return


class TOMoviesSpider(TOBaseSpider):
    urls = TO_URLS_MOVIES

    @staticmethod
    def is_activated():
        return True if TO_ACTIVATE and TO_ACTIVATE_MOVIES else False


class TOMoviesHDSpider(TOBaseSpider):
    urls = TO_URLS_MOVIES_HD

    @staticmethod
    def is_activated():
        return True if TO_ACTIVATE and TO_ACTIVATE_MOVIES_HD else False


class TOTvShowsSpider(TOBaseSpider):
    urls = TO_URLS_TVSHOWS

    need_quality_data_from_title = True
    quality_data_regex = [r"(?i)saison( )?(\d+)?"]

    @staticmethod
    def is_activated():
        return True if TO_ACTIVATE and TO_ACTIVATE_TVSHOWS else False



class TOMangaSpider(TOBaseSpider):
    urls = TO_URLS_MANGA

    need_quality_data_from_title = True
    quality_data_regex = [r"(?i)saison( )?(\d+)?"]

    @staticmethod
    def is_activated():
        return True if TO_ACTIVATE and TO_ACTIVATE_MANGAS else False

