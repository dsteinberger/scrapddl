from flask import Flask
from klein import route, run
from spiders.extreme_down import ExtremDownSpider

from crawler import MyCrawlerRunner, return_spider_output

app = Flask(__name__)


@route("/")
def home(request):
    runner = MyCrawlerRunner()
    deferred = runner.crawl(ExtremDownSpider)
    deferred.addCallback(return_spider_output)
    return deferred


run("localhost", 8080)
