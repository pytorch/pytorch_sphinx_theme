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

### LLM Discovery Configuration

The theme includes built-in support for helping AI agents and LLMs discover and navigate the documentation effectively. This follows the emerging [llms.txt](https://llmstxt.org/) standard.

#### How It Works

When enabled, the theme:
1. Generates a `/llms.txt` file at the site root with navigation guidance
2. Adds machine-readable `<meta name="llm:*">` tags to every page
3. Includes a `<link rel="alternate">` pointing to the llms.txt file

#### `llm_description`
- **Type:** String
- **Default:** `""` (auto-generated from project name)
- **Description:** A brief description of the site for LLMs. Appears in the `llm:description` meta tag and at the top of `llms.txt`.

```python
html_theme_options = {
    "llm_description": "TorchVision provides datasets, models, and transforms for computer vision tasks.",
}
```

#### `llm_content_types`
- **Type:** String (comma-separated list)
- **Default:** `"api-reference, tutorials, guides, examples"`
- **Description:** Types of content available on the site. Helps LLMs understand what to expect.

```python
html_theme_options = {
    "llm_content_types": "api-reference, tutorials, examples",
}
```

#### `llm_language`
- **Type:** String
- **Default:** `"python"`
- **Description:** Primary programming language of the documentation/code examples.

```python
html_theme_options = {
    "llm_language": "python",
}
```

#### `llm_important_pages`
- **Type:** String (comma-separated list)
- **Default:** `""`
- **Description:** Key entry points for the documentation. Helps LLMs know where to start.

```python
html_theme_options = {
    "llm_important_pages": "getting-started, api/index, tutorials/quickstart",
}
```

#### `llm_custom_llms_txt`
- **Type:** String
- **Default:** `""`
- **Description:** Custom content for the `llms.txt` file. If provided, this replaces the auto-generated template entirely. Use this for complete control over the LLM guidance.

```python
html_theme_options = {
    "llm_custom_llms_txt": """# Custom LLM Guide for MyProject
> MyProject is a specialized library for...

## Key APIs
- my_module.function_a()
- my_module.function_b()
""",
}
```

#### `llm_disabled`
- **Type:** Boolean
- **Default:** `False`
- **Description:** If `True`, disables all LLM discovery features (no `llms.txt` generation, no meta tags).

```python
html_theme_options = {
    "llm_disabled": True,  # Disable LLM discovery features
}
```

#### Generated Meta Tags

The theme automatically adds the following meta tags to every page. When `llm_domain` or `canonical_url` are configured, absolute URLs are generated:

```html
<meta name="llm:site-type" content="documentation">
<meta name="llm:framework" content="PyTorch">
<meta name="llm:generator" content="Sphinx">
<meta name="llm:description" content="...">
<meta name="llm:navigation-file" content="https://pytorch.org/tutorials/llms.txt">
<meta name="llm:sitemap" content="https://pytorch.org/tutorials/sitemap.xml">
<meta name="llm:version" content="2.0.0">
<meta name="llm:project" content="PyTorch Tutorials">
<meta name="llm:page-type" content="api|tutorial|documentation">
<link rel="alternate" type="text/plain" href="https://pytorch.org/tutorials/llms.txt" title="LLM Navigation Guide">
```

The base URL is determined in this order of precedence:
1. `llm_domain` + `llm_base_path` (if `llm_domain` is set)
2. `canonical_url` (if set)
3. Root-relative paths (e.g., `/llms.txt`) as fallback

#### Example Configuration for TorchVision

```python
html_theme_options = {
    # ... other options ...

    # LLM Discovery
    "llm_description": "TorchVision provides datasets, model architectures, and image transforms for computer vision. Part of the PyTorch ecosystem.",
    "llm_content_types": "api-reference, tutorials, examples, datasets",
    "llm_language": "python",
    "llm_important_pages": "index, models, datasets, transforms",
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
