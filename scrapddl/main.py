from flask import Flask
from flask import render_template

from flask_bootstrap import Bootstrap

from spiders.extreme_down import EDMoviesSpider, EDTvShowsSpider
from spiders.zone_telechargement import ZTMoviesSpider, ZTTvShowsSpider
from spiders.ddl_island import DDLIMoviesSpider, DDLITvShowsSpider
from spiders.golden_kai import GoldenKMangaSpider
from spiders.univers_anime import UniversAnimeMangaSpider

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
    manga_group_items = GroupItem()

    ed_movies_spider = EDMoviesSpider()
    ed_movies_group_items = ed_movies_spider.parse()

    ed_tvshows_spider = EDTvShowsSpider()
    ed_tvshows_group_items = ed_tvshows_spider.parse()

    zt_movies_spider = ZTMoviesSpider()
    zt_movies_group_items = zt_movies_spider.parse()

    zt_tvshows_spider = ZTTvShowsSpider()
    zt_tvshows_group_items = zt_tvshows_spider.parse()

    ddli_movies_spider = DDLIMoviesSpider()
    ddli_movies_group_items = ddli_movies_spider.parse()

    ddli_tvshows_spider = DDLITvShowsSpider()
    ddli_tvshows_group_items = ddli_tvshows_spider.parse()

    gk_manga_spider = GoldenKMangaSpider()
    gk_manga_group_items = gk_manga_spider.parse()

    ua_manga_spider = UniversAnimeMangaSpider()
    ua_manga_group_items = ua_manga_spider.parse()

    movies_group_items.zip_items([
        ed_movies_group_items.items,
        zt_movies_group_items.items,
        ddli_movies_group_items.items])

    tvshows_group_items.zip_items([
        ed_tvshows_group_items.items,
        zt_tvshows_group_items.items,
        ddli_tvshows_group_items.items])

    manga_group_items.zip_items([
        gk_manga_group_items.items,
        ua_manga_group_items.items
    ])

    return render_template('home.html',
                           movies=movies_group_items.renderer(),
                           tvshows=tvshows_group_items.renderer(),
                           mangas=manga_group_items.renderer())


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run()