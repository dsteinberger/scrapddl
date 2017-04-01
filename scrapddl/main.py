from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap

from werkzeug.contrib.cache import SimpleCache

from process import Process

from items.items import Item


simplecache = SimpleCache()
CACHE_TIMEOUT = 60
IMDB_CACHE_TIMEOUT = 60*60


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()


@app.route("/")
def home():
    process = simplecache.get("process")
    if not process:
        process = Process()
        process.process()
        simplecache.set("process", process, CACHE_TIMEOUT)
    return render_template('home.html',
                           movies=process.movies_group_items.renderer(),
                           tvshows=process.tvshows_group_items.renderer(),
                           mangas=process.manga_group_items.renderer())


@app.route("/movies")
def movies():
    process = simplecache.get("process")
    if not process:
        process = Process()
        process.process()
        simplecache.set("process", process, CACHE_TIMEOUT)
    return render_template('movies.html',
                           movies=process.movies_group_items.renderer())


@app.route("/tvshows")
def tvshows():
    process = simplecache.get("process")
    if not process:
        process = Process()
        process.process()
        simplecache.set("process", process, CACHE_TIMEOUT)
    return render_template('tvshows.html',
                           tvshows=process.tvshows_group_items.renderer())


@app.route("/mangas")
def mangas():
    process = simplecache.get("process")
    if not process:
        process = Process()
        process.process()
        simplecache.set("process", process, CACHE_TIMEOUT)
    return render_template('mangas.html',
                           mangas=process.manga_group_items.renderer())


@app.route("/imdb/<slug>/")
def imdb_rating(slug):
    title = request.args.get('title')
    if title:
        cache_key = u"{}_imdb".format(title)
        imdb = simplecache.get(cache_key)
        if not imdb:
            imdb = Item.fetch_imdb_rating(title)
            simplecache.set(cache_key, imdb, IMDB_CACHE_TIMEOUT)
        if imdb.rating:
            return render_template('imdb_rating.html', imdb=imdb)
    return ''


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run()