import logging
import re
from abc import ABC, abstractmethod
from typing import ClassVar

import requests
import cloudscraper
from lxml import html
from lxml.html import HtmlElement
from urllib.parse import urlparse

from lxml.etree import XPathEvalError
from slugify import slugify

from scrapddl.items.items import GroupItem, Item
from scrapddl.settings import (
    TIMEOUT_REQUEST_PROVIDERS, CLEAN_PATTERN_TITLE,
    HTTP_POOL_CONNECTIONS, HTTP_POOL_MAXSIZE, HTTP_MAX_RETRIES,
)

logger = logging.getLogger(__name__)


class BaseSpider(ABC):
    urls: ClassVar[list[str]] = []
    main_attr_html: ClassVar[str | None] = None
    main_class: ClassVar[str | None] = None
    from_website: ClassVar[str | None] = None
    need_quality_data_from_title: ClassVar[bool] = False
    quality_data_regex: ClassVar[list[str]] = []
    domain: ClassVar[str] = ""

    # Shared cloudscraper session for all spider instances
    _shared_scraper: ClassVar[cloudscraper.CloudScraper | None] = None

    @classmethod
    def get_scraper(cls) -> cloudscraper.CloudScraper:
        """Get or create a shared cloudscraper session"""
        if cls._shared_scraper is None:
            cls._shared_scraper = cloudscraper.create_scraper()
            adapter = requests.adapters.HTTPAdapter(
                pool_connections=HTTP_POOL_CONNECTIONS,
                pool_maxsize=HTTP_POOL_MAXSIZE,
                max_retries=HTTP_MAX_RETRIES,
            )
            cls._shared_scraper.mount('http://', adapter)
            cls._shared_scraper.mount('https://', adapter)
        return cls._shared_scraper

    def __init__(self) -> None:
        self.group_items = GroupItem()
        # Use shared scraper to avoid creating too many sessions
        self.request_scraper = self.get_scraper()

    @staticmethod
    def is_absolute(url: str) -> bool:
        return bool(urlparse(url).netloc)

    def _get_root(self, tree: HtmlElement) -> list[HtmlElement]:
        return tree.xpath(f"//{self.main_attr_html}[@class='{self.main_class}']")

    @abstractmethod
    def _get_page_url(self, element: HtmlElement) -> str:
        pass

    @staticmethod
    @abstractmethod
    def is_activated() -> bool:
        pass

    def clean_title(self, title: str) -> str:

        def _compile_title(title: str, remove: str) -> str:
            return re.sub(remove, "", title)

        for pattern in CLEAN_PATTERN_TITLE:
            title = _compile_title(title, pattern)

        return title

    @abstractmethod
    def _get_title(self, element: HtmlElement) -> str:
        pass

    @abstractmethod
    def _get_genre(self, element: HtmlElement) -> str | None:
        pass

    @abstractmethod
    def _get_image(self, element: HtmlElement) -> str | None:
        pass

    @abstractmethod
    def _get_quality_language(self, element: HtmlElement) -> str | None:
        pass

    def _get_quality_language_from_title(self, element: HtmlElement) -> str:
        extra_quality = ""

        # Retrieve quality Data on title
        title = self._get_title(element)
        for regex in self.quality_data_regex:
            p = re.compile(regex)
            data = p.search(title)
            if data:  # Check if regex matched
                extra_quality += f'{data.group(0)} '

        return extra_quality

    def _get_elements(self, url: str) -> list[HtmlElement] | None:
        page = None
        content = None

        # First attempt with cloudscraper
        try:
            page = self.request_scraper.get(url,
                                            timeout=TIMEOUT_REQUEST_PROVIDERS)
            content = page.content
        except requests.RequestException as e:
            logger.error("Request failed for %s: %s", url, e)
        finally:
            if page is not None:
                page.close()

        # Retry without certificate verification if first attempt failed
        if content is None:
            page = None
            try:
                logger.warning("Retrying %s without SSL verification", url)
                page = requests.get(url, timeout=TIMEOUT_REQUEST_PROVIDERS,
                                    verify=False)
                content = page.content
            except requests.RequestException as e:
                logger.error("Request failed for %s: %s", url, e)
                return None
            finally:
                if page is not None:
                    page.close()

        tree = html.fromstring(content)
        try:
            return self._get_root(tree)
        except (IndexError, AttributeError) as e:
            logger.error("Failed to get root for %s: %s", url, e)
            return None

    def _parse_page(self, url: str) -> None:
        try:
            elements = self._get_elements(url)
            if not elements:
                logger.warning("No elements found for %s", url)
                return
            for element in elements:
                o = Item(self.from_website or "")
                try:
                    o.page_url = self._get_page_url(element)
                except (IndexError, AttributeError) as e:
                    logger.debug("Failed to get page_url: %s - %s", e, o.__dict__)
                try:
                    title = self._get_title(element)
                    o.title = self.clean_title(title)
                except (IndexError, AttributeError, TypeError, XPathEvalError) as e:
                    logger.debug("Failed to get title: %s - %s", e, o.__dict__)
                    o.title = ""
                else:
                    o.slug = slugify(o.title)

                try:
                    o.genre = self._get_genre(element)
                except (IndexError, AttributeError) as e:
                    logger.debug("Failed to get genre: %s - %s", e, o.__dict__)

                try:
                    o.image = self._get_image(element)
                except (IndexError, AttributeError) as e:
                    logger.debug("Failed to get image: %s - %s", e, o.__dict__)

                quality_language: str | None = None
                try:
                    quality_language = self._get_quality_language(element)
                except (IndexError, AttributeError) as e:
                    logger.debug("Failed to get quality_language: %s - %s", e, o.__dict__)
                if self.need_quality_data_from_title:
                    try:
                        extra_quality = self._get_quality_language_from_title(
                            element)
                    except (IndexError, AttributeError) as e:
                        logger.debug("Failed to get extra quality: %s - %s", e, o.__dict__)
                    else:
                        if quality_language:
                            quality_language = \
                                f'{extra_quality} {quality_language}'
                        else:
                            # when quality_language is None
                            quality_language = extra_quality
                o.quality_language = quality_language

                self.group_items.items.append(o)
        except Exception as e:
            logger.exception("Unexpected error parsing %s: %s", url, e)

    def parse(self) -> GroupItem:
        for relative_url in self.urls:
            url = "{}{}".format(self.domain, relative_url)
            self._parse_page(url)
        return self.group_items
