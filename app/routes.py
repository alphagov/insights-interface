import json
import os
import markdown

from flask import render_template
from werkzeug.exceptions import NotFound

from app import app, utils

ROOT_DIR = os.getcwd()

@app.route("/")
def index():
    components = os.listdir("govuk_components")
    components.sort()
    content_dir = f'{ROOT_DIR}/app/content'
    print([page_.path for page_ in utils._get_pages(content_dir)])
    return render_template("index.html", components=components, pages=utils._get_pages(content_dir))

@app.route(f'/<requested_page>')
def _render_page(requested_page):
    for page_ in utils._get_pages(f'{ROOT_DIR}/app/content'):
        if requested_page == page_.name:
            #return page_.render()
            return render_template('template.html', toc=page_.toc, page_content=page_.render())


@app.route("/components/<string:component>")
def component(component):
    try:
        with open("govuk_components/{}/fixtures.json".format(component)) as json_file:
            fixtures = json.load(json_file)
    except FileNotFoundError:
        raise NotFound

    return render_template("component.html", fixtures=fixtures)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server(error):
    return render_template("500.html"), 500
