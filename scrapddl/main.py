from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap

from werkzeug.contrib.cache import SimpleCache

from process import Process

from items.items import Item


simplecache = SimpleCache()
CACHE_TIMEOUT = 60
IMDB_CACHE_TIMEOUT = 0


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/refresh")
def refresh():
    simplecache.clear()
    return render_template('home.html')


def process_section(section):
    process = simplecache.get("process") or Process()
    if not process.has_process_object(section):
        print u"######  PROCESS : {}".format(section)
        getattr(process, "process_{}".format(section))()
        simplecache.set("process", process, CACHE_TIMEOUT)
    return process


@app.route("/movies-home")
def movies_home():
    section = "movies"
    process = process_section(section)
    return render_template('js_home.html',
                           section=section,
                           objects_list=process.movies_group_items.renderer())


@app.route("/tvshows-home")
def tvshows_home():
    section = "tvshows"
    process = process_section(section)
    return render_template('js_home.html',
                           section=section,
                           objects_list=process.tvshows_group_items.renderer())


@app.route("/mangas-home")
def mangas_home():
    section = "mangas"
    process = process_section(section)
    return render_template('js_home.html',
                           section=section,
                           objects_list=process.mangas_group_items.renderer())


@app.route("/movies")
def movies():
    section = "movies"
    process = process_section(section)
    return render_template('movies.html',
                           movies=process.movies_group_items.renderer())



@app.route("/tvshows")
def tvshows():
    section = "tvshows"
    process = process_section(section)
    return render_template('tvshows.html',
                           tvshows=process.tvshows_group_items.renderer())


@app.route("/mangas")
def mangas():
    section = "mangas"
    process = process_section(section)
    return render_template('mangas.html',
                           mangas=process.mangas_group_items.renderer())


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
            return render_template('___imdb_rating.html', imdb=imdb)
    return ''


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run()