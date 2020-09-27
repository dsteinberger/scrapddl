import pytest

from scrapddl.spiders.base import BaseSpider


class testSpider(BaseSpider):
    pass


@pytest.fixture()
def spider():
    return testSpider()


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
