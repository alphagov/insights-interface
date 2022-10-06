import json
import os
import markdown
import os

from werkzeug.exceptions import NotFound
from flask import Flask,url_for,render_template,request,render_template_string
from app import app

app = Flask(__name__)

ROOT_DIR = os.getcwd()
print(ROOT_DIR)
print(f'{ROOT_DIR}/app/content/')

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

def _get_pages(root_dir):
    pages = []
    for dir_, _, files in os.walk(f'{ROOT_DIR}/app/content/'):
        for file in files:
            pages.append(page(dir_, file))
    return pages

@app.route('/')
def _render_home_page():
    toc = ['<ul>']
    toc.extend([f'<li><a href=\'{page_.name}\'>{page_.toc_tokens[0]["name"]}</a></li>' for page_ in _get_pages(ROOT_DIR)])
    toc.append('</ul>')
    print(toc)
    return render_template('template.html', toc=''.join(toc))

@app.route(f'/<requested_page>')
def _render_page(requested_page):
    for page_ in _get_pages(ROOT_DIR):
        if requested_page == page_.name:
            return render_template('template.html', toc=page_.toc, content=page_.html)

# from app import app
#
#
# @app.route("/")
# def index():
#     components = os.listdir("govuk_components")
#     components.sort()
#
#     return render_template("index.html", components=components)
#
#
# @app.route("/components/<string:component>")
# def component(component):
#     try:
#         with open("govuk_components/{}/fixtures.json".format(component)) as json_file:
#             fixtures = json.load(json_file)
#     except FileNotFoundError:
#         raise NotFound
#
#     return render_template("component.html", fixtures=fixtures)
#
#
# @app.errorhandler(404)
# def not_found(error):
#     return render_template("404.html"), 404
#
#
# @app.errorhandler(500)
# def internal_server(error):
#     return render_template("500.html"), 500
