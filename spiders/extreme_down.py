import requests
from lxml import html

from items.items import GroupItem, Item


class ExtremDownSpider(object):
    start_urls = ['https://www.extreme-down.in/films-sd/']
    main_attr_html = 'a'
    main_class = 'top-last thumbnails'

    group_items = GroupItem()

    def _get_root(self, tree):
        return tree.xpath("//{}[@class='{}']".format(
            self.main_attr_html, self.main_class))

    def _get_page_url(self, element):
        return element.items()[1][1]

    def _get_title(self, element):
        return element.xpath(".//span[@class='top-title']")[0].text

    def _get_genre(self, element):
        return element.xpath(".//span[@class='top-genre']")[0].text

    def _get_image(self, element):
        return element.xpath(".//img/@src")[0]

    def _get_quality_language(self, element):
        return element.xpath(".//span[@class='top-lasttitle']")[0].text

    def parse(self):
        page = requests.get(self.start_urls[0])
        tree = html.fromstring(page.content)
        elements = self._get_root(tree)
        for element in elements:
            o = Item()
            o.page_url = self._get_page_url(element)
            o.title = self._get_title(element)
            o.genre = self._get_genre(element)
            o.image = self._get_image(element)
            o.quality_language = self._get_quality_language(element)
            self.group_items.movies.append(o)
        return self.group_items
