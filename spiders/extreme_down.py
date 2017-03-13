import scrapy


class ExtremDownSpider(scrapy.Spider):
    name = 'extreme-down.in'
    start_urls = ['https://www.extreme-down.in/films-sd/']

    def parse(self, response):
        for content in response.css('.top-last'):
            yield {
                'image': content.css('img').xpath('@src').extract_first(),
                'title': content.css('.top-title::text').extract_first(),
                'genre': content.css('.top-genre::text').extract_first()}
