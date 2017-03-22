from base import BaseSpider


class DDLIBaseSpider(BaseSpider):
    main_attr_html = 'div'
    main_class = 'fiche_listing'
    domain = 'http://www.ddl-island.su'

    def _get_page_url(self, element):
        return element.xpath(".//a")[0].items()[0][1]

    def _get_title(self, element):
        title = element.xpath(".//a[@class='f titre_fiche']")[0].text_content()
        return self.clean_title(title)

    def _get_genre(self, element):
        return None

    def _get_image(self, element):
        return element.xpath(".//a/img[@class='thumb']/@src")[0]

    def _get_quality_language(self, element):
        return None


class DDLIMoviesSpider(DDLIBaseSpider):
    urls = ['/emule-telecharger/films-1.html&order=2',
            '/emule-telecharger/films-hd-13.html&order=2']
    clean_pattern_title = ["- VOSTFR"]


class DDLITvShowsSpider(DDLIBaseSpider):
    urls = ['/emule-telecharger/series-tv-6.html&order=2']
    clean_pattern_title = ["- Saison ", "(2014)", "(2015)", "(2016)", "(2017)"]
