import json
import os
import markdown

from flask import render_template
from werkzeug.exceptions import NotFound

from app import app

ROOT_DIR = os.getcwd()

class page:
    def __init__(self, dir_, file):
        self.path = os.path.join(dir_, file)
        self.name = os.path.splitext(file)[0]
        self.ext = os.path.splitext(file)[1]
        with open(self.path) as f: 
                self.raw_text = f.read()

        md = markdown.Markdown(extensions=['tables', 'footnotes', 'toc'])
        self.html = md.convert(self.raw_text)
        self.toc = md.toc 
        self.toc_tokens = md.toc_tokens

def _get_pages(directory):
    pages = []
    for dir_, _, files in os.walk(directory): 
        for file in files: 
            pages.append(page(dir_, file))
    return pages


@app.route("/")
def index():
    components = os.listdir("govuk_components")
    components.sort()
    content_dir = f'{ROOT_DIR}/app/content'
    print([page_.path for page_ in _get_pages(content_dir)])
    return render_template("index.html", components=components, pages=_get_pages(content_dir))

@app.route(f'/<requested_page>')
def _render_page(requested_page):
    for page_ in _get_pages(f'{ROOT_DIR}/app/content'):
        if requested_page == page_.name:
            return render_template('template.html', toc=page_.toc, page_content=page_.html)


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
