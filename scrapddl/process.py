import logging
from typing import Protocol

from scrapddl.spiders import MOVIES_SPIDERS, TVSHOWS_SPIDERS, MANGAS_SPIDERS
from scrapddl.items.items import GroupItem, Item

logger = logging.getLogger(__name__)


class SpiderClass(Protocol):
    """Protocol for spider classes."""
    name: str

    @staticmethod
    def is_activated() -> bool: ...

    def __init__(self) -> None: ...

    def parse(self) -> GroupItem: ...


class Process:

    def __init__(self) -> None:
        self.movies_group_items = GroupItem()
        self.tvshows_group_items = GroupItem()
        self.mangas_group_items = GroupItem()

    def _process_content(self, content_type: str, spider_classes: list[type[SpiderClass]]) -> None:
        """Generic method to process any content type."""
        items_to_process: list[list[Item]] = []
        for spider_class in spider_classes:
            if spider_class.is_activated():
                logger.info("Processing %s: %s", content_type.upper(), spider_class.name)
                spider = spider_class()
                group_items = spider.parse()
                items_to_process.append(group_items.items)

        getattr(self, f"{content_type}_group_items").zip_items(items_to_process)

    def process_movies(self) -> None:
        self._process_content('movies', MOVIES_SPIDERS)

    def process_tvshows(self) -> None:
        self._process_content('tvshows', TVSHOWS_SPIDERS)

    def process_mangas(self) -> None:
        self._process_content('mangas', MANGAS_SPIDERS)

    def has_process_object(self, section: str) -> bool:
        return len(getattr(self, f"{section}_group_items").items) > 0

    def process(self) -> None:
        self.process_movies()
        self.process_tvshows()
        self.process_mangas()
