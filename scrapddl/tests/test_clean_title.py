import pytest

from scrapddl.spiders.base import BaseSpider
from lxml.html import HtmlElement


class ConcreteSpider(BaseSpider):
    """Concrete spider implementation for testing."""

    def _get_page_url(self, element: HtmlElement) -> str:
        return ""

    @staticmethod
    def is_activated() -> bool:
        return True

    def _get_title(self, element: HtmlElement) -> str:
        return ""

    def _get_genre(self, element: HtmlElement) -> str | None:
        return None

    def _get_image(self, element: HtmlElement) -> str | None:
        return None

    def _get_quality_language(self, element: HtmlElement) -> str | None:
        return None


@pytest.fixture()
def spider():
    return ConcreteSpider()


@pytest.mark.parametrize(
    "title,result", [
        pytest.param("test - saison 2", "test", id=" - saison X"),
        pytest.param("test - Saison 2", "test", id=" - Saison X (lowercase)"),
        pytest.param("Raised By Wolves (2020) - Saison 1",
                     "Raised By Wolves",
                     id=" - Saison X (lowercase)"),
        pytest.param("Utopia (2020)", "Utopia", id="Years ()"),
        pytest.param("Utopia [2020]", "Utopia", id="Years []"),
        pytest.param("Utopia (WEB)", "Utopia", id="Chars ()"),
        pytest.param("Utopia [WEB]", "Utopia", id="Chars []"),
        pytest.param("test - (2018) - VF", "test", id=" - saison X - VF"),
    ])
def test_clean_title(spider, title, result):
    title = spider.clean_title(title)
    assert title == result
