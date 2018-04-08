from .base import BaseSpider


class UniversAnimeMangaSpider(BaseSpider):
    urls = ['/', '/page/2']
    main_attr_html = 'ul'
    main_class = 'recent-posts'
    domain = 'https://www.univers-animez.net'
    clean_pattern_title = ["(2014)", "(2015)", "(2016)", "(2017)", "VOSTFR", "VF"]
    from_website = "univers-anime"

    def _get_root(self, tree):
        return tree.xpath("//{}[@class='{}']/li".format(
            self.main_attr_html, self.main_class))

    def _get_page_url(self, element):
        return element.xpath(".//div[@class='post-thumb']/a")[0].items()[0][1]

    def _get_title(self, element):
        title = element.xpath(".//h2/a/@title")[0].strip()
        return self.clean_title(title)

    def _get_genre(self, element):
        genre = element.xpath(".//p")
        if genre:
            return genre[0].text.strip()

    def _get_image(self, element):
        return element.xpath(".//img/@src")[0]

    def _get_quality_language(self, element):
        return None
