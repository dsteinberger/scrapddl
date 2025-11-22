from .base import BaseSpider
from scrapddl.settings import TR_MAIN_ATTR_HTML, TR_ACTIVATE_MOVIES_HD, TR_ACTIVATE_TVSHOWS, TR_ACTIVATE_MANGAS
from scrapddl.settings import TR_MAIN_CLASS
from scrapddl.settings import TR_DOMAIN
from scrapddl.settings import TR_WEBSITE
from scrapddl.settings import TR_URLS_MOVIES
from scrapddl.settings import TR_URLS_MOVIES_HD
from scrapddl.settings import TR_URLS_TVSHOWS
from scrapddl.settings import TR_URLS_MANGA

from scrapddl.settings import TR_ACTIVATE, TR_ACTIVATE_MOVIES


class TRBaseSpider(BaseSpider):
    name = "Tirexo"
    main_attr_html = TR_MAIN_ATTR_HTML
    main_class = TR_MAIN_CLASS
    domain = TR_DOMAIN
    from_website = TR_WEBSITE

    def _get_page_url(self, element):
        url = element.xpath(".//a[@class='mov-t nowrap']/@href")[0]
        return "{}{}".format(self.domain, url)

    def _get_title(self, element):
        # Get title from img title attribute
        return element.xpath(".//img/@title")[0]

    def _get_genre(self, element):
        genre_elem = element.xpath(".//div[@class='cover_infos_genre']")
        if genre_elem:
            # Get all text nodes and join them
            texts = genre_elem[0].xpath('.//text()')
            # Filter out empty strings and join
            genre_text = ', '.join([t.strip() for t in texts if t.strip() and t.strip() != ','])
            return genre_text if genre_text else None
        return None

    def _get_image(self, element):
        image = element.xpath(".//img/@src")[0]
        if not self.is_absolute(image):
            return "{}{}".format(self.domain, image)
        return image

    def _get_quality_language(self, element):
        qualite = element.xpath(".//span[@class='qualite']//text()")
        langue = element.xpath(".//span[@class='langue']//text()")

        quality_text = ' '.join(qualite).strip() if qualite else ''
        language_text = ' '.join(langue).strip() if langue else ''

        # Combine quality and language
        if quality_text and language_text:
            return f"{quality_text} {language_text}"
        return quality_text or language_text or ''


class TRMoviesSpider(TRBaseSpider):
    urls = TR_URLS_MOVIES

    @staticmethod
    def is_activated():
        return True if TR_ACTIVATE and TR_ACTIVATE_MOVIES else False


class TRMoviesHDSpider(TRBaseSpider):
    urls = TR_URLS_MOVIES_HD

    @staticmethod
    def is_activated():
        return True if TR_ACTIVATE and TR_ACTIVATE_MOVIES_HD else False


class TRTvShowsSpider(TRBaseSpider):
    urls = TR_URLS_TVSHOWS

    need_quality_data_from_title = True
    quality_data_regex = [r"(?i)saison( )?(\d+)?"]

    @staticmethod
    def is_activated():
        return True if TR_ACTIVATE and TR_ACTIVATE_TVSHOWS else False


class TRMangaSpider(TRBaseSpider):
    urls = TR_URLS_MANGA

    need_quality_data_from_title = True
    quality_data_regex = [r"(?i)saison( )?(\d+)?"]

    @staticmethod
    def is_activated():
        return True if TR_ACTIVATE and TR_ACTIVATE_MANGAS else False
