__version__ = "0.4.6"

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


def _build_llms_url(domain, base_path, version, relative_path=""):
    """Build a full URL for llms.txt links.

    Args:
        domain: The documentation domain (e.g., "docs.pytorch.org")
        base_path: The base path after domain (e.g., "docs/", "vision/")
        version: The documentation version (e.g., "stable", "2.0.0")
        relative_path: The relative path to the page (e.g., "index.html")

    Returns:
        Full URL like "https://docs.pytorch.org/docs/stable/index.html"
    """
    # Ensure domain doesn't have trailing slash
    domain = domain.rstrip("/")

    # Ensure base_path has proper format (no leading slash, has trailing slash if non-empty)
    base_path = base_path.strip("/")
    if base_path:
        base_path = base_path + "/"

    # Ensure version doesn't have slashes
    version = version.strip("/")

    # Ensure relative_path doesn't have leading slash
    relative_path = relative_path.lstrip("/")

    # Build URL
    if relative_path:
        return f"https://{domain}/{base_path}{version}/{relative_path}"
    else:
        return f"https://{domain}/{base_path}{version}/"


def _generate_llms_txt(app, exception):
    """Dynamically generate llms.txt during documentation build.

    The file is resolved in this order:

    1. **Explicit disable** — ``llm_disabled = "true"`` skips generation entirely.
    2. **Custom file** — ``llm_custom_file`` theme option pointing to a file
       relative to the Sphinx source directory.
    3. **Convention** — A file named ``llms.txt`` in the Sphinx source root.
    4. **Auto-generation** — A simple page listing following the llms.txt spec,
       with URLs resolved as:
       a. ``llm_domain`` + ``llm_base_path`` theme options → fully constructed URLs
       b. Sphinx ``html_baseurl`` config → baseurl + relative path
       c. Relative URLs as a last resort

    Enabled by default. Set ``llm_disabled = "true"`` to disable.
    """
    if exception is not None:
        return  # Don't generate if build failed

    if app.builder.name != "html":
        return

    # Enabled by default; opt-out with llm_disabled = "true"
    theme_options = app.config.html_theme_options or {}
    if str(theme_options.get("llm_disabled", "false")).lower() == "true":
        return

    dest_path = Path(app.outdir) / "llms.txt"

    # --- 1. Explicit option: llm_custom_file ---
    custom_file = theme_options.get("llm_custom_file", "").strip()
    if custom_file:
        custom_path = Path(app.srcdir) / custom_file
        if custom_path.is_file():
            shutil.copy2(custom_path, dest_path)
            print(f"Copied custom llms.txt from: {custom_path}")
            return
        else:
            print(
                f"Warning: llm_custom_file '{custom_file}' not found at "
                f"{custom_path}, falling back to auto-generation"
            )

    # --- 2. Convention: llms.txt in the source root ---
    source_llms = Path(app.srcdir) / "llms.txt"
    if source_llms.is_file():
        shutil.copy2(source_llms, dest_path)
        print(f"Using project-provided llms.txt from: {source_llms}")
        return

    # --- 3. Auto-generation ---
    # Get configuration
    project = app.config.project or "Documentation"
    version = app.config.version or "latest"
    domain = theme_options.get("llm_domain", "").strip()
    base_path = theme_options.get("llm_base_path", "").strip()

    # Resolve the base URL for links:
    # Priority: llm_domain > html_baseurl > relative
    html_baseurl = getattr(app.config, "html_baseurl", None) or ""
    html_baseurl = html_baseurl.strip().rstrip("/")

    def make_url(relative_path):
        if domain:
            return _build_llms_url(domain, base_path, version, relative_path)
        if html_baseurl:
            return f"{html_baseurl}/{relative_path}"
        return relative_path

    # Collect all documentation pages
    docs = []

    try:
        # Get all document names from the environment
        all_docs = list(app.env.all_docs.keys()) if hasattr(app.env, "all_docs") else []

        for docname in sorted(all_docs):
            # Skip internal/private pages
            if docname.startswith("_"):
                continue

            # Get the page title
            title = app.env.titles.get(docname, docname)
            if hasattr(title, "astext"):
                title = title.astext()

            # Build the URL
            url = make_url(docname + ".html")
            docs.append({"title": str(title), "url": url, "docname": docname})

    except Exception as e:
        print(f"Warning: Could not discover pages for llms.txt: {e}")

    # Deduplicate titles if enabled
    # This adds a disambiguating suffix to duplicate titles based on their URL path
    deduplicate = (
        str(theme_options.get("llm_deduplicate_titles", "false")).lower() == "true"
    )
    if deduplicate:
        # Count title occurrences
        title_counts = {}
        for doc in docs:
            title_counts[doc["title"]] = title_counts.get(doc["title"], 0) + 1

        # Find duplicates and add disambiguation
        for doc in docs:
            if title_counts[doc["title"]] > 1:
                # Extract module/path info from docname for disambiguation
                # e.g., "generated/torch.nn.GRU" -> "torch.nn.GRU"
                docname = doc["docname"]

                # Try to get a meaningful suffix from the docname
                if "/" in docname:
                    suffix = docname.split("/")[-1]
                else:
                    suffix = docname

                # Remove "generated/" prefix if present (Sphinx autodoc convention)
                if suffix.startswith("generated/"):
                    suffix = suffix[10:]

                # Only add suffix if it's different from the title
                if suffix.lower() != doc["title"].lower():
                    doc["title"] = f"{doc['title']} ({suffix})"

    # Build the llms.txt content in Hugging Face style
    lines = []

    # Header
    lines.append(f"# {project}")
    lines.append("")

    # Quote block with project description (for spec compliance)
    # If llm_description is set, use it. Otherwise, generate a generic one from project name.
    llm_description = theme_options.get("llm_description", "").strip()
    if not llm_description:
        # Generic fallback using Sphinx project name
        llm_description = f"{project} documentation."

    lines.append(f"> {llm_description}")
    lines.append("")

    lines.append("## Docs")
    lines.append("")

    # List all documentation pages
    for doc in docs:
        lines.append(f"- [{doc['title']}]({doc['url']})")

    # Join content
    content = "\n".join(lines)

    # Write to site root
    try:
        dest_path.write_text(content, encoding="utf-8")
        print(f"Generated llms.txt with {len(docs)} pages at: {dest_path}")
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
            c.astext()
            for c in (def_node.children if def_node else [])
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


def _get_toctree_entries_from_doctree(app, docname):
    """Get all toctree entries from a document, including external URLs.

    Returns a list of tuples: (title, reference, is_external)
    """
    entries = []
    try:
        doctree = app.env.get_doctree(docname)

        # Find all toctree nodes
        from sphinx import addnodes

        for toctree_node in doctree.findall(addnodes.toctree):
            # toctree_node['entries'] contains tuples of (title, ref)
            # where title can be None (use document title) or a string
            # and ref is either a document name or an external URL
            for title, ref in toctree_node.get("entries", []):
                if ref:
                    is_external = ref.startswith(("http://", "https://", "/"))
                    entries.append((title, ref, is_external))
    except Exception:
        pass

    return entries


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


# =============================================================================
# Sphinx setup function
# =============================================================================


def setup(app):
    app.add_html_theme("pytorch_sphinx_theme2", get_html_theme_path())
    app.add_config_value("add_last_updated", False, "html")
    app.connect("html-page-context", add_date_info_to_page)

    # Add hierarchical navigation context for dropdown menus
    app.connect("html-page-context", _add_hierarchical_nav_to_context)

    # Extract page meta description for LLM tags
    app.connect("html-page-context", _extract_page_meta_description)

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
        "version": "0.4.6",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
