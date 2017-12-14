from base import BaseSpider


class RARBGBaseSider(BaseSpider):
    main_attr_html = 'table'
    main_class = 'lista-rounded'
    domain = "https://rarbgmirror.xyz"
    from_website = "rarbg"

    def _get_root(self, tree):
        import ipdb
        ipdb.set_trace()
        return tree.xpath("//{}[@class='{}']/div[@align='center']/td[@class='lista']".format(
            self.main_attr_html, self.main_class))

    def _get_page_url(self, element):
        import ipdb
        ipdb.set_trace()
        return element.xpath(".//a[@class='title']/@href")[0]

    def _get_title(self, element):
        import ipdb
        ipdb.set_trace()
        title = element.xpath(".//a[@class='title']/@title")[0]
        return self.clean_title(title)

    def _get_genre(self, element):
        return None

    def _get_image(self, element):
        import ipdb
        ipdb.set_trace()
        image = element.xpath(".//a[@class='title']/img/@src")[0]
        if not self.is_absolute(image):
            return "{}{}".format(self.domain, image)
        return image

    def _get_quality_language(self, element):
        return None


class RARBGMoviesSpider(RARBGBaseSider):
    urls = ['/torrents.php']
