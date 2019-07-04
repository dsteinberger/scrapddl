from base import BaseSpider


class EDBaseSpider(BaseSpider):
    main_attr_html = 'a'
    main_class = 'top-last thumbnails'
    domain = 'https://ww7.extreme-d0wn.net'
    from_website = "extreme-down"

    def _get_page_url(self, element):
        return element.items()[1][1]

    def _get_title(self, element):
        title = element.xpath(
            ".//span[@class='top-title']")[0].text
        return self.clean_title(title)

    def _get_genre(self, element):
        return element.xpath(
            ".//span[@class='top-genre']")[0].text.strip()

    def _get_image(self, element):
        return element.xpath(".//img/@src")[0]

    def _get_quality_language(self, element):
        return element.xpath(
            ".//span[@class='top-lasttitle']")[0].text.strip()


class EDMoviesSpider(EDBaseSpider):
    urls = ['/films-sd/']
    clean_pattern_title = ["- VOSTFR WEB"]


class EDMoviesHDSpider(EDBaseSpider):
    urls = ['/films-hd/ultrahd-4k']
    clean_pattern_title = ["- VOSTFR WEB"]


class EDTvShowsSpider(EDBaseSpider):
    urls = ['/series/vostfr/']
    clean_pattern_title = ["(2014)", "(2015)", "(2016)", "(2017)"]
