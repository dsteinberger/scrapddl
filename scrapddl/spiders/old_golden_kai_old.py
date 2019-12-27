"""
SITE CLOSE :/
"""
from .base import BaseSpider


class GoldenKMangaSpider(BaseSpider):
    # Close is door... Site not available
    urls = ['/']
    main_attr_html = 'article'
    main_class = 'release__block'
    domain = 'https://goldenkai.me'
    from_website = "golden-kai"

    def _get_page_url(self, element):
        return element.xpath(".//a")[0].items()[0][1]

    def _get_title(self, element):
        title = element.xpath(".//span[@class='release__name__anime']")[0].text.strip()
        return self.clean_title(title)

    def _get_genre(self, element):
        ep = element.xpath(".//span[@class='release__name__episode']")[0].text.strip()
        number = element.xpath(".//span[@class='release__name__number']")[0].text.strip()
        return u"{} {}".format(ep.encode('iso8859').decode('utf8'), number)

    def _get_image(self, element):
        return element.xpath(".//a/img/@src")[0]

    def _get_quality_language(self, element):
        return None
