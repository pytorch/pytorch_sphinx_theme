__version__ = "0.4.9"

import json
import os
import posixpath
import re
import subprocess
from pathlib import Path
from uuid import uuid4

from . import custom_directives
from .custom_directives import HAS_SPHINX_GALLERY
from .llm_generation import (
    _generate_llms_txt,
    _generate_md_files,
    _generate_llms_full_txt,
    _html_to_markdown,
)

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
                    date_info = f'<p class="date-info-last-verified" data-pagefind-ignore style="color: #6c6c6d; font-size: small;">Created On: {created_on} | Last Updated On: {last_updated}</p>'
                    context["body"] = re.sub(
                        h1_pattern, r"<h1\1>\2</h1>\n" + date_info, body, count=1
                    )

        except Exception as e:
            print(f"Error getting dates for {full_source_path}: {e}")


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
            c.astext()
            for c in (def_node.children if def_node else [])
            if isinstance(c, nodes.paragraph)
        ][:2]
        def_html = "".join(f"<p>{p}</p>" for p in paragraphs)
        app.env.glossary_terms_for_tippy[term_id] = (
            f'<dt id="{term_id}">{term_node.astext()}</dt><dd>{def_html}</dd>'
        )


def _merge_toctree_entries(app, env, docnames, other):
    """Merge root toctree entries from parallel workers."""
    other_entries = getattr(other, "_root_toctree_entries", [])
    if other_entries and not getattr(env, "_root_toctree_entries", []):
        env._root_toctree_entries = other_entries


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
            rel_path = (
                posixpath.relpath(glossary_page, page_dir)
                if page_dir
                else glossary_page
            )
            selector_to_html[f'a[href="{rel_path}.html#{term_id}"]'] = glossary_terms[
                term_id
            ]

    if not selector_to_html:
        return

    # Build tippy props
    tippy_props = getattr(app.config, "tippy_props", {})
    props_str = ", ".join(
        [
            f"placement: '{tippy_props.get('placement', 'auto-start')}'",
            f"maxWidth: {tippy_props.get('maxWidth', 500)}",
            f"interactive: {'true' if tippy_props.get('interactive') else 'false'}",
        ]
        + ([f"theme: '{tippy_props['theme']}'"] if tippy_props.get("theme") else [])
    )

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
    app.add_js_file(
        str(js_path.relative_to(Path(app.outdir) / "_static")), loading_method="defer"
    )


# =============================================================================
# Hierarchical header navigation for dropdown menus
# =============================================================================


def _get_toctree_children(app, docname):
    """Get children of a toctree entry using toctree_includes which handles glob patterns."""
    children = []
    try:
        # Use toctree_includes which properly resolves glob patterns
        toctree_includes = getattr(app.env, "toctree_includes", {})
        child_docnames = toctree_includes.get(docname, [])

        for child_docname in child_docnames:
            if child_docname and child_docname != docname:
                # Get title from env.titles
                child_title = app.env.titles.get(child_docname, child_docname)
                if hasattr(child_title, "astext"):
                    child_title = child_title.astext()
                children.append(
                    {
                        "title": str(child_title),
                        "url": child_docname,
                    }
                )
    except Exception:
        pass
    return children


def _cache_root_toctree_entries(app, doctree):
    """Cache toctree entries from the root doc during the read phase.

    Called via doctree-read (not doctree-resolved) so this runs in the main
    process before parallel write workers are spawned. The cached data on
    app.env gets pickled and distributed to all workers.
    """
    docname = app.env.docname
    if docname != app.config.root_doc:
        return

    from sphinx import addnodes

    entries = []
    for toctree_node in doctree.findall(addnodes.toctree):
        for title, ref in toctree_node.get("entries", []):
            if ref:
                is_external = ref.startswith(("http://", "https://", "/"))
                entries.append((title, ref, is_external))

    app.env._root_toctree_entries = entries


def _get_toctree_entries_from_doctree(app, docname):
    """Get all toctree entries from a document, including external URLs.

    Returns a list of tuples: (title, reference, is_external)
    Uses entries cached during the read phase by _cache_root_toctree_entries.
    """
    return getattr(app.env, "_root_toctree_entries", [])


def _generate_hierarchical_header_nav(app, pagename):
    """Generate hierarchical header navigation data for dropdown menus.

    Includes:
    - Toctree entries from the root document (including external URLs)
    - External links from html_theme_options["external_links"]
    """
    nav_items = []

    try:
        root_doc = app.config.root_doc

        # Get toctree entries from the root document (includes external URLs)
        toctree_entries = _get_toctree_entries_from_doctree(app, root_doc)

        for entry_title, ref, is_external in toctree_entries:
            if not ref:
                continue

            if is_external:
                # External URL - use the provided title or the URL itself
                item_title = entry_title if entry_title else ref
                nav_items.append(
                    {
                        "title": str(item_title),
                        "url": ref,
                        "current": False,
                        "children": [],
                        "external": True,
                    }
                )
            else:
                # Internal document
                docname = ref

                # Get the title - use explicit title if provided, otherwise get from env
                if entry_title:
                    item_title = entry_title
                else:
                    item_title = app.env.titles.get(docname, docname)
                    if hasattr(item_title, "astext"):
                        item_title = item_title.astext()

                # Check if this is the current page or an ancestor
                is_current = (
                    docname == pagename
                    or pagename.startswith(docname.rsplit("/", 1)[0] + "/")
                    if "/" in docname
                    else docname == pagename
                )

                # Get children (subsections) from this document's toctree
                children = _get_toctree_children(app, docname)

                nav_items.append(
                    {
                        "title": str(item_title),
                        "url": docname,
                        "current": is_current,
                        "children": children,
                        "external": False,
                    }
                )

        # Also include external_links from html_theme_options
        theme_options = getattr(app.config, "html_theme_options", {}) or {}
        external_links = theme_options.get("external_links", [])
        for link in external_links:
            if isinstance(link, dict) and link.get("url"):
                nav_items.append(
                    {
                        "title": str(link.get("name", link["url"])),
                        "url": link["url"],
                        "current": False,
                        "children": [],
                        "external": True,
                    }
                )
    except Exception:
        pass

    return nav_items


def _add_hierarchical_nav_to_context(app, pagename, templatename, context, doctree):
    """Add hierarchical navigation data to the template context."""
    context["hierarchical_header_nav"] = _generate_hierarchical_header_nav(
        app, pagename
    )


def _extract_page_meta_description(app, pagename, templatename, context, doctree):
    """Extract the meta description from metatags and add it to context for LLM tags.

    The .. meta:: directive in RST generates HTML meta tags in the 'metatags' context
    variable. This function parses that HTML to extract the description value and
    makes it available as 'page_meta_description' for use in templates.
    """
    metatags = context.get("metatags", "")
    if not metatags:
        return

    # Parse the metatags HTML to extract the description
    # metatags contains raw HTML like: <meta content="..." name="description" />
    import re

    # Match format: content="..." name="description" (Sphinx typically uses this order)
    pattern = r'<meta[^>]*content="([^"]*)"[^>]*name="description"[^>]*/?\s*>'
    match = re.search(pattern, metatags, re.IGNORECASE)
    if match:
        context["page_meta_description"] = match.group(1)


def _select_template_from_meta(app, pagename, templatename, context, doctree):
    """Select a custom template based on meta directive in the page.

    This allows pages to specify a custom template via the .. meta:: directive:

    .. meta::
       :template: landing

    Available templates:
    - landing: Landing page layout with left sidebar only and optional search bar

    The template name maps to templates/{name}.html in the theme.
    """
    metatags = context.get("metatags", "")
    if not metatags:
        return templatename

    import re

    # Match format: content="..." name="template"
    pattern = r'<meta[^>]*content="([^"]*)"[^>]*name="template"[^>]*/?\s*>'
    match = re.search(pattern, metatags, re.IGNORECASE)
    if match:
        template_name = match.group(1).strip().lower()
        # Validate template name to prevent path traversal
        if template_name in ("landing",):
            return f"{template_name}.html"

    return templatename


def _update_html_context_for_template(app, pagename, templatename, context, doctree):
    """Add template-specific context variables.

    This runs after template selection and adds context variables needed
    by specific templates.
    """
    metatags = context.get("metatags", "")
    if not metatags:
        return

    import re

    # Check if this is a landing page and extract landing-specific options
    template_pattern = r'<meta[^>]*content="([^"]*)"[^>]*name="template"[^>]*/?\s*>'
    template_match = re.search(template_pattern, metatags, re.IGNORECASE)

    if template_match and template_match.group(1).strip().lower() == "landing":
        # Check for landing-show-search option
        show_search_pattern = (
            r'<meta[^>]*content="([^"]*)"[^>]*name="landing-show-search"[^>]*/?\s*>'
        )
        show_search_match = re.search(show_search_pattern, metatags, re.IGNORECASE)
        if show_search_match:
            context["theme_landing_show_search"] = (
                show_search_match.group(1).strip().lower() == "true"
            )


def _apply_template_selection(app, pagename, templatename, context, doctree):
    """Apply custom template selection based on page metadata.

    This handler modifies the context to use an alternative template
    when specified via the .. meta:: directive.

    Note: Sphinx's html-page-context event doesn't allow changing the template
    directly, so we use a workaround by adding the template name to context
    and using Jinja2's extends mechanism in our templates.
    """
    metatags = context.get("metatags", "")
    if not metatags:
        return

    import re

    # Match format: content="..." name="template"
    pattern = r'<meta[^>]*content="([^"]*)"[^>]*name="template"[^>]*/?\s*>'
    match = re.search(pattern, metatags, re.IGNORECASE)
    if match:
        template_name = match.group(1).strip().lower()
        # Validate template name to prevent path traversal
        if template_name in ("landing",):
            context["custom_template"] = f"{template_name}.html"


# =============================================================================
# Rich Landing Page (YAML frontmatter-driven)
# =============================================================================

# Try to import yaml; fall back to a built-in minimal parser
try:
    import yaml as _yaml
except ImportError:
    _yaml = None


def _parse_yaml_frontmatter(text):
    """Minimal YAML parser for landing page frontmatter.

    Handles the subset of YAML used by landing_page configs: nested dicts,
    lists, strings, booleans. Uses PyYAML when available, otherwise falls
    back to a simple line-by-line parser.
    """
    if _yaml is not None:
        return _yaml.safe_load(text)

    # ---- Minimal built-in parser ----
    result = {}
    stack = [(result, -1)]  # (current_dict_or_list, indent_level)

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        i += 1

        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(stripped)

        # Pop stack to find parent at correct indent level
        while len(stack) > 1 and stack[-1][1] >= indent:
            stack.pop()

        parent, _ = stack[-1]

        # List item
        if stripped.startswith("- "):
            item_text = stripped[2:].strip()

            if isinstance(parent, dict):
                # Find the last key that should hold this list
                last_key = list(parent.keys())[-1] if parent else None
                if last_key is not None and parent[last_key] is None:
                    parent[last_key] = []
                if last_key is not None and isinstance(parent[last_key], list):
                    target_list = parent[last_key]
                else:
                    target_list = parent.setdefault("_items", [])
            elif isinstance(parent, list):
                target_list = parent
            else:
                continue

            if ":" in item_text:
                # Inline dict item: "- key: value"
                new_dict = {}
                k, v = item_text.split(":", 1)
                new_dict[k.strip()] = _yaml_cast(v.strip())
                target_list.append(new_dict)
                stack.append((new_dict, indent + 2))
            else:
                target_list.append(_yaml_cast(item_text))

        # Key-value pair
        elif ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip().strip('"').strip("'")
            val = val.strip()

            if isinstance(parent, dict):
                if val:
                    parent[key] = _yaml_cast(val)
                else:
                    parent[key] = None  # Will be filled by nested content
                    stack.append((parent, indent))
            elif isinstance(parent, list):
                # dict inside a list (continuation of last list item)
                if parent and isinstance(parent[-1], dict):
                    parent[-1][key] = _yaml_cast(val) if val else None
                    if not val:
                        stack.append((parent[-1], indent))

    return result


def _yaml_cast(val):
    """Cast a YAML string value to the appropriate Python type."""
    if not val or val == "~" or val == "null":
        return None
    if val.strip('"').strip("'") != val:
        return val.strip('"').strip("'")
    low = val.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    return val


def _inject_landing_page_data(app, pagename, templatename, context, doctree):
    """Extract landing_page YAML frontmatter and inject into template context.

    When a .md page contains a ``landing_page:`` key in its YAML frontmatter,
    the parsed data is injected into the Jinja template context so that the
    landing.html template can render a rich, category-based landing page.
    """
    source_path = app.env.doc2path(pagename)
    if not source_path.endswith(".md"):
        return

    try:
        with open(source_path, "r") as f:
            content = f.read()
    except (IOError, OSError):
        return

    # Parse YAML frontmatter (between --- markers)
    if not content.startswith("---"):
        return
    end = content.find("---", 3)
    if end == -1:
        return

    try:
        frontmatter = _parse_yaml_frontmatter(content[3:end])
    except Exception:
        return

    if not isinstance(frontmatter, dict) or "landing_page" not in frontmatter:
        return

    landing_data = frontmatter["landing_page"]
    context["landing_page"] = landing_data
    # Return template name to tell Sphinx to use landing.html for this page
    return "landing.html"


def _run_pagefind(app, exception):
    """Run Pagefind after build to create the search index."""
    if exception:
        return
    if app.builder.name != "html":
        return

    outdir = app.outdir

    import glob as globmod
    hidden_pages = []
    for pattern in ["genindex*.html", "py-modindex.html", "search.html", "404.html"]:
        for filepath in globmod.glob(os.path.join(outdir, pattern)):
            hidden = filepath + "._pagefind_skip"
            try:
                os.rename(filepath, hidden)
                hidden_pages.append((filepath, hidden))
            except OSError:
                pass

    exclude_selectors = (
        ".headerlink, .rating, .date-info-last-verified, "
        ".pytorch-call-to-action-links, .bd-header, "
        ".bd-sidebar-primary, .bd-sidebar-secondary, "
        ".site-footer, .pytorch-footer, nav, .breadcrumb, "
        ".search-container-wrapper, .bd-header-article, "
        ".skip-link, #pst-skip-link, .back-to-top, #pst-back-to-top"
    )

    try:
        for cmd in ["npx pagefind", "pagefind"]:
            try:
                result = subprocess.run(
                    f'{cmd} --site "{outdir}" --exclude-selectors "{exclude_selectors}"',
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if result.returncode == 0:
                    from sphinx.util import logging
                    logger = logging.getLogger(__name__)
                    logger.info("Pagefind search index built successfully")
                    return
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue

        from sphinx.util import logging
        logger = logging.getLogger(__name__)
        logger.warning(
            "Pagefind not found. Install with 'npm install pagefind' for full-text search. "
            "Search will fall back to title-only matching."
        )
    finally:
        for original, hidden in hidden_pages:
            try:
                os.rename(hidden, original)
            except OSError:
                pass


# =============================================================================
# Sphinx setup function
# =============================================================================


def setup(app):
    app.add_html_theme("pytorch_sphinx_theme2", get_html_theme_path())
    app.add_config_value("add_last_updated", False, "html")
    app.connect("html-page-context", add_date_info_to_page)

    # Cache root doc toctree entries during read phase (before doctrees may be
    # discarded by builders that skip disk writes for performance)
    app.connect("doctree-read", _cache_root_toctree_entries)
    app.connect("env-merge-info", _merge_toctree_entries)

    # Add hierarchical navigation context for dropdown menus
    app.connect("html-page-context", _add_hierarchical_nav_to_context)

    # Extract page meta description for LLM tags
    app.connect("html-page-context", _extract_page_meta_description)

    # Add template context variables for landing pages and other templates
    app.connect("html-page-context", _update_html_context_for_template)

    # Template selection from meta directive (must return new template name)
    # This event handler returns templatename via html-collect-pages hook instead
    app.connect("html-page-context", _apply_template_selection)

    # Rich landing page: extract landing_page YAML frontmatter
    app.connect("html-page-context", _inject_landing_page_data)

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

    # Generate llms.txt (and optionally .md files) after build completes
    app.connect("build-finished", _generate_llms_txt)

    # Run Pagefind to build search index after HTML build completes
    app.connect("build-finished", _run_pagefind)

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

    # Register landing page directives (available without sphinx_gallery)
    app.add_directive("landingcardgrid", custom_directives.LandingCardGridDirective)
    app.add_directive("landingcard", custom_directives.LandingCardDirective)
    app.add_directive("landingsearchbar", custom_directives.LandingSearchBarDirective)

    return {
        "version": "0.4.9",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
