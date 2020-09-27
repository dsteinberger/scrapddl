import re

import requests
import cloudscraper
from lxml import html
from urllib.parse import urlparse
from slugify import slugify

from scrapddl.items.items import GroupItem, Item
from scrapddl.settings import TIMEOUT_REQUEST_PROVIDERS, CLEAN_PATTERN_TITLE


class BaseSpider(object):
    urls = []
    main_attr_html = None
    main_class = None
    from_website = None

    def __init__(self):
        self.group_items = GroupItem()
        # use to bypass Cloudflare's anti-bot page
        self.request_scraper = cloudscraper.create_scraper()

    @staticmethod
    def is_absolute(url):
        return bool(urlparse(url).netloc)

    def _get_root(self, tree):
        return tree.xpath(f"//{self.main_attr_html}[@class='{self.main_class}']")

    def _get_page_url(self, element):
        raise NotImplementedError()

    def clean_title(self, title):

        def _compile_title(title, remove):
            return re.sub(remove, "", title)

        for pattern in CLEAN_PATTERN_TITLE:
            title = _compile_title(title, pattern)

        return title

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
            page = self.request_scraper.get(url,
                                            timeout=TIMEOUT_REQUEST_PROVIDERS)
        except requests.RequestException as e:
            print(f"ERROR - request url: {url} ### {e}")
            # Retry without check certificat
            try:
                page = requests.get(url, timeout=TIMEOUT_REQUEST_PROVIDERS,
                                    verify=False)
            except requests.RequestException as e:
                print(f"ERROR - request url: {url} ### {e}")
        tree = html.fromstring(page.content)
        try:
            return self._get_root(tree)
        except (IndexError, AttributeError) as e:
            print(f"ERROR - get root: {url} ### {e}")

    def _parse_page(self, url):
        try:
            elements = self._get_elements(url)
            if not elements:
                print(f"ERROR - get root is empty: {url}")
                return
            for element in elements:
                o = Item(self.from_website)
                try:
                    o.page_url = self._get_page_url(element)
                except (IndexError, AttributeError) as e:
                    print(f"ERROR - page url: {e} ### {o.__dict__}")
                try:
                    o.title = self._get_title(element)
                except (IndexError, AttributeError) as e:
                    print(f"ERROR - title: {e} ### {o.__dict__}")
                o.slug = slugify(o.title)
                try:
                    o.genre = self._get_genre(element)
                except (IndexError, AttributeError) as e:
                    print(f"ERROR - genre: {e} ### {o.__dict__}")
                try:
                    o.image = self._get_image(element)
                except (IndexError, AttributeError) as e:
                    print(f"ERROR - image: {e} ### {o.__dict__}")
                try:
                    o.quality_language = self._get_quality_language(element)
                except (IndexError, AttributeError) as e:
                    print(f"ERROR - quality & language: {e} ### {o.__dict__}")
                self.group_items.items.append(o)
        except Exception as e:
            print(f"ERROR - GLOBAL: {e} ### {url}")

    def parse(self):
        for relative_url in self.urls:
            url = "{}{}".format(self.domain, relative_url)
            self._parse_page(url)
        return self.group_items
