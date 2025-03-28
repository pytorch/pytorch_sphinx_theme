__version__ = "0.1.0"

import json
import os
import re
from pathlib import Path
from . import custom_directives

def get_html_theme_path():
    return os.path.dirname(os.path.abspath(__file__))


def get_theme_variables():
    """Return theme variables dictionary from Jinja template and links.json."""
    # Get external_urls from Jinja template (existing functionality)
    external_urls = {}
    template_path = os.path.join(os.path.dirname(__file__), "theme_variables.jinja")
    if os.path.exists(template_path):
        with open(template_path) as f:
            content = f.read()
            # Extract the dictionary from the Jinja template
            match = re.search(r"{%- set external_urls = (.*?) -%}", content, re.DOTALL)
            if match:
                # Convert the dictionary string to a Python dictionary
                external_urls_str = match.group(1)
                local_vars = {}
                exec("external_urls = " + external_urls_str, {}, local_vars)
                external_urls = local_vars["external_urls"]

    # Get links from JSON file
    links_path = os.path.join(os.path.dirname(__file__), "links.json")
    links = {}
    if os.path.exists(links_path):
        try:
            with open(links_path) as f:
                links = json.load(f)
        except json.JSONDecodeError:
            pass

    # Combine both sources
    return {"external_urls": external_urls, **links}


def setup(app):
    app.add_html_theme("pytorch_sphinx_theme2", get_html_theme_path())
    app.add_directive('includenodoc', directives.IncludeDirective)
    app.add_directive('galleryitem', directives.GalleryItemDirective)
    app.add_directive('customgalleryitem', directives.CustomGalleryItemDirective)
    app.add_directive('customcarditem', directives.CustomCardItemDirective)
    app.add_directive('customcalloutitem', directives.CustomCalloutItemDirective)

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
