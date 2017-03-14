import requests
from lxml import html
from itertools import chain

from items.items import GroupItem, Item


class ZoneTelechargementSpider(object):
    movies_url = ['http://www.zone-telechargement.ws/nouveaute/',
                  'http://www.zone-telechargement.ws/films-bluray-hd/']
    main_attr_html = 'div'
    main_class = 'cover_global'

    def __init__(self):
        self.group_items = GroupItem()

    def _get_root(self, tree):
        return tree.xpath("//{}[@class='{}']".format(
            self.main_attr_html, self.main_class))

    def _get_page_url(self, element):
        return element.xpath(
            ".//div[@class='cover_infos_title']/a")[0].items()[0][1]

    def _get_title(self, element):
        return element.xpath(
            ".//div[@class='cover_infos_title']/a")[0].text.strip()

    def _get_genre(self, element):
        return None

    def _get_image(self, element):
        return element.xpath(".//img/@src")[0]

    def _get_quality_language(self, element):
        return element.xpath(
            ".//div[@class='cover_infos_title']/span/span/b")[0].text.strip()

    def _get_elements(self, url):
        page = requests.get(url)
        tree = html.fromstring(page.content)
        return self._get_root(tree)

    def _parse_items(self, url):
        items = []
        page = requests.get(url)
        tree = html.fromstring(page.content)
        elements = self._get_root(tree)
        for element in elements:
            o = Item()
            o.page_url = self._get_page_url(element)
            o.title = self._get_title(element)
            o.genre = self._get_genre(element)
            o.image = self._get_image(element)
            o.quality_language = self._get_quality_language(element)
            items.append(o)
        return items

    def parse(self):
        results = []
        for url in self.movies_url:
            results.append(self._parse_items(url))
        # zip results
        self.group_items.items += [l for l in chain(*zip(*results))]

        return self.group_items
