import os
import markdown
from flask import render_template_string

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
    def render(self):
        prerendered_body = render_template_string(self.raw_text)
        return markdown.markdown(prerendered_body, extensions=['tables', 'footnotes', 'toc'])

def _get_pages(directory):
    pages = []
    for dir_, _, files in os.walk(directory): 
        for file in files: 
            pages.append(page(dir_, file))
    return pages