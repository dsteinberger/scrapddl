from .base import BaseSpider
from settings import ZT_MAIN_ATTR_HTML
from settings import ZT_MAIN_CLASS
from settings import ZT_DOMAIN
from settings import ZT_WEBSITE
from settings import ZT_URLS_MOVIES
from settings import ZT_URLS_MOVIES_HD
from settings import ZT_URLS_TVSHOWS
from settings import ZT_URLS_MANGA


class ZTBaseSider(BaseSpider):
    main_attr_html = ZT_MAIN_ATTR_HTML
    main_class = ZT_MAIN_CLASS
    domain = ZT_DOMAIN
    from_website = ZT_WEBSITE

    def _get_page_url(self, element):
        return "{}{}".format(self.domain, element.xpath(
            ".//div[@class='cover_infos_title']/a")[0].items()[0][1])

    def _get_title(self, element):
        title = element.xpath(
            ".//div[@class='cover_infos_title']/a")[0].text
        return self.clean_title(title)

    def _get_genre(self, element):
        genre = element.xpath(".//div[@class='cover_infos_genre']")
        if genre:
            # NOT WORKING WHY... ?
            return genre[0].text

    def _get_image(self, element):
        image = element.xpath(".//img/@src")[0]
        if not self.is_absolute(image):
            return "{}{}".format(self.domain, image)
        return image

    def _get_quality_language(self, element):
        return element.xpath(
            ".//div[@class='cover_infos_title']/span/span/b")[0].text.strip()


class ZTMoviesSpider(ZTBaseSider):
    urls = ZT_URLS_MOVIES


class ZTMoviesHDSpider(ZTBaseSider):
    urls = ZT_URLS_MOVIES_HD


class ZTTvShowsSpider(ZTBaseSider):
    urls = ZT_URLS_TVSHOWS
    clean_pattern_title = ["(2010)", "(2011)", "(2012)", "(2013)",
                           "(2014)", "(2015)", "(2016)", "(2017)", "(2018)",
                           "(2019)", "(2020)""- Saison "]


class ZTMangaSpider(ZTBaseSider):
    urls = ZT_URLS_MANGA
    clean_pattern_title = ["(2010)", "(2011)", "(2012)", "(2013)",
                           "(2014)", "(2015)", "(2016)", "(2017)",
                           "(2018)", "(2019)", "(2020)"
                           "[Complete]", "2nd Season", "Saison"]
