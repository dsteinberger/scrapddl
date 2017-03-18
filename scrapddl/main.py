from flask import Flask
from flask import render_template

from flask_bootstrap import Bootstrap

from process import Process
from cache import cached


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


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run()