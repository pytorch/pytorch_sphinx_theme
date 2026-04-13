# Configuration Reference

This document provides a comprehensive reference for all configuration options available in the PyTorch Sphinx Theme 2. These options are set in your project's `conf.py` file.

## Quick Start

```python
# conf.py

html_theme = "pytorch_sphinx_theme2"
html_theme_path = [pytorch_sphinx_theme2.get_html_theme_path()]

html_theme_options = {
    "canonical_url": "https://docs.pytorch.org/your-project/",
    "analytics_id": "UA-XXXXXXXX-X",
    "navbar_align": "left",
    "use_edit_page_button": True,
}
```

---

## html_theme_options

All theme-specific options are configured via the `html_theme_options` dictionary in `conf.py`.

### Navigation Options

#### `navbar_align`
- **Type:** String
- **Default:** `"left"`
- **Description:** Controls the alignment of navigation items in the navbar. Options: `"left"`, `"center"`, `"right"`.

#### `navbar_start`
- **Type:** String (comma-separated list of component names)
- **Default:** `"navbar-logo"`
- **Description:** Components to display at the start (left) of the navbar. Common components:
  - `"navbar-logo"` - The site logo
  - `"version-switcher"` - Version dropdown switcher

```python
html_theme_options = {
    "navbar_start": ["navbar-logo", "version-switcher"],
}
```

#### `navbar_center`
- **Type:** String
- **Default:** `"navbar-nav"`
- **Description:** Components to display in the center of the navbar. Typically contains the main navigation links.

#### `navbar_end`
- **Type:** String (comma-separated list of component names)
- **Default:** `"search-field-custom, theme-switcher, navbar-icon-links"`
- **Description:** Components to display at the end (right) of the navbar. Common components:
  - `"search-field-custom"` - Search input field
  - `"theme-switcher"` - Light/dark mode toggle
  - `"navbar-icon-links"` - Social/external icon links

#### `navbar_persistent`
- **Type:** String
- **Default:** `""`
- **Description:** Components that persist across all pages in the navbar.

#### `collapse_navigation`
- **Type:** Boolean
- **Default:** `False`
- **Description:** If `True`, collapses the navigation sections by default, showing `[+]` icons to expand.

#### `show_prev_next`
- **Type:** Boolean
- **Default:** `False`
- **Description:** If `True`, displays "Previous" and "Next" navigation buttons.

#### `display_version`
- **Type:** Boolean
- **Default:** `True`
- **Description:** If `True`, displays the version number in the sidebar/navbar.

#### `logo_text`
- **Type:** String
- **Default:** `"Home"`
- **Description:** Text to display next to or below the logo.

#### `enable_navbar_dropdowns`
- **Type:** Boolean
- **Default:** `True`
- **Description:** Enable dropdown menus in horizontal navbar for items with children. Set to `False` to show only flat links (no dropdowns).

---

### Article Layout Options

#### `article_header_start`
- **Type:** String
- **Default:** `"breadcrumbs"`
- **Description:** Components to display at the start of the article header. Common components:
  - `"breadcrumbs"` - Navigation breadcrumbs

#### `article_header_end`
- **Type:** String
- **Default:** `"rate_page.html"`
- **Description:** Components to display at the end of the article header.

#### `secondary_sidebar_items`
- **Type:** String (comma-separated list)
- **Default:** `"page-toc, edit-this-page, sourcelink"`
- **Description:** Items to show in the secondary (right) sidebar:
  - `"page-toc"` - Table of contents for the current page
  - `"edit-this-page"` - Link to edit the source file
  - `"sourcelink"` - Link to view the source

#### `article_footer_items`
- **Type:** String
- **Default:** `"footer-rating.html"`
- **Description:** Components to display in the article footer.

#### `use_edit_page_button`
- **Type:** Boolean
- **Default:** `True`
- **Description:** If `True`, displays an "Edit this page" button that links to the source file on GitHub/GitLab.

---

### Project Information

#### `pytorch_project`
- **Type:** String
- **Default:** `""`
- **Description:** Identifies the PyTorch project. Used to customize certain theme behaviors. Common values: `"docs"`, `"tutorials"`.

#### `canonical_url`
- **Type:** String
- **Default:** `""`
- **Description:** The canonical URL for the documentation. Used for SEO to indicate the preferred version of a page to search engines.

```python
html_theme_options = {
    "canonical_url": "https://docs.pytorch.org/stable/",
}
```

#### `analytics_id`
- **Type:** String
- **Default:** `""`
- **Description:** Google Analytics tracking ID for page analytics.

```python
html_theme_options = {
    "analytics_id": "UA-XXXXXXXX-X",
}
```

---

### Header and Footer Control

#### `show_lf_header`
- **Type:** Boolean
- **Default:** `False`
- **Description:** If `True`, shows the Linux Foundation header banner.

#### `show_lf_footer`
- **Type:** Boolean
- **Default:** `True`
- **Description:** If `True`, shows the Linux Foundation footer.

---

### RunLLM Widget Configuration

The theme supports integration with RunLLM for AI-powered documentation assistance.

#### `runllm_assistant_id`
- **Type:** String
- **Default:** `""`
- **Description:** Your RunLLM assistant ID. **Required** to enable the widget. Each repository should have its own unique assistant ID from RunLLM.

#### `runllm_name`
- **Type:** String
- **Default:** `"Assistant"`
- **Description:** Display name for the RunLLM assistant.

#### `runllm_position`
- **Type:** String
- **Default:** `"BOTTOM_RIGHT"`
- **Description:** Position of the RunLLM widget on the page. Options: `"BOTTOM_RIGHT"`, `"BOTTOM_LEFT"`.

```python
html_theme_options = {
    "runllm_assistant_id": "your-assistant-id",
    "runllm_name": "PyTorch Assistant",
    "runllm_position": "BOTTOM_RIGHT",
}
```

---

### PyTorch.org Link

#### `show_pytorch_org_link`
- **Type:** Boolean
- **Default:** `True`
- **Description:** If `True`, shows a "Go to pytorch.org" link in the navbar on desktop and sidebar on mobile.

---

### Announcement Banner Configuration

The theme supports an optional announcement banner that appears at the top of the page (above the navigation). Use it for surveys, event announcements, release notes, deprecation notices, or any important information you want to highlight to users.

Configure it as a dictionary with the following keys:

#### `announcement_banner`
- **Type:** Dictionary
- **Default:** `None` (banner disabled)
- **Description:** Configuration dictionary for the announcement banner.

> **Note:** This option is named `announcement_banner` (not `announcement`) to avoid conflicts with PyData Sphinx Theme's built-in `announcement` option which expects a string.

**Dictionary keys:**

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| `text` | String | **Yes** | - | The main message to display in the banner |
| `url` | String | No | `""` | URL for the call-to-action link |
| `link_text` | String | No | `"Learn More"` | Text for the call-to-action link |
| `dismissible` | Boolean | No | `True` | If `True`, shows a close button (X) that allows users to dismiss the banner. Dismissal is remembered via localStorage. |

#### Example: Survey Banner (Dismissible)

```python
html_theme_options = {
    "announcement_banner": {
        "text": "Help us improve PyTorch! Take our 2-minute survey.",
        "url": "https://forms.gle/your-survey-id",
        "link_text": "Take Survey",
        "dismissible": True,
    },
}
```

#### Example: Persistent Event Banner (Non-Dismissible)

```python
html_theme_options = {
    "announcement_banner": {
        "text": "PyTorch Conference 2026 registration is now open!",
        "url": "https://pytorch.org/conference",
        "link_text": "Register Now",
        "dismissible": False,
    },
}
```

#### Example: Text-Only Notice (No Link)

```python
html_theme_options = {
    "announcement_banner": {
        "text": "PyTorch 3.0 has been released! Check the release notes in the sidebar.",
    },
}
```

---

### LLM Discovery Configuration

The theme includes built-in support for helping AI agents and LLMs discover and navigate the documentation effectively. This follows the emerging [llms.txt](https://llmstxt.org/) standard.

#### How It Works

When enabled (opt-in), the theme:
1. Generates a `/llms.txt` file at the site root with navigation guidance
2. Adds machine-readable `<meta name="llm:*">` tags to every page
3. Includes a `<link rel="alternate">` pointing to the llms.txt file

URLs in `llms.txt` are resolved in this priority order:
1. **`llm_domain`** + `llm_base_path` theme options → fully constructed URLs (e.g., `https://docs.pytorch.org/docs/stable/index.html`)
2. **`html_baseurl`** Sphinx config → baseurl + relative path (e.g., `https://docs.pytorch.org/docs/stable/index.html`)
3. **Relative URLs** as a last resort (e.g., `index.html`)

Most PyTorch doc sets already define `html_baseurl` in their `conf.py`, so absolute URLs are generated automatically without any extra theme configuration.

#### `llm_disabled`
- **Type:** String (`"true"` or `"false"`)
- **Default:** `"true"` (disabled by default)
- **Description:** Set to `"false"` to enable `llms.txt` generation and LLM meta tags.

```python
html_theme_options = {
    "llm_disabled": "false",  # Enable LLM discovery features
}
```

#### `llm_description`
- **Type:** String
- **Default:** `""` (auto-generated from project name)
- **Description:** A brief description of the site for LLMs. Appears in the `llm:description` meta tag and at the top of `llms.txt`.

```python
html_theme_options = {
    "llm_description": "TorchVision provides datasets, models, and transforms for computer vision tasks.",
}
```

#### `llm_domain` (optional)
- **Type:** String
- **Default:** `""` (uses relative URLs)
- **Description:** Domain for the documentation site. When set, `llms.txt` generates absolute URLs instead of relative ones.

```python
html_theme_options = {
    "llm_domain": "docs.pytorch.org",  # Optional: generates absolute URLs
}
```

#### `llm_base_path` (optional)
- **Type:** String
- **Default:** `""`
- **Description:** Base path after domain (e.g., `"tutorials/"`, `"vision/"`). Only used when `llm_domain` is set.

```python
html_theme_options = {
    "llm_domain": "docs.pytorch.org",
    "llm_base_path": "tutorials",
}
```

#### `llm_custom_file` (optional)
- **Type:** String
- **Default:** `""` (auto-generate or use convention)
- **Description:** Path to a custom `llms.txt` file, relative to the Sphinx source directory. When set, this file is copied verbatim to the output instead of auto-generating one.

```python
html_theme_options = {
    "llm_disabled": "false",
    "llm_custom_file": "my-custom-llms.txt",  # relative to source dir
}
```

#### `llm_generate_md`
- **Type:** String (`"true"` or `"false"`)
- **Default:** `"true"` (enabled by default)
- **Description:** When enabled, generates a clean `.md` (Markdown) file alongside each `.html` page in the build output, and links to `.md` files in `llms.txt` instead of `.html` files.

The generated `.md` files strip all navigation, sidebars, scripts, and theme-injected metadata (e.g., date info), producing clean, readable content suitable for LLMs. Unicode smart quotes and other typographic characters are normalized to ASCII equivalents for maximum compatibility.

**Generated files:**
- `*.md` — one per HTML page, alongside the `.html` files
- `llms.txt` — page index with links to `.md` files
- `llms-full.txt` — all page content concatenated (controlled separately by `llm_generate_full`)

```python
html_theme_options = {
    "llm_generate_md": "true",  # Enabled by default
}
```

To disable markdown generation (links in `llms.txt` will point to `.html` files):

```python
html_theme_options = {
    "llm_generate_md": "false",
}
```

#### `llm_generate_full`
- **Type:** String (`"true"` or `"false"`)
- **Default:** `"true"` (enabled by default)
- **Description:** When enabled, generates `llms-full.txt` — a single file concatenating all page content for LLM ingestion. For large projects (e.g., PyTorch with thousands of API pages), this file can be extremely large and may not fit in most LLM context windows. Set to `"false"` to skip generating `llms-full.txt` while still generating individual `.md` files and `llms.txt`.

```python
html_theme_options = {
    "llm_generate_md": "true",
    "llm_generate_full": "false",  # Skip llms-full.txt for large projects
}
```

#### `llm_deduplicate_titles`
- **Type:** String (`"true"` or `"false"`)
- **Default:** `"false"`
- **Description:** When enabled, adds disambiguating suffixes to duplicate page titles in `llms.txt`. Useful for projects with auto-generated API docs where multiple pages share the same title.

For example, if two pages are both titled "GRU", they become:
- `GRU (torch.nn.GRU)`
- `GRU (torch.nn.GRUCell)`

```python
html_theme_options = {
    "llm_deduplicate_titles": "true",
}
```

#### Source-Root Convention

If no `llm_custom_file` is specified, the theme automatically checks for a file named `llms.txt` in the Sphinx source root directory (the same directory as `conf.py`). If found, it is used as-is instead of auto-generating one. This allows a zero-config override — just drop an `llms.txt` file next to `conf.py`.

**Resolution order:**
1. `llm_custom_file` theme option → copy that file
2. `llms.txt` in the source root → copy that file
3. Auto-generate from the documentation pages

#### Generated Meta Tags

The theme automatically adds the following meta tags to every page:

```html
<meta name="llm:site-type" content="documentation">
<meta name="llm:framework" content="PyTorch">
<meta name="llm:generator" content="Sphinx">
<meta name="llm:description" content="...">
<meta name="llm:navigation-file" content="/llms.txt">
<meta name="llm:sitemap" content="/sitemap.xml">
<meta name="llm:version" content="2.0.0">
<meta name="llm:project" content="PyTorch Tutorials">
<meta name="llm:page-type" content="api|tutorial|documentation">
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM Navigation Guide">
```

When `llm_domain` is configured, URLs become absolute (e.g., `https://docs.pytorch.org/tutorials/llms.txt`).

#### Example: Minimal Configuration (Relative URLs)

```python
html_theme_options = {
    "llm_disabled": "false",
    "llm_description": "TorchVision provides datasets, model architectures, and image transforms for computer vision.",
}
```

#### Example: Full Configuration (Absolute URLs)

```python
html_theme_options = {
    "llm_disabled": "false",
    "llm_description": "TorchVision provides datasets, model architectures, and image transforms for computer vision.",
    "llm_domain": "docs.pytorch.org",
    "llm_base_path": "vision",
}
```

---

### Icon Links

#### `icon_links`
- **Type:** List of dictionaries
- **Description:** External links displayed as icons in the navbar.

```python
html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/pytorch/pytorch",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "X",
            "url": "https://x.com/PyTorch",
            "icon": "fa-brands fa-x-twitter",
        },
        {
            "name": "Discourse",
            "url": "https://dev-discuss.pytorch.org/",
            "icon": "fa-brands fa-discourse",
        },
    ],
}
```

---

### Extra Project Links

#### `extra_project_links`
- **Type:** List of dictionaries
- **Description:** Additional project-related links to display (e.g., in the sidebar or footer).

```python
html_theme_options = {
    "extra_project_links": [
        {
            "name": "See All Recipes",
            "url": "https://pytorch.org/tutorials/recipes/recipes_index.html",
        },
        {
            "name": "See All Prototype Recipes",
            "url": "https://pytorch.org/tutorials/prototype/prototype_index.html",
        },
    ],
}
```

---

### External Links

#### `external_links`
- **Type:** List of dictionaries
- **Description:** External navigation links to display in the navbar.

```python
html_theme_options = {
    "external_links": [
        {
            "name": "Tutorials",
            "url": "https://pytorch.org/tutorials/",
        },
    ],
}
```

---

### Version Switcher

#### `switcher`
- **Type:** Dictionary
- **Description:** Configuration for the version switcher dropdown.

```python
html_theme_options = {
    "switcher": {
        "json_url": "https://docs.pytorch.org/docs/pytorch-versions.json",
        "version_match": "main",
    },
}
```

---

### Logo Configuration

#### `logo`
- **Type:** Dictionary
- **Description:** Custom logo configuration.

```python
html_theme_options = {
    "logo": {
        "image_light": "_static/logo-light.svg",
        "image_dark": "_static/logo-dark.svg",
    },
}
```

---

### Header Links Before Dropdown

#### `header_links_before_dropdown`
- **Type:** Integer
- **Default:** `4`
- **Description:** Number of navigation links to show before collapsing into a dropdown menu.

---

### Language Bindings Links

#### `language_bindings_links`
- **Type:** String
- **Default:** `""`
- **Description:** Links to language bindings documentation.

---

### Version Info

#### `version_info`
- **Type:** String
- **Default:** `""`
- **Description:** Additional version information to display.

---

## html_context Options

The `html_context` dictionary provides context variables available in templates.

```python
html_context = {
    "github_url": "https://github.com",
    "github_user": "pytorch",
    "github_repo": "pytorch",
    "github_version": "main",
    "doc_path": "docs/source",
    "feedback_url": "https://github.com/pytorch/pytorch/issues",
    "version": version,
}
```

### Repository Configuration

#### `github_url`
- **Type:** String
- **Description:** Base URL for GitHub (typically `"https://github.com"`).

#### `github_user`
- **Type:** String
- **Description:** GitHub organization or user name.

#### `github_repo`
- **Type:** String
- **Description:** GitHub repository name.

#### `github_version`
- **Type:** String
- **Description:** Branch or version for GitHub links (e.g., `"main"`, `"master"`, `"stable"`).

#### `doc_path`
- **Type:** String
- **Description:** Path to the documentation source files within the repository. Used by the "Edit on GitHub" button to construct the correct URL for editing source files.

| Repository Structure | `doc_path` Value |
|---------------------|------------------|
| `repo/docs/file.rst` | `"docs"` |
| `repo/docs/source/file.rst` | `"docs/source"` |
| `repo/source/file.rst` | `"source"` |
| `repo/file.rst` (root) | `""` or `"."` |

#### `has_sphinx_gallery`
- **Type:** Boolean
- **Description:** Set to `True` to enable call-to-action buttons (Run in Google Colab, Download Notebook, View on GitHub) on sphinx-gallery generated pages.

```python
html_context = {
    "has_sphinx_gallery": True,
}
```

### Sphinx-Gallery Call-to-Action Links

When using [sphinx-gallery](https://sphinx-gallery.github.io/) to generate tutorials from Python scripts, the theme can display call-to-action buttons at the top of each tutorial page:

- **Run in Google Colab** - Opens the notebook in Google Colab
- **Download Notebook** - Downloads the `.ipynb` file
- **View on GitHub** - Links to the source `.py` file

#### Enabling Call-to-Action Links

To enable these buttons, set `has_sphinx_gallery` to `True` and configure the repository settings:

```python
html_context = {
    "has_sphinx_gallery": True,
    "github_url": "https://github.com",
    "github_user": "your-org",
    "github_repo": "your-tutorials-repo",
    "github_version": "main",           # Branch for source .py files
    "colab_branch": "gh-pages",         # Branch where .ipynb files are hosted
}
```

#### How the Links Work

| Button | URL Pattern |
|--------|-------------|
| **Run in Google Colab** | `https://colab.research.google.com/github/{user}/{repo}/blob/{colab_branch}/_downloads/{notebook_path}` |
| **Download Notebook** | Links to the sphinx-gallery generated `.ipynb` download |
| **View on GitHub** | `https://github.com/{user}/{repo}/blob/{github_version}/{tutorial_path}.py` |

#### `colab_branch`
- **Type:** String
- **Default:** `"gh-pages"`
- **Description:** The branch where notebook files (`.ipynb`) are hosted for Google Colab access. Typically this is `gh-pages` where the built documentation is deployed.

```python
html_context = {
    "colab_branch": "gh-pages",
}
```

#### Requirements

1. **sphinx-gallery extension** must be enabled:
   ```python
   extensions = [
       "sphinx_gallery.gen_gallery",
   ]
   ```

2. **sphinx-gallery must be configured**:
   ```python
   sphinx_gallery_conf = {
       "examples_dirs": "examples",        # Directory with .py tutorial files
       "gallery_dirs": "auto_examples",    # Output directory for generated docs
       "filename_pattern": "/example_",    # Pattern for files to process
   }
   ```

3. **Notebooks must be accessible** on the `colab_branch` (e.g., `gh-pages`) for Colab to load them.

#### Complete Example

```python
# conf.py
extensions = [
    "sphinx_gallery.gen_gallery",
    "pytorch_sphinx_theme2",
]

sphinx_gallery_conf = {
    "examples_dirs": "examples",
    "gallery_dirs": "auto_examples",
    "filename_pattern": "/example_",
}

html_context = {
    "has_sphinx_gallery": True,
    "github_url": "https://github.com",
    "github_user": "pytorch",
    "github_repo": "tutorials",
    "github_version": "main",
    "colab_branch": "gh-pages",
}
```

### Feedback Configuration

#### `feedback_url`
- **Type:** String
- **Description:** URL for documentation feedback/issues.

### Date Information

#### `date_info`
- **Type:** Dictionary
- **Description:** Configuration for date display on pages.

```python
html_context = {
    "date_info": {
        "paths_to_skip": ["installing", "changelog"],
    },
}
```

---

## Theme Variables

The theme provides additional variables via `get_theme_variables()`:

```python
import pytorch_sphinx_theme2

theme_variables = pytorch_sphinx_theme2.get_theme_variables()
html_context = {
    "theme_variables": theme_variables,
    "library_links": theme_variables.get("library_links", []),
}
```

### Library Links

Pre-configured links to PyTorch ecosystem libraries (loaded from `links.json`):

```json
{
  "library_links": [
    {"url": "https://docs.pytorch.org/executorch", "name": "ExecuTorch"},
    {"url": "https://docs.pytorch.org/vision", "name": "torchvision"},
    {"url": "https://docs.pytorch.org/audio", "name": "torchaudio"}
  ]
}
```

---

## Additional Sphinx Configuration

### Last Updated Dates

Enable automatic "Created On" and "Last Updated On" date display:

```python
def setup(app):
    app.config.add_last_updated = True
    from pytorch_sphinx_theme2 import add_date_info_to_page
    app.connect("html-page-context", add_date_info_to_page)
```

### Sphinx-Tippy Integration

For glossary tooltips with parallel build support:

```python
extensions = [
    "sphinx_tippy",
    "pytorch_sphinx_theme2",  # Register as extension
]

tippy_props = {
    "placement": "auto-start",
    "maxWidth": 500,
    "interactive": True,
    "theme": "material",
}

# Skip non-glossary URLs
tippy_skip_urls = (r"^(?!.*_glossary(\.html)?#term-).*$",)
tippy_enable_mathjax = True
```

### Custom CSS

Add custom stylesheets:

```python
html_css_files = [
    "custom.css",
]
```

### Static Files

Configure static file paths:

```python
html_static_path = ["_static"]
```

### Source Link

Show/hide links to page source:

```python
html_show_sourcelink = True
```

---

## Page-Level Configuration

Individual pages can override theme settings using reStructuredText metadata:

```rst
:github_url: https://github.com/pytorch/pytorch/blob/main/custom/path.rst
```

Available page-level options:
- `:github_url:` - Force the "Edit on GitHub" link to a specific URL
- `:bitbucket_url:` - Force the "Edit on Bitbucket" link to a specific URL
- `:gitlab_url:` - Force the "Edit on GitLab" link to a specific URL

---

## Complete Example

Here's a complete `conf.py` example with common configurations:

```python
import pytorch_sphinx_theme2

html_theme = "pytorch_sphinx_theme2"
html_theme_path = [pytorch_sphinx_theme2.get_html_theme_path()]

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "myst_nb",
    "sphinx_tippy",
    "pytorch_sphinx_theme2",
]

# Theme options
html_theme_options = {
    # Navigation
    "navbar_align": "left",
    "navbar_start": ["navbar-logo", "version-switcher"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["search-field-custom", "theme-switcher", "navbar-icon-links"],
    "collapse_navigation": False,
    "use_edit_page_button": True,

    # Project info
    "canonical_url": "https://docs.pytorch.org/your-project/",
    "analytics_id": "UA-XXXXXXXX-X",

    # Header/Footer
    "show_lf_header": False,
    "show_lf_footer": True,

    # Icon links
    "icon_links": [
        {"name": "GitHub", "url": "https://github.com/pytorch/pytorch", "icon": "fa-brands fa-github"},
        {"name": "X", "url": "https://x.com/PyTorch", "icon": "fa-brands fa-x-twitter"},
    ],

    # Version switcher
    "switcher": {
        "json_url": "https://docs.pytorch.org/docs/pytorch-versions.json",
        "version_match": "main",
    },
}

# Context for templates
theme_variables = pytorch_sphinx_theme2.get_theme_variables()
html_context = {
    "theme_variables": theme_variables,
    "github_url": "https://github.com",
    "github_user": "pytorch",
    "github_repo": "your-repo",
    "github_version": "main",
    "doc_path": "docs",
}

# Static files
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Date info setup
def setup(app):
    app.config.add_last_updated = True
    from pytorch_sphinx_theme2 import add_date_info_to_page
    app.connect("html-page-context", add_date_info_to_page)
    return {"version": "0.1.0", "parallel_read_safe": True}
```

---

## See Also

- [PyData Sphinx Theme Documentation](https://pydata-sphinx-theme.readthedocs.io/) - The parent theme
- [Sphinx Configuration](https://www.sphinx-doc.org/en/master/usage/configuration.html) - Sphinx documentation
