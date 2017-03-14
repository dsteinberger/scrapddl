from itertools import chain

from flask import Flask
from flask import render_template

from flask_bootstrap import Bootstrap

from spiders.extreme_down import ExtremDownSpider
from spiders.zone_telechargement import ZoneTelechargementSpider

from items.items import GroupItem


def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

app = create_app()


@app.route("/")
def home():
    movies_group_items = GroupItem()

    ed_spider = ExtremDownSpider()
    ed_group_items = ed_spider.parse()

    zt_spider = ZoneTelechargementSpider()
    zt_group_items = zt_spider.parse()

    movies_group_items.items = [
        l for l in chain(*zip(ed_group_items.items, zt_group_items.items))]

    return render_template('home.html',
                           movies=movies_group_items.renderer())


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run()