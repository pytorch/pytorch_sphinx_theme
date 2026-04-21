"""LLM Navigation Guide (llms.txt) and markdown generation support.

This module handles:
- Generating llms.txt with page listings for LLM discovery
- Converting Sphinx HTML output to clean markdown files
- Generating llms-full.txt with all content concatenated
"""

import os
import re
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from html import unescape
from pathlib import Path


def _html_to_markdown(html_content):
    """Convert HTML content to clean markdown.

    Extracts the main article/body content from a Sphinx-generated HTML page
    and converts it to readable markdown. Uses BeautifulSoup if available,
    otherwise falls back to regex-based conversion.
    """
    try:
        from bs4 import BeautifulSoup, NavigableString, Tag

        try:
            import lxml  # noqa: F401
            parser = "lxml"
        except ImportError:
            parser = "html.parser"
        soup = BeautifulSoup(html_content, parser)

        # Remove script, style, nav, and sidebar elements
        for tag in soup.find_all(
            ["script", "style", "nav", "footer", "header", "aside"]
        ):
            tag.decompose()

        # Remove Sphinx-specific non-content elements
        for selector in [
            ".headerlink",
            ".sphinxsidebar",
            ".related",
            ".footer",
            ".navigation",
            ".breadcrumb",
            ".date-info-last-verified",
            '[role="navigation"]',
            '[role="search"]',
            ".search-button",
        ]:
            for el in soup.select(selector):
                el.decompose()

        # Try to find the main content area (Sphinx uses various containers)
        content = (
            soup.find("article")
            or soup.find("div", class_="body")
            or soup.find("div", class_="document")
            or soup.find("div", {"role": "main"})
            or soup.find("main")
            or soup.body
            or soup
        )

        def _convert_node(node):
            """Recursively convert an HTML node to markdown."""
            if isinstance(node, NavigableString):
                text = str(node)
                # Collapse whitespace but preserve single newlines
                return text

            if not isinstance(node, Tag):
                return ""

            tag_name = node.name

            # Skip hidden elements
            if node.get("style") and "display:none" in node.get("style", ""):
                return ""

            # Get inner content by recursing into children
            inner = "".join(_convert_node(child) for child in node.children)

            if tag_name in ("h1", "h2", "h3", "h4", "h5", "h6"):
                level = int(tag_name[1])
                prefix = "#" * level
                text = inner.strip()
                if text:
                    return f"\n\n{prefix} {text}\n\n"
                return ""

            if tag_name == "p":
                text = inner.strip()
                if text:
                    return f"\n\n{text}\n\n"
                return ""

            if tag_name == "br":
                return "\n"

            if tag_name == "a":
                href = node.get("href", "")
                text = inner.strip()
                if href and text and not href.startswith("#"):
                    return f"[{text}]({href})"
                return text

            if tag_name == "strong" or tag_name == "b":
                text = inner.strip()
                if text:
                    return f"**{text}**"
                return ""

            if tag_name == "em" or tag_name == "i":
                text = inner.strip()
                if text:
                    return f"*{text}*"
                return ""

            if tag_name == "code":
                text = inner.strip()
                if text:
                    # Don't nest backticks
                    if "`" in text:
                        return text
                    return f"`{text}`"
                return ""

            if tag_name == "pre":
                # Code blocks - try to detect language from class
                code_el = node.find("code")
                lang = ""
                classes = (code_el or node).get("class", [])
                for cls in classes:
                    if cls.startswith("language-") or cls.startswith("highlight-"):
                        lang = cls.split("-", 1)[1]
                        break

                code_text = (code_el or node).get_text()
                return f"\n\n```{lang}\n{code_text.strip()}\n```\n\n"

            if tag_name == "blockquote":
                text = inner.strip()
                if text:
                    quoted = "\n".join(
                        f"> {line}" for line in text.split("\n")
                    )
                    return f"\n\n{quoted}\n\n"
                return ""

            if tag_name in ("ul", "ol"):
                items = []
                for idx, li in enumerate(node.find_all("li", recursive=False)):
                    li_text = _convert_node(li).strip()
                    if tag_name == "ol":
                        items.append(f"{idx + 1}. {li_text}")
                    else:
                        items.append(f"- {li_text}")
                if items:
                    return "\n\n" + "\n".join(items) + "\n\n"
                return ""

            if tag_name == "li":
                return inner.strip()

            if tag_name == "table":
                return _convert_table(node)

            if tag_name == "img":
                alt = node.get("alt", "")
                src = node.get("src", "")
                return f"![{alt}]({src})"

            if tag_name == "hr":
                return "\n\n---\n\n"

            if tag_name in (
                "div",
                "section",
                "article",
                "span",
                "dd",
                "dt",
                "dl",
                "figure",
                "figcaption",
                "tbody",
                "thead",
                "tr",
                "td",
                "th",
            ):
                return inner

            return inner

        def _convert_table(table_node):
            """Convert an HTML table to markdown."""
            rows = []
            for tr in table_node.find_all("tr"):
                cells = []
                for cell in tr.find_all(["td", "th"]):
                    cell_text = _convert_node(cell).strip()
                    # Replace pipes and newlines in cell content
                    cell_text = cell_text.replace("|", "\\|").replace("\n", " ")
                    cells.append(cell_text)
                if cells:
                    rows.append(cells)

            if not rows:
                return ""

            # Build markdown table
            lines = []
            lines.append("| " + " | ".join(rows[0]) + " |")
            lines.append("| " + " | ".join("---" for _ in rows[0]) + " |")
            for row in rows[1:]:
                # Pad row if needed
                while len(row) < len(rows[0]):
                    row.append("")
                lines.append("| " + " | ".join(row[: len(rows[0])]) + " |")

            return "\n\n" + "\n".join(lines) + "\n\n"

        md = _convert_node(content)

    except ImportError:
        # Fallback: regex-based conversion when BeautifulSoup is not available
        # Strip everything outside the body content
        body_match = re.search(
            r'<div class="body"[^>]*>(.*?)</div>\s*(?:<div class="clearer")',
            html_content,
            re.DOTALL,
        )
        if body_match:
            text = body_match.group(1)
        else:
            text = html_content

        # Remove script and style blocks
        text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)

        # Convert headings
        for i in range(1, 7):
            prefix = "#" * i
            text = re.sub(
                rf"<h{i}[^>]*>(.*?)</h{i}>",
                rf"\n\n{prefix} \1\n\n",
                text,
                flags=re.DOTALL,
            )

        # Convert code blocks
        text = re.sub(
            r"<pre[^>]*><code[^>]*>(.*?)</code></pre>",
            r"\n\n```\n\1\n```\n\n",
            text,
            flags=re.DOTALL,
        )
        text = re.sub(
            r"<pre[^>]*>(.*?)</pre>",
            r"\n\n```\n\1\n```\n\n",
            text,
            flags=re.DOTALL,
        )

        # Convert inline code
        text = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", text)

        # Convert links
        text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r"[\2](\1)", text)

        # Convert bold and italic
        text = re.sub(r"<(?:strong|b)>(.*?)</(?:strong|b)>", r"**\1**", text)
        text = re.sub(r"<(?:em|i)>(.*?)</(?:em|i)>", r"*\1*", text)

        # Convert list items
        text = re.sub(r"<li[^>]*>(.*?)</li>", r"- \1", text, flags=re.DOTALL)

        # Convert paragraphs
        text = re.sub(r"<p[^>]*>(.*?)</p>", r"\n\n\1\n\n", text, flags=re.DOTALL)

        # Strip remaining HTML tags
        text = re.sub(r"<[^>]+>", "", text)

        md = text

    # Unescape HTML entities
    md = unescape(md)

    # Normalize Unicode punctuation to ASCII equivalents for maximum compatibility
    md = md.replace("\u2018", "'").replace("\u2019", "'")   # smart single quotes
    md = md.replace("\u201c", '"').replace("\u201d", '"')   # smart double quotes
    md = md.replace("\u2013", "-").replace("\u2014", "--")  # en-dash, em-dash
    md = md.replace("\u2026", "...")                        # ellipsis
    md = md.replace("\u00a0", " ")                          # non-breaking space

    # Clean up excessive whitespace
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r" {2,}", " ", md)
    md = md.strip()

    return md


def _convert_single_doc(args):
    """Convert a single HTML doc to markdown. Top-level function for multiprocessing.

    Args:
        args: Tuple of (docname, outdir_str).

    Returns:
        Tuple of (docname, md_content) on success, or (docname, None) on failure.
    """
    docname, outdir_str = args
    outdir = Path(outdir_str)
    html_path = outdir / (docname + ".html")

    if not html_path.is_file():
        return (docname, None)

    try:
        html_content = html_path.read_text(encoding="utf-8")
        md_content = _html_to_markdown(html_content)

        if not md_content.strip():
            return (docname, None)

        md_path = outdir / (docname + ".md")
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(md_content, encoding="utf-8")
        return (docname, md_content)

    except Exception as e:
        print(f"Warning: Could not convert {docname}.html to markdown: {e}")
        return (docname, None)


def _generate_md_files(app, docs):
    """Generate .md files from built HTML pages using parallel processing.

    Uses ProcessPoolExecutor for parallel conversion, with automatic fallback
    to sequential processing if multiprocessing is unavailable (e.g., in
    sandboxed build environments like Netlify).

    Args:
        app: The Sphinx application object.
        docs: List of doc dicts with 'docname' keys.

    Returns:
        Dict mapping docname -> md_content for successfully converted pages.
    """
    outdir_str = str(app.outdir)
    args_list = [(doc["docname"], outdir_str) for doc in docs]
    results = {}
    total = len(args_list)
    max_workers = min(os.cpu_count() or 4, 8)

    try:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(_convert_single_doc, args): args[0]
                for args in args_list
            }
            done_count = 0
            log_interval = max(1, total // 10)
            for future in as_completed(futures):
                docname, md_content = future.result()
                if md_content is not None:
                    results[docname] = md_content
                done_count += 1
                if done_count % log_interval == 0 or done_count == total:
                    print(f"  Markdown conversion: {done_count}/{total} files processed")
    except (OSError, RuntimeError) as e:
        print(f"Parallel processing unavailable ({e}), falling back to sequential")
        results = {}
        for i, args in enumerate(args_list):
            docname, md_content = _convert_single_doc(args)
            if md_content is not None:
                results[docname] = md_content
            if (i + 1) % max(1, total // 10) == 0:
                print(f"  Markdown conversion: {i + 1}/{total} files processed")

    return results


def _generate_llms_full_txt(app, docs, outdir, md_contents):
    """Generate llms-full.txt by concatenating all markdown content.

    Per the llms.txt spec, llms-full.txt contains the full content of all
    documentation pages in a single file for easy LLM ingestion.

    Args:
        app: The Sphinx application object.
        docs: List of doc dicts with 'docname' keys.
        outdir: The output directory path.
        md_contents: Dict mapping docname -> md_content (from _generate_md_files).
    """
    project = app.config.project or "Documentation"
    theme_options = app.config.html_theme_options or {}
    llm_description = theme_options.get("llm_description", "").strip()
    if not llm_description:
        llm_description = f"{project} documentation."

    sections = []
    sections.append(f"# {project}\n\n> {llm_description}\n")

    for doc in docs:
        md_content = md_contents.get(doc["docname"])
        if md_content and md_content.strip():
            sections.append(f"\n---\n\n{md_content}")

    full_content = "\n".join(sections)
    full_path = Path(outdir) / "llms-full.txt"

    try:
        full_path.write_text(full_content, encoding="utf-8")
        print(f"Generated llms-full.txt at: {full_path}")
    except Exception as e:
        print(f"Warning: Could not write llms-full.txt: {e}")


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
       a. ``llm_domain`` + ``llm_base_path`` theme options -> fully constructed URLs
       b. Sphinx ``html_baseurl`` config -> baseurl + relative path
       c. Relative URLs as a last resort

    Enabled by default. Set ``llm_disabled = "true"`` to disable.

    Additional options:
    - ``llm_generate_full = "false"`` — skip llms-full.txt generation (expensive
      on large builds with thousands of pages).
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
    generate_md = (
        str(theme_options.get("llm_generate_md", "true")).lower() == "true"
    )

    # Resolve the base URL for links:
    # Priority: llm_domain > html_baseurl > relative
    html_baseurl = getattr(app.config, "html_baseurl", None) or ""
    html_baseurl = html_baseurl.strip().rstrip("/")

    # File extension for links: .md when markdown generation is enabled, .html otherwise
    link_ext = ".md" if generate_md else ".html"

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

            # Build the URL (use .md or .html based on config)
            url = make_url(docname + link_ext)
            docs.append({"title": str(title), "url": url, "docname": docname})

    except Exception as e:
        print(f"Warning: Could not discover pages for llms.txt: {e}")

    generate_full = (
        str(theme_options.get("llm_generate_full", "true")).lower() == "true"
    )

    # Generate .md files from HTML if enabled
    if generate_md and docs:
        md_contents = _generate_md_files(app, docs)
        print(f"Generated {len(md_contents)} markdown files from HTML pages")

        if generate_full:
            _generate_llms_full_txt(app, docs, app.outdir, md_contents)
    elif generate_full and docs:
        md_contents = _generate_md_files(app, docs)
        print(f"Generated {len(md_contents)} markdown files for llms-full.txt")
        _generate_llms_full_txt(app, docs, app.outdir, md_contents)

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
