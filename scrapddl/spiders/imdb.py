import requests
from lxml import html


class ImdbSpider(object):
    domain = "http://www.imdb.com"
    search_path = "/find?ref_=nv_sr_fn&s=tt"

    def __init__(self, title):
        self.title = title  # already encoded
        self.search_url = u"{}{}&q={}".format(self.domain, self.search_path, self.title)
        self.link_detail = None
        self.rating = None

    def process(self):
        self.search_title()
        self.detail_item()

    def search_title(self):
        page = requests.get(self.search_url)
        tree = html.fromstring(page.content)
        try:
            detail_path = tree.xpath("//td[@class='result_text']/a")[0].items()[0][1]
            self.link_detail = u"{}{}".format(self.domain, detail_path)
        except IndexError:
            pass

    def detail_item(self):
        if self.link_detail:
            page = requests.get(self.link_detail)
            tree = html.fromstring(page.content)
            try:
                self.rating = tree.xpath("//span[@itemprop='ratingValue']")[0].text.strip()
            except IndexError:
                pass
