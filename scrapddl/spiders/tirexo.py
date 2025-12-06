from .base import BaseSpider
from .factory import create_provider_spiders
from scrapddl.settings import (
    TR_MAIN_CLASS, TR_MAIN_ATTR_HTML, TR_DOMAIN, TR_WEBSITE
)


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
        return element.xpath(".//img/@title")[0]

    def _get_genre(self, element):
        genre_elem = element.xpath(".//div[@class='cover_infos_genre']")
        if genre_elem:
            texts = genre_elem[0].xpath('.//text()')
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

        if quality_text and language_text:
            return f"{quality_text} {language_text}"
        return quality_text or language_text or ''


# Auto-generate spider classes
_spiders = create_provider_spiders(TRBaseSpider, 'TR')

TRMoviesSpider = _spiders['movies']
TRMoviesHDSpider = _spiders['movies_hd']
TRTvShowsSpider = _spiders['tvshows']
TRMangaSpider = _spiders['manga']
