from base import BaseSpider


class ZTBaseSider(BaseSpider):
    main_attr_html = 'div'
    main_class = 'cover_global'
    domain = "https://zone-telechargement2.org/"
    from_website = "zone-telechargement"

    def _get_page_url(self, element):
        return element.xpath(
            ".//div[@class='cover_infos_title']/a")[0].items()[0][1]

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
    urls = ['?p=films&no-bluray']


class ZTMoviesHDSpider(ZTBaseSider):
    urls = ['?p=films&s=ultra-hd-4k']


class ZTTvShowsSpider(ZTBaseSider):
    urls = ['?p=series&s=vostfr']
    clean_pattern_title = ["(2010)", "(2011)", "(2012)", "(2013)",
                           "(2014)", "(2015)", "(2016)", "(2017)", "- Saison "]


class ZTMangaSpider(ZTBaseSider):
    urls = ['?p=mangas&s=vostfr']
    clean_pattern_title = ["(2010)", "(2011)", "(2012)", "(2013)",
                           "(2014)", "(2015)", "(2016)", "(2017)",
                           "[Complete]", "2nd Season", "Saison"]
