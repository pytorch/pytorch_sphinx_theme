__version__ = "0.1.0"

import json
import os
import re
from pathlib import Path

from . import custom_directives
from .add_last_verified import add_dates_to_html
from .custom_directives import HAS_SPHINX_GALLERY


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

            # Use regex to extract the dictionary content
            match = re.search(r"external_urls\s*=\s*({.*?})", content, re.DOTALL)
            if match:
                external_urls_str = match.group(1)

                try:
                    # Parse the dictionary string
                    local_vars = {}
                    exec("external_urls = " + external_urls_str, {}, local_vars)
                    external_urls = local_vars["external_urls"]
                    print(f"Parsed external_urls: {list(external_urls.keys())[:5]}")
                except Exception as e:
                    print(f"Error parsing external_urls: {e}")
            else:
                print("No dictionary found in template")

    # Get links from JSON file
    links_path = os.path.join(os.path.dirname(__file__), "links.json")
    links = {}
    if os.path.exists(links_path):
        try:
            with open(links_path) as f:
                links = json.load(f)
        except json.JSONDecodeError:
            pass

    result = {"external_urls": external_urls, **links}
    return result


def on_build_finished(app, exception):
    print("\n\n==== ON BUILD FINISHED CALLED ====\n\n")
    if exception is None and app.builder.name == "html":
        build_dir = app.outdir
        config = app.config.html_context.get("date_info", {})
        enabled = config.get("enabled", True)
        paths_to_skip = config.get("paths_to_skip", [])
        source_to_build_mapping = config.get("source_to_build_mapping", {"": ""})

        print(f"Build directory: {build_dir}")
        print(f"Date info enabled: {enabled}")
        print(f"Paths to skip: {paths_to_skip}")
        print(f"Source to build mapping: {source_to_build_mapping}")

        add_dates_to_html(build_dir, paths_to_skip, source_to_build_mapping, enabled)
        print("Finished adding dates to HTML files.")


def setup(app):
    app.add_html_theme("pytorch_sphinx_theme2", get_html_theme_path())

    if HAS_SPHINX_GALLERY:
        app.add_directive("includenodoc", custom_directives.IncludeDirective)
        app.add_directive("galleryitem", custom_directives.GalleryItemDirective)
        app.add_directive(
            "customgalleryitem", custom_directives.CustomGalleryItemDirective
        )
        app.add_directive("customcarditem", custom_directives.CustomCardItemDirective)
        app.add_directive(
            "customcalloutitem", custom_directives.CustomCalloutItemDirective
        )

    app.connect("build-finished", on_build_finished)
    print("Registered build-finished event handler")

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
