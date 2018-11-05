import requests
import urlparse
from lxml import html

from slugify import slugify

from scrapddl.settings import TIMEOUT_REQUEST_PROVIDERS

from items.items import GroupItem, Item


class BaseSpider(object):
    urls = []
    main_attr_html = None
    main_class = None
    clean_pattern_title = []
    from_website = None

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
        try:
            page = requests.get(url, timeout=TIMEOUT_REQUEST_PROVIDERS)
        except requests.RequestException as e:
            print u"ERROR - request url: {} ### {}".format(url, e)
            # Retry without check certificat
            try:
                page = requests.get(url, timeout=TIMEOUT_REQUEST_PROVIDERS,
                                    verify=False)
            except requests.RequestException as e:
                print u"ERROR - request url: {} ### {}".format(url, e)
        tree = html.fromstring(page.content)
        try:
            return self._get_root(tree)
        except (IndexError, AttributeError) as e:
            print u"ERROR - get root: {} ### {}".format(url, e)

    def _parse_page(self, url):
        try:
            elements = self._get_elements(url)
            if not elements:
                print u"ERROR - get root is empty: {}".format(url)
                return
            for element in elements:
                o = Item(self.from_website)
                try:
                    o.page_url = self._get_page_url(element)
                except (IndexError, AttributeError) as e:
                    print u"ERROR - page url: {} ### {}".format(e, o.__dict__)
                try:
                    o.title = self._get_title(element)
                except (IndexError, AttributeError) as e:
                    print u"ERROR - title: {} ### {}".format(e, o.__dict__)
                o.slug = slugify(o.title)
                try:
                    o.genre = self._get_genre(element)
                except (IndexError, AttributeError) as e:
                    print u"ERROR - genre: {} ### {}".format(e, o.__dict__)
                try:
                    o.image = self._get_image(element)
                except (IndexError, AttributeError) as e:
                    print u"ERROR - image: {} ### {}".format(e, o.__dict__)
                try:
                    o.quality_language = self._get_quality_language(element)
                except (IndexError, AttributeError) as e:
                    print u"ERROR - quality & language: {} ### {}".format(e, o.__dict__)
                self.group_items.items.append(o)
        except Exception as e:
            print u"ERROR - GLOBAL: {} ### {}".format(e, url)

    def parse(self):
        for relative_url in self.urls:
            url = "{}{}".format(self.domain, relative_url)
            self._parse_page(url)
        return self.group_items
