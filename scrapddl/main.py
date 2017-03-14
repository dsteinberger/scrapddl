from flask import Flask
from flask import render_template

from flask_bootstrap import Bootstrap

from spiders.extreme_down import EDMoviesSpider, EDTvShowsSpider
from spiders.zone_telechargement import ZTMoviesSpider, ZTTvShowsSpider

from items.items import GroupItem


def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

app = create_app()


@app.route("/")
def home():
    movies_group_items = GroupItem()
    tvshows_group_items = GroupItem()

    ed_movies_spider = EDMoviesSpider()
    ed_movies_group_items = ed_movies_spider.parse()

    ed_tvshows_spider = EDTvShowsSpider()
    ed_tvshows_group_items = ed_tvshows_spider.parse()

    zt_movies_spider = ZTMoviesSpider()
    zt_movies_group_items = zt_movies_spider.parse()

    zt_tvshows_spider = ZTTvShowsSpider()
    zt_tvshows_group_items = zt_tvshows_spider.parse()

    movies_group_items.zip_items(
        [ed_movies_group_items.items, zt_movies_group_items.items])

    tvshows_group_items.zip_items(
        [ed_tvshows_group_items.items, zt_tvshows_group_items.items])

    return render_template('home.html',
                           movies=movies_group_items.renderer(),
                           tvshows=tvshows_group_items.renderer())


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run()