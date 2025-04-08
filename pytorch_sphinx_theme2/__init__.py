__version__ = "0.1.0"

import json
import os
import re
import subprocess 
from pathlib import Path

from . import custom_directives
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

def get_git_dates(file_path):
    """Get creation and last update dates for a file."""
    try:
        # Get last update date
        git_command = [
            "git", "log", "-1", "--date=format:%B %d, %Y", 
            "--format=%ad", "--", file_path
        ]
        last_updated = subprocess.check_output(git_command).decode().strip()
        
        # Get creation date
        git_command = [
            "git", "log", "--reverse", "--diff-filter=A", "--date=format:%B %d, %Y",
            "--format=%ad", "-1", "--", file_path
        ]
        created_on = subprocess.check_output(git_command).decode().strip()
        
        # Check if dates are empty and provide defaults
        if not created_on:
            created_on = "Unknown"
        if not last_updated:
            last_updated = "Unknown"
            
        return created_on, last_updated
    except Exception as e:
        print(f"Git date error for {file_path}: {e}")
        return "Unknown", "Unknown"

def html_page_context(app, pagename, templatename, context, doctree):
    if doctree is None:
        return
    
    paths_to_skip = context.get("date_info", {}).get("paths_to_skip", [])
    if any(pagename == path.rstrip('/') or pagename.startswith(path.rstrip('/') + '/') for path in paths_to_skip):
        return

    source_file = context.get('sourcename')
    if source_file:
        # Remove the .txt extension that Sphinx adds
        if source_file.endswith('.txt'):
            source_file = source_file[:-4]

        # Get the full path to the source file
        source_dir = app.srcdir if hasattr(app, 'srcdir') else ''
        full_source_path = os.path.join(source_dir, source_file)
        
        try:
            created_on, last_updated = get_git_dates(full_source_path)
            print(f"Got dates for {full_source_path}: {created_on}, {last_updated}")
            
            # Only add date info if we have actual dates
            if created_on != "Unknown" and last_updated != "Unknown":
                body = context.get('body', '')
                h1_pattern = r'<h1([^>]*)>(.*?)</h1>'
                match = re.search(h1_pattern, body)
                if match:
                    date_info = f'<p class="date-info-last-verified" style="color: #6c6c6d; font-size: small;">Created on: {created_on} | Last updated: {last_updated}</p>'
                    context['body'] = re.sub(h1_pattern, r'<h1\1>\2</h1>\n' + date_info, body, count=1)
            
        except Exception as e:
            print(f"Error getting dates for {full_source_path}: {e}")


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

    app.connect('html-page-context', html_page_context)
    print("Registered build-finished event handler")

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
