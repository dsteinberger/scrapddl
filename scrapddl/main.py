import logging

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from werkzeug.wrappers import Response

logger = logging.getLogger(__name__)

from cachelib.simple import SimpleCache

from scrapimdb import ImdbSpider

from scrapddl.process import Process
from scrapddl.settings import IMDB_RATING_ACTIVE, IMDB_RATING_MINIMAL_TOP
from scrapddl.settings import CACHE_TIMEOUT, IMDB_CACHE_TIMEOUT
from scrapddl.settings import ED_DOMAIN
from scrapddl.settings import ZT_DOMAIN, WC_DOMAIN, TR_DOMAIN, AT_DOMAIN
from scrapddl.settings import MOVIES_SECTION_ACTIVE
from scrapddl.settings import TVSHOWS_SECTION_ACTIVE
from scrapddl.settings import MANGAS_SECTION_ACTIVE

from scrapddl.items.items import GroupItem


simplecache: SimpleCache = SimpleCache()


def create_app() -> Flask:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    app = Flask(__name__)
    return app


app = create_app()


@app.context_processor
def settings() -> dict[str, object]:
    return {
        "imdb_rating_active": IMDB_RATING_ACTIVE,
        "movies_section_active": MOVIES_SECTION_ACTIVE,
        "tvshows_section_active": TVSHOWS_SECTION_ACTIVE,
        "mangas_section_active": MANGAS_SECTION_ACTIVE,
        "ed_url": ED_DOMAIN,
        "zt_url": ZT_DOMAIN,
        "wc_url": WC_DOMAIN,
        "tr_url": TR_DOMAIN,
        "at_url": AT_DOMAIN,
    }


@app.route("/")
def home() -> str:
    return render_template('home.html')


@app.route("/refresh")
def refresh() -> Response:
    simplecache.delete("process")
    return redirect(url_for('home'))


def process_section(section: str) -> Process:
    process = simplecache.get("process") or Process()
    if not process.has_process_object(section):
        logger.info("Processing section: %s", section)
        getattr(process, "process_{}".format(section))()
        simplecache.set("process", process, CACHE_TIMEOUT)
    return process


# HOME
# ----


@app.route("/movies-home")
def movies_home() -> str:
    if MOVIES_SECTION_ACTIVE:
        section = "movies"
        process = process_section(section)
        return render_template('js_home.html',
                               section=section,
                               objects_list=process.movies_group_items.renderer())
    return ''


@app.route("/tvshows-home")
def tvshows_home() -> str:
    if TVSHOWS_SECTION_ACTIVE:
        section = "tvshows"
        process = process_section(section)
        return render_template('js_home.html',
                               section=section,
                               objects_list=process.tvshows_group_items.renderer())
    return ''


@app.route("/mangas-home")
def mangas_home() -> str:
    if MANGAS_SECTION_ACTIVE:
        section = "mangas"
        process = process_section(section)
        return render_template('js_home.html',
                               section=section,
                               objects_list=process.mangas_group_items.renderer())
    return ''


@app.route("/movies-refresh")
def movies_refresh() -> Response:
    process = simplecache.get("process")
    if process:
        process.movies_group_items = GroupItem()  # New object instead of mutation
        simplecache.set("process", process, CACHE_TIMEOUT)
    return redirect(url_for('movies_home'))


@app.route("/tvshows-refresh")
def tvshows_refresh() -> Response:
    process = simplecache.get("process")
    if process:
        process.tvshows_group_items = GroupItem()  # New object instead of mutation
        simplecache.set("process", process, CACHE_TIMEOUT)
    return redirect(url_for('tvshows_home'))


@app.route("/mangas-refresh")
def mangas_refresh() -> Response:
    process = simplecache.get("process")
    if process:
        process.mangas_group_items = GroupItem()  # New object instead of mutation
        simplecache.set("process", process, CACHE_TIMEOUT)
    return redirect(url_for('mangas_home'))


# SECTION
# -------


@app.route("/movies")
def movies() -> str:
    section = "movies"
    process = process_section(section)
    return render_template('movies.html',
                           movies=process.movies_group_items.renderer())



@app.route("/tvshows")
def tvshows() -> str:
    section = "tvshows"
    process = process_section(section)
    return render_template('tvshows.html',
                           tvshows=process.tvshows_group_items.renderer())


@app.route("/mangas")
def mangas() -> str:
    section = "mangas"
    process = process_section(section)
    return render_template('mangas.html',
                           mangas=process.mangas_group_items.renderer())


# IMDB
# ----

class Imdb:
    def __init__(self, rating: str | None, url: str) -> None:
        self.rating = rating
        self.url = url
        self.is_top: bool = False

@app.route("/imdb/<slug>/")
def imdb_rating(slug: str) -> str:
    if IMDB_RATING_ACTIVE:
        title = request.args.get('title')
        if title:
            cache_key = f"{title}_imdb"
            imdb = simplecache.get(cache_key)
            if not imdb:
                try:
                    spider = ImdbSpider(title)
                except Exception as e:
                    logger.error("IMDB spider error: %s", e)
                    return ''
                try:
                    rating = spider.get_rating()
                except Exception:
                    logger.warning("No IMDB rating found for: %s", title)
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
def static_proxy(path: str) -> Response:
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run()
