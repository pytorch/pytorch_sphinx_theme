# Changelog

All notable changes to pytorch_sphinx_theme2 are documented here.

## v0.4.13

### Bug Fixes

- **Duplicate Search Results Collapsed** (PR #255) — Follow-up to #252, addressing the other half of the upstream report. `performSearch` runs a title, object and fulltext pass that each emit their own row for one page, and the built-in dedup keys on `[docname, title, anchor, descr, filename]`, which differs per pass — so a single symbol page was listed repeatedly. Rows were also labelled with whichever heading matched, so searching `linear` produced eight indistinguishable `Linear` entries. Rows for one `generated/<symbol>` page now collapse into a single entry labelled with that symbol. Same-page duplicates in the top 10: `nn.linear` 4 to 0, `conv2d` 2 to 0.

---

## v0.4.12

### Bug Fixes

- **Search Relevance for Symbol Queries** (PR #252) — Replaced Sphinx's stock `Scorer` so API symbols rank above module stub pages. The Python domain gives every module search priority 0 (worth +15) against +5 for classes and functions, and `performSearch` merges three passes onto one list without normalising their scales. Searching `nn.linear` returned twelve `*.modules.linear` module pages ahead of `torch.nn.Linear` at rank 29; it is now first. Measured over 16 symbol queries against the PyTorch `main` index: MRR 0.488 to 0.969, top-1 4/16 to 15/16.

### Infrastructure

- **GitHub Actions Node 20 Deprecation** (PR #253) — Bumped `actions/checkout`, `actions/setup-python`, `actions/setup-node`, `actions/upload-artifact` and `actions/download-artifact` to their current majors.

---

## v0.4.11

Released to PyPI on 2026-05-19. The version bump itself was never merged, so this entry is recorded retroactively.

### Bug Fixes

- **Dropdown Width Fix** (PR #251) — `sphinx-design` dropdowns are rendered as `.sd-card`, so they inherited the card constraints and were clipped to the card width (500px at mobile breakpoints). `.sd-card.sd-dropdown` now spans the full container width, and the card hover underline pseudo-element is suppressed on dropdowns.

### Documentation

- **MyST Directives Test Page** (PR #251) — Added `docs/test-myst-directives.md` covering the MyST directive set, and enabled the `fieldlist`, `substitution`, `tasklist`, `attrs_inline` and `attrs_block` extensions plus `myst_substitutions` in `docs/conf.py`.

---

## v0.4.10

### Bug Fixes

- **C++ Docs Navbar Bullets Fix** — Fixed top navigation bar rendering as a bulleted list in C++ docs. Wrapped fallback `generate_header_nav_html()` output in proper `<nav><ul class="bd-navbar-elements navbar-nav">` markup, and added `env-merge-info` handler to preserve toctree entries across parallel build workers.
- **Right Nav Spacing Fix** — Fixed excessive vertical spacing between "On this page" TOC entries by switching `.page-toc .section-nav` from flex to block layout, restoring proper margin collapsing between items.

---

## v0.4.9

### Performance

- **Optimized llms-full.txt Generation** (PR #244) — Added `llm_generate_full` theme option to skip expensive llms-full.txt generation on large builds. Uses `lxml` parser when available for faster HTML-to-markdown conversion. Capped parallel workers at 8 and added progress logging.

### Bug Fixes

- **Navbar Fix for Parallel Writes** (PR #245) — Fixed empty navbar when doctree disk writes are skipped (e.g., by PyTorch CI optimization PR #180177). Toctree entries are now cached during the read phase via `doctree-read` so all parallel write workers have access to navigation data.

---

## v0.4.7

### New Features

- **Markdown Generation for LLM Docs** (PR #239) — Refactored the LLM content generation into a dedicated `llm_generation.py` module with a new markdown generation function. Added support for new theme options and comprehensive test coverage.

- **Collapsible List Component** (PR #240) — Added collapsible list styles and JavaScript for C++ documentation pages. Supports nested expandable/collapsible sections with smooth animations.

### Bug Fixes

- **Right Nav Scroll Fix** (PR #240) — Fixed right-side navigation scroll behavior in the layout template.

- **Google Search Thumbnail Fix** (PR #241) — Fixed red X thumbnail appearing in Google search results by updating component styles and cookie banner markup.

---

## v0.4.6

### Improvements

- **LLM Navigation Guide (llms.txt) Improvements** (PR #237) — Enhanced the `llms.txt` generator with several fixes:
  - Now enabled by default — generates `llms.txt` automatically unless disabled or a custom file is provided
  - Spec-compliant format with H1 title, quote block description, H2 sections, and proper title format
  - Added optional `llm_deduplicate_titles` theme option to disambiguate duplicate titles (e.g., "GRU" → "GRU (torch.nn.GRU)")
  - Generic fallback uses project name for description if `llm_description` is not set

### Bug Fixes

- **Google Search Fix** (PR #236) — Fixed issues with the Google custom search bar styling and responsive behavior

---

## v0.4.5

### New Features

- **Announcement Banner** (PR #231) — Added configurable announcement banner component for displaying site-wide notifications, surveys, and announcements. Supports customizable text, link, background color, and optional dismiss button. Configure via `announcement` theme option with `text`, `link`, `background_color`, and `dismissable` properties.

### Bug Fixes

- **Cookie Policy Link Update** (PR #230) — Updated the cookie policy link in the cookie banner to point to the correct URL.

---

## v0.4.4

- **Tutorial Card Image Sizing Fix** — Constrained tutorial card images to a fixed width (`200px` desktop, `175px` tablet) instead of `25%`, and switched the `<img>` to `max-width: 100%; max-height: 100%; object-fit: contain` so images maintain their aspect ratio. Images are now centered within the container using flexbox.

---

## v0.4.3

- **Custom `llms.txt` Support** — Projects can provide their own hand-crafted `llms.txt` instead of relying on auto-generation. Two mechanisms are supported: (1) set the `llm_custom_file` theme option to point to a file relative to the source directory, or (2) place an `llms.txt` file in the Sphinx source root (next to `conf.py`) and it will be used automatically. The resolution order is: explicit `llm_custom_file` → source-root convention → auto-generation.
- **Version Switcher Compact Display** — The version-switcher dropdown button now truncates long version strings (e.g. `v2.11.0 (cu128)` → `v2.11.0`) using CSS `max-width` with `text-overflow: ellipsis`. The version text is styled in the theme's primary color with bold weight. The dropdown caret is absolutely positioned so it remains visible despite the overflow clipping.
- **Logo-to-Version Spacing** — Added `0.5rem` left margin between the navbar logo and the version switcher to prevent them from appearing too close together.
- Minor code formatting and comment cleanup in `docs/conf.py` and `theme.conf`.

---

## v0.4.2

### Bug Fixes

- **Oversized Navbar Logo** — Constrained the desktop navbar logo to `max-height: 20px` so it sits proportionally within the 45px header bar instead of rendering at full SVG size.

### Improvements

- **LLM URL Resolution Fallback** — The `llms.txt` generator now resolves page URLs through a three-tier fallback: `llm_domain` + `llm_base_path` → Sphinx `html_baseurl` → relative URLs. Previously, only `llm_domain` or relative URLs were supported, which meant projects using `html_baseurl` without `llm_domain` got relative-only links.

---

## v0.4.0

### New Features

- **Dropdown Navigation Menus** (PR #225) — The horizontal navbar now supports hierarchical dropdown menus. Top-level toctree entries with children display hover-activated dropdowns on desktop. Overflow items collapse into a "More" dropdown. External URLs are supported. Configurable via `enable_navbar_dropdowns` theme option (default: `true`). Pure CSS — no JavaScript required.
- **LLM Discovery Support** — Automatically generates `/llms.txt` at build time listing all documentation pages as Markdown links, following the [llms.txt standard](https://llmstxt.org/). Every page includes machine-readable `<meta name="llm:*">` tags (site-type, framework, description, version, page-type, navigation-file, sitemap). Configured via `llm_domain`, `llm_base_path`, `llm_description`, and `llm_disabled` theme options.
- **RunLLM Widget Integration** (PR #216) — AI-powered documentation assistant widget. Enable by setting `runllm_assistant_id` in theme options. Additional options: `runllm_name`, `runllm_position`, `runllm_keyboard_shortcut`.
- **Sphinx-Tippy Parallel Build Fix** — Fixes tooltip data loss when using sphinx-tippy with parallel Sphinx builds. Glossary terms are now extracted during the read phase and properly merged across workers. Configurable glossary page via `tippy_glossary_page` setting.
- **Page Date Information** — Displays "Created On" and "Last Updated On" dates below page titles, sourced from git history. Enable with `add_last_updated = True`. Supports `paths_to_skip` for excluding specific pages.
- **SEO Structured Data** — Every page now includes JSON-LD structured data (`Article` schema) with headline, description, URL, author, dates, and image. Hidden breadcrumb schema for search engine optimization. OpenGraph image meta tag support.
- **Configurable Tutorial Call-to-Action Links** — "Run in Colab", "Download Notebook", and "View on GitHub" buttons now work for any repository via `github_user`, `github_repo`, `github_version`, and `colab_branch` in `html_context`.

### UI/Layout Improvements

- **Responsive Layout Overhaul** (PR #223) — Wide screen content capped at `max-width: 1800px` with auto centering. Progressive navbar font and padding compaction across three breakpoints to prevent wrapping. Adaptive header padding for desktop and mobile.
- **Auto-Hide Empty Sidebar** (PR #226) — Left sidebar automatically hides via CSS when it contains no navigation items, with main content padding adjusted accordingly.
- **Smooth Scroll with TOC Locking** — Custom smooth scroll animation. Clicking an anchor link locks the TOC highlight to that target until the user manually scrolls.
- **Myst-NB Code Cell Styling** — Styled code cells and output cells with "Out:" labels, matching the tutorials page look.
- **Conditional Header/Footer Height** — Dynamic CSS variable adjustment when `show_lf_header` or `show_lf_footer` are disabled.

### Bug Fixes

- Fixed broken external links in the navigation bar.
- Fixed top padding layout on mobile.
- Fixed sidebar positioning with proper viewport height calculation on desktop.
- Fixed search page scroll by overriding height and overflow restrictions on result containers.
- Fixed glossary page path references.
- Fixed cookie banner to properly hide on localhost, `docs.pytorch.org`, `docs-preview.pytorch.org`, and local network addresses.

### Content/Data Updates

- Updated PyTorch library links to include only libraries in the official PyTorch GitHub org.
- Added comprehensive configuration reference documentation covering all theme options with examples.

### Infrastructure

- Modernized CI workflows (PR #219).
- Added Netlify documentation preview support (PR #221).
- Added S3 documentation preview upload (PR #222).

---

## v0.3.0

### New Features

- **Tippy.js Tooltips Support** (PR #212, #213) — Added glossary tooltips using tippy.js, with a parallel build fix to prevent data loss in multi-worker Sphinx builds.
- **Top Navigation Bar Dropdown Categories** (PR #210) — Updated the top navigation bar with reorganized dropdown categories.

### Bug Fixes

- Fixed 404.html template to use JavaScript-based path detection, ensuring the "Back Home" button works across all deployment paths.
- Fixed JSON-LD structured data to use `Article` schema with `articleBody`.
- Fixed search highlighting.
- Fixed OG image path.
- Fixed copyright banner for non-LF projects.
- Fixed Sphinx footer for non-LF projects.
- Hid old cookie banner on `docs.pytorch.org`; added Osano cookie consent for LF-owned domains.
- Fixed `canonical_url` to avoid duplicates.
- Fixed `includenodoc` directive to parse raw docstrings (PR #209).
- Fixed condition for sphinx-gallery widgets at the top of the page.

### Improvements

- Removed the `override-version` script (PR #214).
- Updated requirements.txt (PR #211).
- Updated `theme_variables` with correct links.
- Added condition for tutorials-specific widgets.
- Updated output cell styles for `--sg-script-pre`.
- Updated sitemap settings and version acquisition.

---

## v0.0.18 and earlier

Initial versions of `pytorch_sphinx_theme2`, based on `pydata-sphinx-theme`. Included core layout, navigation, styling, and sphinx-gallery integration for PyTorch documentation sites.
