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
            "git",
            "log",
            "-1",
            "--date=format:%b %d, %Y",
            "--format=%ad",
            "--",
            file_path,
        ]
        last_updated = subprocess.check_output(git_command).decode().strip()

        # Get creation date
        git_command = [
            "git",
            "log",
            "--follow",
            "--format=%ad",
            "--date=format:%b %d, %Y",
            "--",
            file_path,
        ]
        creation_output = (
            subprocess.check_output(git_command).decode().strip().split("\n")
        )
        created_on = creation_output[-1] if creation_output else "Unknown"

        # Check if dates are empty and provide defaults
        if not created_on:
            created_on = "Unknown"
        if not last_updated:
            last_updated = "Unknown"

        return created_on, last_updated
    except Exception as e:
        print(f"Git date error for {file_path}: {e}")
        return "Unknown", "Unknown"


def add_date_info_to_page(app, pagename, templatename, context, doctree):
    if not getattr(app.config, "add_last_updated", False):
        return

    if doctree is None:
        return

    # Check if date info is already present in the body
    body = context.get("body", "")
    if '<p class="date-info-last-verified"' in body:
        return  # Date info already inserted, skip

    paths_to_skip = ["_static", "_images", "_templates"] + context.get(
        "date_info", {}
    ).get("paths_to_skip", [])
    if any(
        pagename == path.rstrip("/") or pagename.startswith(path.rstrip("/") + "/")
        for path in paths_to_skip
    ):
        return

    source_file = context.get("sourcename")
    if source_file:
        # Remove the .txt extension that Sphinx adds
        if source_file.endswith(".txt"):
            source_file = source_file[:-4]

        # Get the full path to the source file
        source_dir = app.srcdir if hasattr(app, "srcdir") else ""
        full_source_path = os.path.join(source_dir, source_file)

        try:
            created_on, last_updated = get_git_dates(full_source_path)

            # Add dates to context to use in templates
            context["doc_created"] = created_on
            context["doc_updated"] = last_updated

            # Only add date info if we have actual dates
            if created_on != "Unknown" and last_updated != "Unknown":
                body = context.get("body", "")
                h1_pattern = r"<h1([^>]*)>(.*?)</h1>"
                match = re.search(h1_pattern, body)
                if match:
                    date_info = f'<p class="date-info-last-verified" style="color: #6c6c6d; font-size: small;">Created On: {created_on} | Last Updated On: {last_updated}</p>'
                    context["body"] = re.sub(
                        h1_pattern, r"<h1\1>\2</h1>\n" + date_info, body, count=1
                    )

        except Exception as e:
            print(f"Error getting dates for {full_source_path}: {e}")



def setup(app):
    app.add_html_theme("pytorch_sphinx_theme2", get_html_theme_path())
    app.add_config_value("add_last_updated", False, "html")
    # Use config-inited which fires earlier than builder-inited
    app.connect("html-page-context", add_date_info_to_page)

    # Fix sphinx-tippy for parallel builds (-j auto)
    # The problem: sphinx_tippy collects tooltip data during html-page-context
    # (write phase), but this data is lost in parallel workers because
    # env-merge-info runs during read phase (before data collection).
    #
    # Solution: Extract glossary terms during doctree-resolved (read phase),
    # store in app.env where it merges properly, then write JS files for
    # glossary tooltips during html-page-context (immediately, not deferred).
    try:
        from docutils import nodes
        from uuid import uuid4
        from bs4 import BeautifulSoup

        print("[tippy-fix] All imports successful, enabling glossary tooltip fix")

        def extract_glossary_terms(app, doctree, docname):
            """Extract glossary terms during read phase for parallel build support."""
            # Check for glossary docnames (with or without underscore prefix)
            glossary_docnames = ["_glossary", "glossary"]
            if docname not in glossary_docnames:
                return

            print(f"[tippy-fix] Processing glossary document: {docname}")

            if not hasattr(app.env, "glossary_terms_for_tippy"):
                app.env.glossary_terms_for_tippy = {}

            terms_found = 0

            # Method 1: Standard RST glossary - look for definition_list_item nodes
            for node in doctree.findall(nodes.definition_list_item):
                term_node = node.next_node(nodes.term)
                def_node = node.next_node(nodes.definition)

                if term_node is None:
                    continue

                term_ids = term_node.get("ids", [])
                if not term_ids:
                    continue

                term_id = term_ids[0]
                term_text = term_node.astext()

                def_html = ""
                if def_node is not None:
                    paragraphs = []
                    for child in def_node.children:
                        if isinstance(child, nodes.paragraph):
                            paragraphs.append(child.astext())
                            if len(paragraphs) >= 2:
                                break
                    def_html = "".join(f"<p>{p}</p>" for p in paragraphs)

                term_html = f'<dt id="{term_id}">{term_text}</dt><dd>{def_html}</dd>'
                app.env.glossary_terms_for_tippy[term_id] = term_html
                terms_found += 1

            # Method 2: Also check for term nodes directly (MyST may structure differently)
            if terms_found == 0:
                for term_node in doctree.findall(nodes.term):
                    term_ids = term_node.get("ids", [])
                    if not term_ids:
                        continue

                    term_id = term_ids[0]
                    term_text = term_node.astext()

                    # Find parent definition_list_item to get definition
                    parent = term_node.parent
                    def_html = ""
                    if parent is not None:
                        for sibling in parent.children:
                            if isinstance(sibling, nodes.definition):
                                paragraphs = []
                                for child in sibling.children:
                                    if isinstance(child, nodes.paragraph):
                                        paragraphs.append(child.astext())
                                        if len(paragraphs) >= 2:
                                            break
                                def_html = "".join(f"<p>{p}</p>" for p in paragraphs)
                                break

                    term_html = f'<dt id="{term_id}">{term_text}</dt><dd>{def_html}</dd>'
                    app.env.glossary_terms_for_tippy[term_id] = term_html
                    terms_found += 1

            print(f"[tippy-fix] Extracted {terms_found} glossary terms from {docname}")

        def merge_glossary_terms(app, env, docnames, other):
            """Merge glossary terms from parallel workers."""
            if not hasattr(env, "glossary_terms_for_tippy"):
                env.glossary_terms_for_tippy = {}
            other_terms = getattr(other, "glossary_terms_for_tippy", {})
            if other_terms:
                print(f"[tippy-fix] Merging {len(other_terms)} glossary terms from worker")
            env.glossary_terms_for_tippy.update(other_terms)

        def write_glossary_tippy_js(app, pagename, templatename, context, doctree):
            """Write tippy JS immediately during page context for glossary links."""
            if not doctree or app.builder.name != "html":
                return

            glossary_terms = getattr(app.env, "glossary_terms_for_tippy", {})
            if not glossary_terms:
                return

            body_html = context.get("body", "")
            if not body_html:
                return

            soup = BeautifulSoup(body_html, "html.parser")

            selector_to_html = {}
            glossary_link_pattern = re.compile(r"_glossary\.html#(term-[\w-]+)")

            for anchor in soup.find_all("a", href=True):
                href = anchor.get("href", "")
                match = glossary_link_pattern.search(href)
                if match:
                    term_id = match.group(1)
                    if term_id in glossary_terms:
                        page_dir = os.path.dirname(pagename)
                        if page_dir:
                            rel_glossary = os.path.relpath("_glossary", page_dir)
                        else:
                            rel_glossary = "_glossary"
                        selector = f'a[href="{rel_glossary}.html#{term_id}"]'
                        selector_to_html[selector] = glossary_terms[term_id]

            if not selector_to_html:
                return

            print(f"[tippy-fix] Writing JS for {pagename} with {len(selector_to_html)} glossary links")

            tippy_props = getattr(app.config, "tippy_props", {})
            props = {
                "placement": f"'{tippy_props.get('placement', 'auto-start')}'",
                "maxWidth": str(tippy_props.get("maxWidth", 500)),
                "interactive": "true"
                if tippy_props.get("interactive", False)
                else "false",
            }
            theme = tippy_props.get("theme")
            if theme:
                props["theme"] = f"'{theme}'"

            tippy_props_str = ", ".join(f"{k}: {v}" for k, v in props.items())

            js_content = f'''selector_to_html = {json.dumps(selector_to_html)}
skip_classes = ["headerlink", "sd-stretched-link"]

window.onload = function () {{
    for (const [select, tip_html] of Object.entries(selector_to_html)) {{
        const links = document.querySelectorAll(` ${{select}}`);
        for (const link of links) {{
            if (skip_classes.some(c => link.classList.contains(c))) {{
                continue;
            }}
            tippy(link, {{
                content: tip_html,
                allowHTML: true,
                arrow: true,
                {tippy_props_str},
            }});
        }};
    }};
    console.log("tippy glossary tips loaded!");
}};
'''

            parts = pagename.split("/")
            tippy_dir = Path(app.outdir) / "_static" / "tippy"
            tippy_dir.mkdir(parents=True, exist_ok=True)

            if len(parts) > 1:
                page_tippy_dir = tippy_dir / "/".join(parts[:-1])
                page_tippy_dir.mkdir(parents=True, exist_ok=True)
            else:
                page_tippy_dir = tippy_dir

            for old_file in page_tippy_dir.glob(f"{parts[-1]}.*.js"):
                old_file.unlink()

            js_filename = f"{parts[-1]}.{uuid4()}.js"
            if len(parts) > 1:
                js_path = tippy_dir / "/".join(parts[:-1]) / js_filename
            else:
                js_path = tippy_dir / js_filename

            js_path.write_text(js_content, encoding="utf-8")

            rel_js_path = js_path.relative_to(Path(app.outdir) / "_static")
            app.add_js_file(str(rel_js_path), loading_method="defer")

        app.connect("doctree-resolved", extract_glossary_terms)
        app.connect("env-merge-info", merge_glossary_terms)
        app.connect("html-page-context", write_glossary_tippy_js, priority=900)

    except ImportError as e:
        print(f"[tippy-fix] DISABLED - missing dependency: {e}")

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

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
