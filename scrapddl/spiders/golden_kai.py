from .base import BaseSpider


class GoldenKMangaSpider(BaseSpider):
    urls = ['/']
    main_attr_html = 'article'
    main_class = 'release__block'
    domain = 'https://goldenkai.me'

    def _get_page_url(self, element):
        return element.xpath(".//a")[0].items()[0][1]

    def _get_title(self, element):
        return element.xpath(".//span[@class='release__name__anime']")[0].text.strip()

    def _get_genre(self, element):
        ep = element.xpath(".//span[@class='release__name__episode']")[0].text.strip()
        try:
            number = element.xpath(".//span[@class='release__name__number']")[0].text.strip()
        except AttributeError:
            number = ""
        return u"{} {}".format(ep.encode('iso8859').decode('utf8'), number)

    def _get_image(self, element):
        return element.xpath(".//a/img/@src")[0]

    def _get_quality_language(self, element):
        return None
