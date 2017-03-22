import requests
import urlparse
from lxml import html

from slugify import slugify

from items.items import GroupItem, Item


class BaseSpider(object):
    urls = []
    main_attr_html = None
    main_class = None
    clean_pattern_title = []

    def __init__(self):
        self.group_items = GroupItem()

    @staticmethod
    def is_absolute(url):
        return bool(urlparse.urlparse(url).netloc)

    def _get_root(self, tree):
        return tree.xpath("//{}[@class='{}']".format(
            self.main_attr_html, self.main_class))

    def _get_page_url(self, element):
        raise NotImplementedError()

    def clean_title(self, title):
        for pattern in self.clean_pattern_title:
            if pattern in title:
                title_clean = title.split(pattern)[0]
                return title_clean.strip()
        return title.strip()

    def _get_title(self, element):
        raise NotImplementedError()

    def _get_genre(self, element):
        raise NotImplementedError()

    def _get_image(self, element):
        raise NotImplementedError()

    def _get_quality_language(self, element):
        raise NotImplementedError()

    def _get_elements(self, url):
        page = requests.get(url)
        tree = html.fromstring(page.content)
        return self._get_root(tree)

    def _parse_page(self, url):
        for element in self._get_elements(url):
            o = Item()
            o.page_url = self._get_page_url(element)
            o.title = self._get_title(element)
            o.slug = slugify(o.title)
            o.genre = self._get_genre(element)
            o.image = self._get_image(element)
            o.quality_language = self._get_quality_language(element)
            self.group_items.items.append(o)

    def parse(self):
        for relative_url in self.urls:
            url = "{}{}".format(self.domain, relative_url)
            self._parse_page(url)

        return self.group_items
