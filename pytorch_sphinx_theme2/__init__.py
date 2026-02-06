__version__ = "0.1.0"

import json
import os
import posixpath
import re
import shutil
import subprocess
from pathlib import Path
from uuid import uuid4

from . import custom_directives
from .custom_directives import HAS_SPHINX_GALLERY

# Optional import for tippy glossary support
try:
    from bs4 import BeautifulSoup
    from docutils import nodes

    HAS_TIPPY_DEPS = True
except ImportError:
    HAS_TIPPY_DEPS = False


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



# =============================================================================
# LLM Navigation Guide (llms.txt) support
# =============================================================================


def _generate_llms_txt(app, exception):
    """Generate llms.txt from template and copy to site root after build completes."""
    if exception is not None:
        return  # Don't generate if build failed
    
    if app.builder.name != "html":
        return
    
    # Check if LLM features are disabled
    theme_options = app.config.html_theme_options or {}
    if str(theme_options.get("llm_disabled", "false")).lower() == "true":
        return
    
    # Check for custom llms.txt content first
    custom_content = theme_options.get("llm_custom_llms_txt", "")
    
    if custom_content:
        # Use custom content directly
        content = custom_content
    else:
        # Generate from template
        try:
            from jinja2 import Environment, FileSystemLoader
            
            template_dir = Path(__file__).parent / "templates"
            env = Environment(loader=FileSystemLoader(str(template_dir)))
            template = env.get_template("llms.txt.jinja")
            
            # Gather context for template
            context = {
                "project": app.config.project,
                "version": app.config.version or "latest",
                "master_doc": app.config.root_doc,
                "llm_description": theme_options.get("llm_description", ""),
                "llm_docs_base_url": theme_options.get("llm_docs_base_url", ""),
                "llm_content_types": theme_options.get("llm_content_types", "api-reference, tutorials, guides, examples"),
                "llm_language": theme_options.get("llm_language", "python"),
                "llm_important_pages": theme_options.get("llm_important_pages", ""),
                "llm_key_docs": theme_options.get("llm_key_docs", ""),
            }
            
            content = template.render(**context)
        except Exception as e:
            print(f"Warning: Could not generate llms.txt from template: {e}")
            # Fallback to static file if it exists
            static_path = Path(app.outdir) / "_static" / "llms.txt"
            if static_path.exists():
                shutil.copy2(static_path, Path(app.outdir) / "llms.txt")
            return
    
    # Write to site root
    dest_path = Path(app.outdir) / "llms.txt"
    try:
        dest_path.write_text(content, encoding="utf-8")
        print(f"Generated llms.txt at site root: {dest_path}")
    except Exception as e:
        print(f"Warning: Could not write llms.txt to site root: {e}")


# =============================================================================
# Sphinx-tippy parallel build fix
# =============================================================================
# Problem: sphinx-tippy collects tooltip data during html-page-context (write
# phase), but this data is lost in parallel workers because env-merge-info runs
# during read phase (before data collection).
#
# Solution: Extract glossary terms during doctree-resolved (read phase), store
# in app.env where it merges properly, then write JS files during html-page-context.


def _extract_glossary_terms(app, doctree, docname):
    """Extract glossary terms during read phase for parallel build support."""
    if not HAS_TIPPY_DEPS:
        return

    glossary_page = getattr(app.config, "tippy_glossary_page", "_glossary")
    if docname != glossary_page:
        return

    if not hasattr(app.env, "glossary_terms_for_tippy"):
        app.env.glossary_terms_for_tippy = {}

    for node in doctree.findall(nodes.definition_list_item):
        term_node = node.next_node(nodes.term)
        def_node = node.next_node(nodes.definition)
        if not term_node or not term_node.get("ids"):
            continue

        term_id = term_node["ids"][0]
        paragraphs = [
            c.astext() for c in (def_node.children if def_node else [])
            if isinstance(c, nodes.paragraph)
        ][:2]
        def_html = "".join(f"<p>{p}</p>" for p in paragraphs)
        app.env.glossary_terms_for_tippy[term_id] = (
            f'<dt id="{term_id}">{term_node.astext()}</dt><dd>{def_html}</dd>'
        )


def _merge_glossary_terms(app, env, docnames, other):
    """Merge glossary terms from parallel workers."""
    if not hasattr(env, "glossary_terms_for_tippy"):
        env.glossary_terms_for_tippy = {}
    env.glossary_terms_for_tippy.update(getattr(other, "glossary_terms_for_tippy", {}))


def _write_glossary_tippy_js(app, pagename, templatename, context, doctree):
    """Write tippy JS for glossary links on each page."""
    if not HAS_TIPPY_DEPS or not doctree or app.builder.name != "html":
        return

    glossary_terms = getattr(app.env, "glossary_terms_for_tippy", {})
    body_html = context.get("body", "")
    if not glossary_terms or not body_html:
        return

    # Find glossary links in page
    glossary_page = getattr(app.config, "tippy_glossary_page", "_glossary")
    pattern = re.compile(rf"{re.escape(glossary_page)}\.html#(term-[\w-]+)")
    soup = BeautifulSoup(body_html, "html.parser")

    selector_to_html = {}
    for anchor in soup.find_all("a", href=True):
        match = pattern.search(anchor["href"])
        if match and match.group(1) in glossary_terms:
            term_id = match.group(1)
            page_dir = posixpath.dirname(pagename)
            rel_path = posixpath.relpath(glossary_page, page_dir) if page_dir else glossary_page
            selector_to_html[f'a[href="{rel_path}.html#{term_id}"]'] = glossary_terms[term_id]

    if not selector_to_html:
        return

    # Build tippy props
    tippy_props = getattr(app.config, "tippy_props", {})
    props_str = ", ".join([
        f"placement: '{tippy_props.get('placement', 'auto-start')}'",
        f"maxWidth: {tippy_props.get('maxWidth', 500)}",
        f"interactive: {'true' if tippy_props.get('interactive') else 'false'}",
    ] + ([f"theme: '{tippy_props['theme']}'"] if tippy_props.get("theme") else []))

    # Write JS file
    js_content = f"""selector_to_html = {json.dumps(selector_to_html)}
window.onload = function () {{
    for (const [select, tip_html] of Object.entries(selector_to_html)) {{
        document.querySelectorAll(select).forEach(link => {{
            if (!["headerlink", "sd-stretched-link"].some(c => link.classList.contains(c))) {{
                tippy(link, {{ content: tip_html, allowHTML: true, arrow: true, {props_str} }});
            }}
        }});
    }};
}};
"""
    tippy_dir = Path(app.outdir) / "_static" / "tippy"
    parts = pagename.split("/")
    if len(parts) > 1:
        (tippy_dir / "/".join(parts[:-1])).mkdir(parents=True, exist_ok=True)
    else:
        tippy_dir.mkdir(parents=True, exist_ok=True)

    # Clean old files and write new one
    page_dir = tippy_dir / "/".join(parts[:-1]) if len(parts) > 1 else tippy_dir
    for old in page_dir.glob(f"{parts[-1]}.*.js"):
        old.unlink()

    js_path = page_dir / f"{parts[-1]}.{uuid4()}.js"
    js_path.write_text(js_content, encoding="utf-8")
    app.add_js_file(str(js_path.relative_to(Path(app.outdir) / "_static")), loading_method="defer")


# =============================================================================
# Hierarchical header navigation for dropdown menus
# =============================================================================


def _get_toctree_children(app, docname):
    """Get children of a toctree entry using toctree_includes which handles glob patterns."""
    children = []
    try:
        # Use toctree_includes which properly resolves glob patterns
        toctree_includes = getattr(app.env, 'toctree_includes', {})
        child_docnames = toctree_includes.get(docname, [])
        
        for child_docname in child_docnames:
            if child_docname and child_docname != docname:
                # Get title from env.titles
                child_title = app.env.titles.get(child_docname, child_docname)
                if hasattr(child_title, "astext"):
                    child_title = child_title.astext()
                children.append({
                    "title": str(child_title),
                    "url": child_docname,
                })
    except Exception:
        pass
    return children


def _generate_hierarchical_header_nav(app, pagename):
    """Generate hierarchical header navigation data for dropdown menus."""
    nav_items = []
    
    try:
        root_doc = app.config.root_doc
        
        # Use toctree_includes which properly handles all toctree entries including globs
        toctree_includes = getattr(app.env, 'toctree_includes', {})
        root_children = toctree_includes.get(root_doc, [])
        
        for docname in root_children:
            if not docname:
                continue
                
            # Get the title
            item_title = app.env.titles.get(docname, docname)
            if hasattr(item_title, "astext"):
                item_title = item_title.astext()
            
            # Check if this is the current page or an ancestor
            is_current = (docname == pagename or pagename.startswith(docname.rsplit('/', 1)[0] + "/") if '/' in docname else docname == pagename)
            
            # Get children (subsections) from this document's toctree
            children = _get_toctree_children(app, docname)
            
            nav_items.append({
                "title": str(item_title),
                "url": docname,
                "current": is_current,
                "children": children,
            })
    except Exception:
        pass

    return nav_items


def _add_hierarchical_nav_to_context(app, pagename, templatename, context, doctree):
    """Add hierarchical navigation data to the template context."""
    context["hierarchical_header_nav"] = _generate_hierarchical_header_nav(app, pagename)


# =============================================================================
# Sphinx setup function
# =============================================================================


def setup(app):
    app.add_html_theme("pytorch_sphinx_theme2", get_html_theme_path())
    app.add_config_value("add_last_updated", False, "html")
    app.connect("html-page-context", add_date_info_to_page)

    # Add hierarchical navigation context for dropdown menus
    app.connect("html-page-context", _add_hierarchical_nav_to_context)

    # Configuration for sphinx-tippy parallel build fix
    # tippy_glossary_page: name of the glossary page (without extension)
    app.add_config_value("tippy_glossary_page", "_glossary", "html")

    # Connect sphinx-tippy parallel build fix handlers
    # These fix the issue where tooltip data is lost in parallel workers
    if HAS_TIPPY_DEPS:
        app.connect("doctree-resolved", _extract_glossary_terms)
        app.connect("env-merge-info", _merge_glossary_terms)
        # Write JS immediately during page context (high priority to run early)
        app.connect("html-page-context", _write_glossary_tippy_js, priority=900)

    # Copy llms.txt to site root after build completes
    app.connect("build-finished", _generate_llms_txt)

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
