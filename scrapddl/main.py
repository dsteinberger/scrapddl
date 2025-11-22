from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

from cachelib.simple import SimpleCache

from scrapimdb import ImdbSpider

from process import Process
from settings import IMDB_RATING_ACTIVE
from settings import IMDB_RATING_MINIMAL_TOP
from settings import ED_DOMAIN, UA_DOMAIN
from settings import ZT_DOMAIN, WC_DOMAIN
from settings import MOVIES_SECTION_ACTIVE
from settings import TVSHOWS_SECTION_ACTIVE
from settings import MANGAS_SECTION_ACTIVE

from items.items import Item


simplecache = SimpleCache()
CACHE_TIMEOUT = 60
IMDB_CACHE_TIMEOUT = 0


def create_app():
    app = Flask(__name__)
    return app


app = create_app()


@app.context_processor
def settings():
    return {
        "imdb_rating_active": IMDB_RATING_ACTIVE,
        "movies_section_active": MOVIES_SECTION_ACTIVE,
        "tvshows_section_active": TVSHOWS_SECTION_ACTIVE,
        "mangas_section_active": MANGAS_SECTION_ACTIVE,
        "ed_url": ED_DOMAIN,
        "zt_url": ZT_DOMAIN,
        "wc_url": WC_DOMAIN,
        "ua_url": UA_DOMAIN,
    }


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/refresh")
def refresh():
    simplecache.delete("process")
    return redirect(url_for('home'))


def process_section(section):
    process = simplecache.get("process") or Process()
    if not process.has_process_object(section):
        print(f"######  PROCESS : {section}")
        getattr(process, "process_{}".format(section))()
        simplecache.set("process", process, CACHE_TIMEOUT)
    return process


# HOME
# ----


@app.route("/movies-home")
def movies_home():
    if MOVIES_SECTION_ACTIVE:
        section = "movies"
        process = process_section(section)
        return render_template('js_home.html',
                               section=section,
                               objects_list=process.movies_group_items.renderer())
    return ''


@app.route("/tvshows-home")
def tvshows_home():
    if TVSHOWS_SECTION_ACTIVE:
        section = "tvshows"
        process = process_section(section)
        return render_template('js_home.html',
                               section=section,
                               objects_list=process.tvshows_group_items.renderer())
    return ''


@app.route("/mangas-home")
def mangas_home():
    if MANGAS_SECTION_ACTIVE:
        section = "mangas"
        process = process_section(section)
        return render_template('js_home.html',
                               section=section,
                               objects_list=process.mangas_group_items.renderer())
    return ''


@app.route("/movies-refresh")
def movies_refresh():
    process = simplecache.get("process")
    if process:
        process.movies_group_items.items = []
        simplecache.set("process", process, CACHE_TIMEOUT)
    return redirect(url_for('movies_home'))


@app.route("/tvshows-refresh")
def tvshows_refresh():
    process = simplecache.get("process")
    if process:
        process.tvshows_group_items.items = []
        simplecache.set("process", process, CACHE_TIMEOUT)
    return redirect(url_for('tvshows_home'))


@app.route("/mangas-refresh")
def mangas_refresh():
    process = simplecache.get("process")
    if process:
        process.mangas_group_items.items = []
        simplecache.set("process", process, CACHE_TIMEOUT)
    return redirect(url_for('mangas_home'))


# SECTION
# -------


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


# IMDB
# ----

class Imdb(object):
    def __init__(self, rating, url):
        self.rating = rating
        self.url = url

@app.route("/imdb/<slug>/")
def imdb_rating(slug):
    if IMDB_RATING_ACTIVE:
        title = request.args.get('title')
        if title:
            cache_key = f"{title}_imdb"
            imdb = simplecache.get(cache_key)
            if not imdb:
                try:
                    spider = ImdbSpider(title)
                except Exception as e:
                    print(f"ERROR - {e}")
                    return ''
                try:
                    rating = spider.get_rating()
                except Exception:
                    print(f"WARNING - no rating for: {title}")
                    rating = None
                imdb = Imdb(rating, spider.get_link())
                simplecache.set(cache_key, imdb, IMDB_CACHE_TIMEOUT)
            if imdb.rating:
                rating = float(imdb.rating)
                if rating >= IMDB_RATING_MINIMAL_TOP:
                    imdb.is_top = True
                else:
                    imdb.is_top = False
                return render_template('___imdb_rating.html', imdb=imdb)
    return ''


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run()