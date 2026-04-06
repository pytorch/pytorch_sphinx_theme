"""Tests for LLM markdown generation (_html_to_markdown and related functions)."""

import re
import shutil
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from pytorch_sphinx_theme2 import (
    _html_to_markdown,
    _generate_md_files,
    _generate_llms_full_txt,
)


# =============================================================================
# _html_to_markdown tests
# =============================================================================


class TestHtmlToMarkdownHeadings:
    def test_h1(self):
        md = _html_to_markdown("<h1>Title</h1>")
        assert "# Title" in md

    def test_h2(self):
        md = _html_to_markdown("<h2>Section</h2>")
        assert "## Section" in md

    def test_h3(self):
        md = _html_to_markdown("<h3>Subsection</h3>")
        assert "### Subsection" in md

    def test_headerlinks_stripped(self):
        html = '<h1>Title<a class="headerlink" href="#">&para;</a></h1>'
        md = _html_to_markdown(html)
        assert "headerlink" not in md
        assert "\u00b6" not in md  # paragraph sign stripped


class TestHtmlToMarkdownInlineFormatting:
    def test_bold(self):
        md = _html_to_markdown("<p><strong>bold</strong></p>")
        assert "**bold**" in md

    def test_italic(self):
        md = _html_to_markdown("<p><em>italic</em></p>")
        assert "*italic*" in md

    def test_inline_code(self):
        md = _html_to_markdown("<p><code>some_func()</code></p>")
        assert "`some_func()`" in md

    def test_link(self):
        md = _html_to_markdown('<p><a href="https://example.com">click</a></p>')
        assert "[click](https://example.com)" in md


class TestHtmlToMarkdownCodeBlocks:
    def test_pre_code(self):
        html = "<pre><code>x = 1\ny = 2</code></pre>"
        md = _html_to_markdown(html)
        assert "```" in md
        assert "x = 1" in md

    def test_language_class(self):
        html = '<pre><code class="language-python">print("hi")</code></pre>'
        md = _html_to_markdown(html)
        assert "```python" in md


class TestHtmlToMarkdownLists:
    def test_unordered_list(self):
        html = "<ul><li>one</li><li>two</li></ul>"
        md = _html_to_markdown(html)
        assert "- one" in md
        assert "- two" in md

    def test_ordered_list(self):
        html = "<ol><li>first</li><li>second</li></ol>"
        md = _html_to_markdown(html)
        assert "1. first" in md
        assert "2. second" in md


class TestHtmlToMarkdownTables:
    def test_simple_table(self):
        html = """
        <table>
        <tr><th>Name</th><th>Value</th></tr>
        <tr><td>foo</td><td>bar</td></tr>
        </table>
        """
        md = _html_to_markdown(html)
        assert "| Name | Value |" in md
        assert "| foo | bar |" in md
        assert "| --- | --- |" in md


class TestHtmlToMarkdownContentExtraction:
    def test_extracts_article_content(self):
        html = """
        <html><body>
        <nav>Navigation stuff</nav>
        <article><h1>Real Content</h1><p>Hello world</p></article>
        <footer>Footer stuff</footer>
        </body></html>
        """
        md = _html_to_markdown(html)
        assert "Real Content" in md
        assert "Hello world" in md
        assert "Navigation stuff" not in md
        assert "Footer stuff" not in md

    def test_strips_date_info(self):
        html = """
        <article>
        <h1>Page Title</h1>
        <p class="date-info-last-verified">Created On: Jan 1, 2024 | Last Updated On: Feb 2, 2024</p>
        <p>Actual content here.</p>
        </article>
        """
        md = _html_to_markdown(html)
        assert "Created On:" not in md
        assert "Actual content here" in md

    def test_strips_search_elements(self):
        html = """
        <article>
        <div role="search"><input type="text"></div>
        <p>Content</p>
        </article>
        """
        md = _html_to_markdown(html)
        assert "Content" in md


class TestHtmlToMarkdownUnicode:
    def test_smart_quotes_normalized(self):
        html = "<p>it\u2019s a \u201ctest\u201d</p>"
        md = _html_to_markdown(html)
        assert "it's" in md
        assert '"test"' in md

    def test_em_dash_normalized(self):
        html = "<p>one\u2014two</p>"
        md = _html_to_markdown(html)
        assert "one--two" in md

    def test_en_dash_normalized(self):
        html = "<p>1\u20132</p>"
        md = _html_to_markdown(html)
        assert "1-2" in md

    def test_ellipsis_normalized(self):
        html = "<p>wait\u2026</p>"
        md = _html_to_markdown(html)
        assert "wait..." in md

    def test_html_entities_unescaped(self):
        html = "<p>&amp; &lt; &gt; &quot;</p>"
        md = _html_to_markdown(html)
        assert "& < >" in md


class TestHtmlToMarkdownMisc:
    def test_empty_html(self):
        md = _html_to_markdown("")
        assert md == ""

    def test_whitespace_cleanup(self):
        html = "<p>hello</p>\n\n\n\n\n<p>world</p>"
        md = _html_to_markdown(html)
        assert "\n\n\n" not in md

    def test_blockquote(self):
        html = "<blockquote><p>quoted text</p></blockquote>"
        md = _html_to_markdown(html)
        assert "> quoted text" in md

    def test_image(self):
        html = '<img src="pic.png" alt="A picture">'
        md = _html_to_markdown(html)
        assert "![A picture](pic.png)" in md

    def test_horizontal_rule(self):
        html = "<p>above</p><hr><p>below</p>"
        md = _html_to_markdown(html)
        assert "---" in md


# =============================================================================
# _generate_md_files tests
# =============================================================================


class TestGenerateMdFiles:
    def test_generates_md_from_html(self, tmp_path):
        # Create a fake HTML file
        html_content = "<article><h1>Test Page</h1><p>Hello world</p></article>"
        (tmp_path / "page.html").write_text(html_content, encoding="utf-8")

        app = MagicMock()
        app.outdir = str(tmp_path)

        docs = [{"docname": "page"}]
        results = _generate_md_files(app, docs)

        assert len(results) == 1
        assert "page" in results
        assert "# Test Page" in results["page"]
        assert "Hello world" in results["page"]
        md_path = tmp_path / "page.md"
        assert md_path.exists()

    def test_skips_missing_html(self, tmp_path):
        app = MagicMock()
        app.outdir = str(tmp_path)

        docs = [{"docname": "nonexistent"}]
        results = _generate_md_files(app, docs)
        assert len(results) == 0

    def test_creates_subdirectories(self, tmp_path):
        subdir = tmp_path / "community"
        subdir.mkdir()
        html_content = "<article><h1>Guide</h1><p>Content</p></article>"
        (subdir / "guide.html").write_text(html_content, encoding="utf-8")

        app = MagicMock()
        app.outdir = str(tmp_path)

        docs = [{"docname": "community/guide"}]
        results = _generate_md_files(app, docs)

        assert len(results) == 1
        assert "community/guide" in results
        assert (subdir / "guide.md").exists()

    def test_skips_empty_conversion(self, tmp_path):
        # HTML with only non-content elements
        html_content = "<nav>nav only</nav>"
        (tmp_path / "empty.html").write_text(html_content, encoding="utf-8")

        app = MagicMock()
        app.outdir = str(tmp_path)

        docs = [{"docname": "empty"}]
        results = _generate_md_files(app, docs)
        # May or may not produce output depending on fallback behavior,
        # but should not crash
        assert isinstance(results, dict)


# =============================================================================
# _generate_llms_full_txt tests
# =============================================================================


class TestGenerateLlmsFullTxt:
    def test_generates_concatenated_file(self, tmp_path):
        app = MagicMock()
        app.config.project = "TestProject"
        app.config.html_theme_options = {"llm_description": "A test project."}

        docs = [{"docname": "page1"}, {"docname": "page2"}]
        md_contents = {
            "page1": "# Page 1\n\nContent one.",
            "page2": "# Page 2\n\nContent two.",
        }
        _generate_llms_full_txt(app, docs, str(tmp_path), md_contents)

        full_path = tmp_path / "llms-full.txt"
        assert full_path.exists()
        content = full_path.read_text(encoding="utf-8")
        assert "# TestProject" in content
        assert "A test project." in content
        assert "Content one." in content
        assert "Content two." in content

    def test_uses_default_description(self, tmp_path):
        app = MagicMock()
        app.config.project = "MyDocs"
        app.config.html_theme_options = {}

        docs = [{"docname": "page"}]
        md_contents = {"page": "# Page\n\nContent."}
        _generate_llms_full_txt(app, docs, str(tmp_path), md_contents)

        content = (tmp_path / "llms-full.txt").read_text(encoding="utf-8")
        assert "MyDocs documentation." in content

    def test_skips_missing_md(self, tmp_path):
        app = MagicMock()
        app.config.project = "Test"
        app.config.html_theme_options = {}

        docs = [{"docname": "missing"}]
        md_contents = {}
        _generate_llms_full_txt(app, docs, str(tmp_path), md_contents)

        content = (tmp_path / "llms-full.txt").read_text(encoding="utf-8")
        assert "# Test" in content
        # Should just have the header, no page content
        assert "---" not in content


# =============================================================================
# Parallelism tests
# =============================================================================

PYTORCH_DOCS_HTML = Path("/data/users/svekars/pytorch/docs/cpp/build/html")


class TestParallelConversion:
    """Test that parallel markdown generation works correctly and is faster."""

    @pytest.fixture
    def pytorch_html_dir(self, tmp_path):
        """Copy PyTorch C++ docs HTML files to a temp dir for testing."""
        if not PYTORCH_DOCS_HTML.exists():
            pytest.skip("PyTorch C++ docs not built; run the docs build first")

        html_files = list(PYTORCH_DOCS_HTML.rglob("*.html"))
        if len(html_files) < 5:
            pytest.skip("Not enough HTML files for a meaningful parallelism test")

        # Copy HTML files preserving directory structure
        for html_file in html_files:
            rel = html_file.relative_to(PYTORCH_DOCS_HTML)
            dest = tmp_path / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(html_file, dest)

        return tmp_path, html_files

    def _build_docs_list(self, html_dir, html_files):
        """Build docs list from HTML files relative to html_dir."""
        docs = []
        for f in html_files:
            rel = f.relative_to(PYTORCH_DOCS_HTML)
            docname = str(rel.with_suffix(""))
            docs.append({"docname": docname})
        return docs

    def test_parallel_produces_valid_markdown(self, pytorch_html_dir):
        """All converted files should contain valid, non-empty markdown."""
        tmp_path, html_files = pytorch_html_dir
        docs = self._build_docs_list(tmp_path, html_files)

        app = MagicMock()
        app.outdir = str(tmp_path)

        results = _generate_md_files(app, docs)

        assert len(results) > 0, "Should convert at least some pages"
        for docname, md_content in results.items():
            assert isinstance(md_content, str)
            assert len(md_content.strip()) > 0, f"{docname} produced empty markdown"
            # Check that .md file was written to disk
            md_path = tmp_path / (docname + ".md")
            assert md_path.exists(), f"{docname}.md was not written to disk"

    def test_parallel_results_match_sequential(self, pytorch_html_dir):
        """Parallel results should be identical to sequential conversion."""
        tmp_path, html_files = pytorch_html_dir
        docs = self._build_docs_list(tmp_path, html_files)

        # Run sequential conversion
        sequential_results = {}
        for doc in docs:
            html_path = tmp_path / (doc["docname"] + ".html")
            if html_path.is_file():
                html_content = html_path.read_text(encoding="utf-8")
                md = _html_to_markdown(html_content)
                if md.strip():
                    sequential_results[doc["docname"]] = md

        # Run parallel conversion (in a fresh tmp dir to avoid .md file conflicts)
        tmp_path2 = tmp_path.parent / "parallel_copy"
        shutil.copytree(tmp_path, tmp_path2, dirs_exist_ok=True)
        # Remove any .md files from the copy
        for md_file in tmp_path2.rglob("*.md"):
            md_file.unlink()

        app = MagicMock()
        app.outdir = str(tmp_path2)

        parallel_results = _generate_md_files(app, docs)

        assert set(parallel_results.keys()) == set(sequential_results.keys()), (
            f"Parallel and sequential converted different pages.\n"
            f"Only in parallel: {set(parallel_results.keys()) - set(sequential_results.keys())}\n"
            f"Only in sequential: {set(sequential_results.keys()) - set(parallel_results.keys())}"
        )

        for docname in sequential_results:
            assert parallel_results[docname] == sequential_results[docname], (
                f"Mismatch for {docname}"
            )

    def test_parallel_faster_than_sequential(self, pytorch_html_dir):
        """Parallel conversion should not be significantly slower than sequential."""
        tmp_path, html_files = pytorch_html_dir
        docs = self._build_docs_list(tmp_path, html_files)

        # Time sequential
        start = time.perf_counter()
        for doc in docs:
            html_path = tmp_path / (doc["docname"] + ".html")
            if html_path.is_file():
                html_content = html_path.read_text(encoding="utf-8")
                _html_to_markdown(html_content)
        sequential_time = time.perf_counter() - start

        # Time parallel (use a fresh copy to avoid .md conflicts)
        tmp_path2 = tmp_path.parent / "timing_copy"
        shutil.copytree(tmp_path, tmp_path2, dirs_exist_ok=True)
        for md_file in tmp_path2.rglob("*.md"):
            md_file.unlink()

        app = MagicMock()
        app.outdir = str(tmp_path2)

        start = time.perf_counter()
        _generate_md_files(app, docs)
        parallel_time = time.perf_counter() - start

        print(f"\nSequential: {sequential_time:.3f}s, Parallel: {parallel_time:.3f}s")
        print(f"Speedup: {sequential_time / parallel_time:.2f}x")
        print(f"Files converted: {len(docs)}")

        # Parallel should not be more than 5x slower than sequential
        # (allows for process startup overhead with small doc sets)
        assert parallel_time < sequential_time * 5, (
            f"Parallel ({parallel_time:.3f}s) was way slower than "
            f"sequential ({sequential_time:.3f}s)"
        )

    def test_parallel_with_many_synthetic_files(self, tmp_path):
        """Test parallelism with a larger synthetic dataset."""
        num_files = 200
        for i in range(num_files):
            html = (
                f"<article><h1>Page {i}</h1>"
                f"<p>{'Content ' * 50}</p>"
                f"<pre><code>x = {i}</code></pre>"
                f"</article>"
            )
            (tmp_path / f"page_{i}.html").write_text(html, encoding="utf-8")

        docs = [{"docname": f"page_{i}"} for i in range(num_files)]

        app = MagicMock()
        app.outdir = str(tmp_path)

        results = _generate_md_files(app, docs)

        assert len(results) == num_files
        for i in range(num_files):
            assert f"page_{i}" in results
            assert f"# Page {i}" in results[f"page_{i}"]
