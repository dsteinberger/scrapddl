from flask import Flask
from flask import render_template, url_for

from flask_bootstrap import Bootstrap

from spiders.extreme_down import ExtremDownSpider


def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

app = create_app()


@app.route("/")
def home():
    extrem_down = ExtremDownSpider()
    group_items = extrem_down.parse()

    return render_template('home.html', movies=group_items.renderer())


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run()