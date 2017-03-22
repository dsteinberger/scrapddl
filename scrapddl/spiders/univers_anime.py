from .base import BaseSpider


class UniversAnimeMangaSpider(BaseSpider):
    urls = ['/', '/page/2']
    main_attr_html = 'div'
    main_class = 'category-mangasaimeseries'
    domain = 'http://www.univers-animezi.com'
    clean_pattern_title = ["VOSTFR", "(2014)", "(2015)", "(2016)", "(2017)"]

    def _get_root(self, tree):
        return tree.xpath("//{}[contains(@class, {}) and contains(@class ,'type-post')]".format(
            self.main_attr_html, self.main_class))

    def _get_page_url(self, element):
        return element.xpath(".//a")[0].items()[0][1]

    def _get_title(self, element):
        title = element.xpath(".//h2[@class='title']/a")[0].text.strip()
        return self.clean_title(title)

    def _get_genre(self, element):
        genre = element.xpath(".//h4/span/strong")
        if genre:
            return genre[0].text.strip()
        return element.xpath(".//h4/strong/span")[0].text.strip()

    def _get_image(self, element):
        return element.xpath(".//img/@src")[0]

    def _get_quality_language(self, element):
        return None
