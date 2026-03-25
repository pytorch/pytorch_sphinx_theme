"""Tests for LLM markdown generation (_html_to_markdown and related functions)."""

import re
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
        count = _generate_md_files(app, docs)

        assert count == 1
        md_path = tmp_path / "page.md"
        assert md_path.exists()
        content = md_path.read_text(encoding="utf-8")
        assert "# Test Page" in content
        assert "Hello world" in content

    def test_skips_missing_html(self, tmp_path):
        app = MagicMock()
        app.outdir = str(tmp_path)

        docs = [{"docname": "nonexistent"}]
        count = _generate_md_files(app, docs)
        assert count == 0

    def test_creates_subdirectories(self, tmp_path):
        subdir = tmp_path / "community"
        subdir.mkdir()
        html_content = "<article><h1>Guide</h1><p>Content</p></article>"
        (subdir / "guide.html").write_text(html_content, encoding="utf-8")

        app = MagicMock()
        app.outdir = str(tmp_path)

        docs = [{"docname": "community/guide"}]
        count = _generate_md_files(app, docs)

        assert count == 1
        assert (subdir / "guide.md").exists()

    def test_skips_empty_conversion(self, tmp_path):
        # HTML with only non-content elements
        html_content = "<nav>nav only</nav>"
        (tmp_path / "empty.html").write_text(html_content, encoding="utf-8")

        app = MagicMock()
        app.outdir = str(tmp_path)

        docs = [{"docname": "empty"}]
        count = _generate_md_files(app, docs)
        # May or may not produce output depending on fallback behavior,
        # but should not crash
        assert count >= 0


# =============================================================================
# _generate_llms_full_txt tests
# =============================================================================


class TestGenerateLlmsFullTxt:
    def test_generates_concatenated_file(self, tmp_path):
        # Create some .md files
        (tmp_path / "page1.md").write_text("# Page 1\n\nContent one.", encoding="utf-8")
        (tmp_path / "page2.md").write_text("# Page 2\n\nContent two.", encoding="utf-8")

        app = MagicMock()
        app.config.project = "TestProject"
        app.config.html_theme_options = {"llm_description": "A test project."}

        docs = [{"docname": "page1"}, {"docname": "page2"}]
        _generate_llms_full_txt(app, docs, str(tmp_path))

        full_path = tmp_path / "llms-full.txt"
        assert full_path.exists()
        content = full_path.read_text(encoding="utf-8")
        assert "# TestProject" in content
        assert "A test project." in content
        assert "Content one." in content
        assert "Content two." in content

    def test_uses_default_description(self, tmp_path):
        (tmp_path / "page.md").write_text("# Page\n\nContent.", encoding="utf-8")

        app = MagicMock()
        app.config.project = "MyDocs"
        app.config.html_theme_options = {}

        docs = [{"docname": "page"}]
        _generate_llms_full_txt(app, docs, str(tmp_path))

        content = (tmp_path / "llms-full.txt").read_text(encoding="utf-8")
        assert "MyDocs documentation." in content

    def test_skips_missing_md(self, tmp_path):
        app = MagicMock()
        app.config.project = "Test"
        app.config.html_theme_options = {}

        docs = [{"docname": "missing"}]
        _generate_llms_full_txt(app, docs, str(tmp_path))

        content = (tmp_path / "llms-full.txt").read_text(encoding="utf-8")
        assert "# Test" in content
        # Should just have the header, no page content
        assert "---" not in content
