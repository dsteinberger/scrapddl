from lxml.html import HtmlElement

from .base import BaseSpider
from .factory import create_provider_spiders
from scrapddl.settings import (
    AT_MAIN_CLASS, AT_MAIN_ATTR_HTML, AT_DOMAIN, AT_WEBSITE
)


class ATBaseSpider(BaseSpider):
    name = "Annuaire Telechargement"
    main_attr_html = AT_MAIN_ATTR_HTML
    main_class = AT_MAIN_CLASS
    domain = AT_DOMAIN
    from_website = AT_WEBSITE

    def _get_page_url(self, element: HtmlElement) -> str:
        parent = element.getparent()
        url = parent.get('href') if parent is not None else ''
        return "{}{}".format(self.domain, url)

    def _get_title(self, element: HtmlElement) -> str:
        title_elem = element.xpath(".//div[@class='titref']")
        return title_elem[0].text if title_elem and title_elem[0].text else ''

    def _get_genre(self, element: HtmlElement) -> None:
        return None

    def _get_image(self, element: HtmlElement) -> str | None:
        image = element.xpath(".//img[@class='affiche']/@src")
        if image:
            img_src: str = image[0]
            if not self.is_absolute(img_src):
                return "{}{}".format(self.domain, img_src)
            return img_src
        return None

    def _get_quality_language(self, element: HtmlElement) -> str:
        qualif = element.xpath(".//div[@class='qualif']")
        return qualif[0].text.strip() if qualif and qualif[0].text else ''


# Auto-generate spider classes
_spiders = create_provider_spiders(ATBaseSpider, 'AT')

ATMoviesSpider = _spiders['movies']
ATMoviesHDSpider = _spiders['movies_hd']
ATTvShowsSpider = _spiders['tvshows']
ATMangaSpider = _spiders['manga']
