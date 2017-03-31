from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap

from process import Process

from cache import cached
from items.items import Item


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()


@app.route("/")
@cached()
def home():
    process = Process()
    process.process()
    return render_template('home.html',
                           movies=process.movies_group_items.renderer(),
                           tvshows=process.tvshows_group_items.renderer(),
                           mangas=process.manga_group_items.renderer())


@app.route("/imdb/<slug>/")
def imdb_rating(slug):
    title = request.args.get('title')
    imdb = Item.fetch_imdb_rating(title)
    if imdb.rating:
        return render_template('imdb_rating.html', imdb=imdb)
    return ''


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run()