from .base import BaseSpider
from scrapddl.settings import AT_MAIN_ATTR_HTML, AT_ACTIVATE_MOVIES_HD, AT_ACTIVATE_TVSHOWS, AT_ACTIVATE_MANGAS
from scrapddl.settings import AT_MAIN_CLASS
from scrapddl.settings import AT_DOMAIN
from scrapddl.settings import AT_WEBSITE
from scrapddl.settings import AT_URLS_MOVIES
from scrapddl.settings import AT_URLS_MOVIES_HD
from scrapddl.settings import AT_URLS_TVSHOWS
from scrapddl.settings import AT_URLS_MANGA

from scrapddl.settings import AT_ACTIVATE, AT_ACTIVATE_MOVIES


class ATBaseSpider(BaseSpider):
    name = "Annuaire Telechargement"
    main_attr_html = AT_MAIN_ATTR_HTML
    main_class = AT_MAIN_CLASS
    domain = AT_DOMAIN
    from_website = AT_WEBSITE

    def _get_page_url(self, element):
        # Element is the statcard div, need to get parent link
        parent = element.getparent()
        url = parent.get('href') if parent is not None else ''
        return "{}{}".format(self.domain, url)

    def _get_title(self, element):
        title_elem = element.xpath(".//div[@class='titref']")
        return title_elem[0].text if title_elem and title_elem[0].text else ''

    def _get_genre(self, element):
        # Genre not available on listing page
        return None

    def _get_image(self, element):
        image = element.xpath(".//img[@class='affiche']/@src")
        if image:
            img_src = image[0]
            if not self.is_absolute(img_src):
                return "{}{}".format(self.domain, img_src)
            return img_src
        return None

    def _get_quality_language(self, element):
        qualif = element.xpath(".//div[@class='qualif']")
        return qualif[0].text.strip() if qualif and qualif[0].text else ''


class ATMoviesSpider(ATBaseSpider):
    urls = AT_URLS_MOVIES

    @staticmethod
    def is_activated():
        return True if AT_ACTIVATE and AT_ACTIVATE_MOVIES else False


class ATMoviesHDSpider(ATBaseSpider):
    urls = AT_URLS_MOVIES_HD

    @staticmethod
    def is_activated():
        return True if AT_ACTIVATE and AT_ACTIVATE_MOVIES_HD else False


class ATTvShowsSpider(ATBaseSpider):
    urls = AT_URLS_TVSHOWS

    need_quality_data_from_title = True
    quality_data_regex = [r"(?i)saison( )?(\d+)?"]

    @staticmethod
    def is_activated():
        return True if AT_ACTIVATE and AT_ACTIVATE_TVSHOWS else False


class ATMangaSpider(ATBaseSpider):
    urls = AT_URLS_MANGA

    need_quality_data_from_title = True
    quality_data_regex = [r"(?i)saison( )?(\d+)?"]

    @staticmethod
    def is_activated():
        return True if AT_ACTIVATE and AT_ACTIVATE_MANGAS else False
