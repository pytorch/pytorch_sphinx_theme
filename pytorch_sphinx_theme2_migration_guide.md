# PyTorch Sphinx Theme Migration Guide
This guide will help you migrate from pytorch_sphinx_theme to pytorch_sphinx_theme2.
pytorch_sphinx_theme2 is based on pydata_sphinx_theme with a few overrides specific to 
pytorch. pydata_sphinx_theme has a great [documentation](https://pydata-sphinx-theme.readthedocs.io/en/stable/)
that can help answer a lot of the theme configuration-related questions.
## Step 1: Clean Up Custom Overrides
Delete all local overrides in `layout.html`. If you have special requirements, file an issue in this repo.
Remove custom CSS files (most likely all `custom.css` can be deleted).

## Step 2: Update `requirements.txt`

For pytorch_sphinx_theme2 theme, requirements should inlcude:
```
sphinx==5.3.0
-e git+https://github.com/pytorch/pytorch_sphinx_theme.git@pytorch_sphinx_theme2#egg=pytorch_sphinx_theme2
sphinxcontrib.katex==0.8.6
sphinxext-opengraph==0.9.1
breathe==4.34.0  # only if generating C++
exhale==0.2.3  # only if generating C++ docs
docutils==0.16
sphinx-design==0.4.0
sphinxcontrib-mermaid==1.0.0
myst-parser==0.18.1  # if want to contribute in markdown
sphinx-gallery==0.11.1  # if hosting interactive tutorials
```

## Step 3: Update `conf.py`

Add imports and theme settings:
```
sys.path.insert(0, os.path.abspath("."))
import pytorch_sphinx_theme2

html_theme = "pytorch_sphinx_theme2"
html_theme_path = [pytorch_sphinx_theme2.get_html_theme_path()]
```

Add opengraph protocol settings: 
```
ogp_site_url = "http://pytorch.org/<your-sub-site>"
ogp_image = "https://pytorch.org/assets/images/social-share.jpg"
```


Add these extensions:

```
extensions = [
    ...
    "sphinx_design",
    "sphinx_sitemap",
    "sphinxcontrib.mermaid",
    "pytorch_sphinx_theme2",
    "sphinxext.opengraph",
]
```

Navbar settings:

```
html_theme_options = {
    "navigation_with_keys": False,
    "analytics_id": "GTM-T8XT4PS",
    "pytorch_project": "tutorials",
    "logo": {
        "text": "",
    },
    "icon_links": [
        {
            "name": "X",
            "url": "https://x.com/PyTorch",
            "icon": "fa-brands fa-x-twitter",
        },
        {
            "name": "GitHub",
            "url": "https://github.com/pytorch/<your-repo>",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "Discourse",
            "url": "https://dev-discuss.pytorch.org/",
            "icon": "fa-brands fa-discourse",
        },
        {
            "name": "PyPi",
            "url": "https://pypi.org/project/<your-project>/",
            "icon": "fa-brands fa-python",
        },
    ],
    "use_edit_page_button": True,
    "navbar_center": "navbar-nav",
}

theme_variables = pytorch_sphinx_theme2.get_theme_variables()
templates_path = [
    "_templates",
    os.path.join(os.path.dirname(pytorch_sphinx_theme2.__file__), "templates"),
]

html_context = {
    "theme_variables": theme_variables,
    "display_github": True,
    "github_url": "https://github.com",
    "github_user": "pytorch",
    "github_repo": "<your-repo>",
    "feedback_url": "https://github.com/pytorch/<path-to-your-repo>",
    "github_version": "main",
    "doc_path": "docs/source",
    "library_links": theme_variables.get("library_links", []),
    "community_links": theme_variables.get("community_links", []),
    "language_bindings_links": html_theme_options.get("language_bindings_links", []),
}
```

If using myst-markdown, add:
```
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_image",
]
```

For special requirements, contact the PyTorch documentation team or create an issue in this repo.

## Restructuring your index.rst/index.md

The pytorch_sphinx_theme2 uses a horizontal navigation bar for your top-level toctree entries. To optimize this layout:

* Consolidate related topics into logical groups
* Limit top-level navigation items (5-7 items work best)
* Use nested toctrees for detailed subsections

Example structure for a typical library:

```
.. toctree::
   :maxdepth: 1
   :hidden:
   
   get_started
   
.. toctree::
   :maxdepth: 1
   :hidden:
   
   tutorials

.. toctree::
   :maxdepth: 1
   :hidden:
   
   api
   
.. toctree::
   :maxdepth: 1
   :hidden:

   howtos

.. toctree::
   :maxdepth: 1
   :hidden:

   glossary
```
The theme uses a two-level navigation system:

* Horizontal Navigation Bar (Top):
  * Each top-level toctree in your `index.rst`/`index.md` appears as a section in this bar.
    These are your main content categories
  * **Important:** Keep these section titles short, preferably single words like "Docs", "Tutorials", "API", "Examples" to avoid overcrowding the navigation bar
* Left Sidebar Navigation:
  * Shows the contents of the currently selected section.
  * Populated by the `toctree` inside the page referenced by the top nav

Example Structure:
```
index.rst (Top navigation - items that will appear on the horizontal bar)
├── get_started.rst (Contains its own toctree for left nav)
├── user_guide.rst (Contains its own toctree for left nav)
├── tutorials.rst (Contains its own toctree for left nav)
└── compilers.rst (Contains its own toctree for left nav)
```
In the PyTorch tutorials example, clicking **Compilers** in the top nav loads `compilers.rst`, which has its own toctrees that populate
the left sidebar with compiler-related topics.

The image shows this in action - **Compilers** is selected in the top nav, and its subtopics appear in the left sidebar.

![compilers page](https://github.com/user-attachments/assets/40c741b0-0f7a-4e0d-a417-9636507f537c)

## Version switcher

There are two options for configuring version information in your documentation:

**Option 1:** Add a version switcher dropdown - for projects that already have multiple versions.

Here is how it will look:
![version-switcher](https://github.com/user-attachments/assets/a82005d2-b7c2-46c1-9d99-32884269637c)

1. Create a `mypackage-versions.json` and host in your repo's gh-pages branch. Example: https://github.com/pytorch/docs/blob/site/pytorch-versions.json
   **NOTE:** The `pytorch-versions.json` file is hosted in a separate repo, but you should host in the gh-pages branch of your own repo in most cases.
   Your versions.json needs to have exactly **one** version set as preferred. Typically, it is the **stable** version.
3. In your `conf.py`, configure:
   ```
   # Get a version of your package. Example for torch:
   torch_version = str(torch.__version__)

   version = "main (" + torch_version + " )"
   release = "main"

   if RELEASE:
     # Turn 1.11.0aHASH into 1.11
     version = ".".join(torch_version.split(".")[:2])
     html_title = " ".join((project, version, "documentation"))
     release = version

   # for the switcher, use:
   switcher_version = "main" if not RELEASE else version
   html_theme_options = {
     # other options...
     "switcher": {
         "json_url": "https://pytorch.org/<path-to-versions-json>",
         "version_match": switcher_version,
     },
     "show_version_warning_banner": True,  # Adds a banner for non-preferred versions
   }

**Option 2:** Display version in the navbar - if your project is new and you don't really have any versions.
Here is an example:

![version_hardcoded](https://github.com/user-attachments/assets/e456ece2-9269-479f-a5d7-7328dc03db07)
1. Configure in `conf.py`:
```
# In conf.py get a version. For example:
version = "v" + str(torch.__version__)
# Set html_options to the following:
html_theme_options = {
    # other options...
    "navbar_start": ["pytorch_version"], # pytorch_version is a JINJA template that it will use.
    "display_version": True,
}
```
