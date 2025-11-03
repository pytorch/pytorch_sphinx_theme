# PyTorch Sphinx Theme

Sphinx theme for [PyTorch Docs](https://pytorch.org/docs/master/torch.html) and [PyTorch Tutorials](https://pytorch.org/tutorials) based on the [pydata_sphinx_theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/index.html).

## Contributing to the theme

To contribute to this theme, edit the files in the `pytorch_sphinx_theme2`
directory.

To make a request for an improvement or new feature, please file an
issue in this repo.

### Styling Changes
To make changes to the styling, edit the SCSS files in
`pytorch_sphinx_theme2/static/scss/`. These files will be compiled
into `theme.css` using Grunt. Do not make changes in the `theme.css`

### Template Changes
To make changes to the templates, edit the HTML files in
`pytorch_sphinx_theme2/templates/` directory.

### JavaScript Changes
To make changes to JavaScript functionality, edit the JS files in
`pytorch_sphinx_theme2/static/js/ directory`. These files will be
concatenated into a single `theme.js` file using Grunt. Do not
make changes in the `theme.js`

## Local Development

Install PyTorch Sphinx Theme:

```
git clone https://github.com/pytorch/pytorch_sphinx_theme
cd pytorch_sphinx_theme
git checkout pytorch_sphinx_theme2  # The default branch is pytorch_sphinx_theme2
pip install -r docs/requirements.txt # Installs dependencies
pip install -e . # Installs local version of the theme
```

**Note:** The default branch for this repository is `pytorch_sphinx_theme2`.

In the root directory, install the dependencies using
using `npm install`:

```
npm install grunt --save-dev
npm install grunt-sass sass grunt-contrib-concat grunt-contrib-watch grunt-shell --save-dev
```

To test your changes locally:

1. Install all the needed dependencies described above.
2. Make your changes.
3. Run `npx grunt docs`. This command will:

   * Compile SCSS to `theme.css`.
   * Concatenate JS files into `theme.js`.
   * Reinstall the theme package.
   * Build the test documentation stored in the `docs/` directory.
   * Start a local server at `http:8000`.
   * Watch for changes to SCSS and JS files.

When applying subsequent changes, you might need to reinstall the theme
by running `pip uninstall -y pytorch_sphinx_theme2` and `pip install -e .`,
and then running the `npx grunt docs` again.

DO NOT submit a PR without running Grunt. We only reference theme.css
and theme.js in the theme, so those need to be compiled with your
changes and the PR needs to have those files updated.

## Testing your changes and submitting a PR

When you are ready to submit a PR with your changes you can first test
that your changes have been applied correctly against either the PyTorch Docs or Tutorials repo:

1. Run the `grunt build` task on your branch and commit the build to Github.
2. In your local docs or tutorials repo, remove any existing `pytorch_sphinx_theme` packages in the `src` folder (there should be a `pip-delete-this-directory.txt` file there)
3. Clone the repo locally `git clone https://github.com/pytorch/pytorch_sphinx_theme`
4. Install `pytorch_sphinx_theme` by running `pip install -e pytorch_sphinx_theme`
5. Install the requirements `pip install -r requirements.txt`
6. Remove the current build. In the docs this is `make clean`, tutorials is `make clean-cache`
7. Build the static site. In the docs this is `make html`, tutorials is `make html-noplot`
8. Open the site and look around. In the docs open `docs/build/html/index.html`, in the tutorials open `_build/html.index.html`

If your changes have been applied successfully, remove the build commit from your branch and submit your PR.

## Publishing the theme

Before the new changes are visible in the theme the maintainer will
need to run the build process:

```bash
npx grunt
```

Once that is successful commit the change to Github.

## Building and Publishing to PyPI

To build and publish a new version of the theme to PyPI, follow these steps:

### 1. Update the version number

Update the version number in `setup.py`:

```python
version="0.1.0",  # Change to your new version
```

### 2. Build the theme assets

Compile SCSS and concatenate JS files:

```bash
npx grunt
```

This runs the default Grunt task which cleans, copies FontAwesome assets, compiles SCSS to CSS, and concatenates JS files.

### 3. Build the wheel

Clean previous builds and create a new wheel:

```bash
# Clean previous builds
rm -rf dist/ build/ pytorch_sphinx_theme2.egg-info/

# Build the wheel (using modern build tools)
pip install build
python -m build
```

Alternatively, using setuptools directly:

```bash
python setup.py sdist bdist_wheel
```

This will create two files in the `dist/` directory:
- `pytorch_sphinx_theme2-{version}-py3-none-any.whl`
- `pytorch_sphinx_theme2-{version}.tar.gz`

### 4. Publish to PyPI

**Option A: Install in current environment**

Note that the latest twine and readme-renderer require `docutils>=0.21.2`, which conflicts with Sphinx's requirement for `docutils<0.21`. First, upgrade pip and setuptools, then install compatible versions:

```bash
pip install --upgrade pip setuptools wheel
pip install --upgrade importlib_metadata
pip install 'twine<5.0' 'readme-renderer<44.0'
```

**Option B: Use a separate environment (recommended)**

This avoids all dependency conflicts.

For conda users:

```bash
conda create -n publish_env python=3.10
conda activate publish_env
pip install --upgrade pip setuptools wheel
pip install build twine
```

For venv users:

```bash
python -m venv publish_env
source publish_env/bin/activate  # On Windows: publish_env\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install build twine
```

**Authentication Setup**

Before publishing, you need to set up authentication:

1. Create accounts:
   - TestPyPI: https://test.pypi.org/account/register/
   - PyPI: https://pypi.org/account/register/

2. Create API tokens:
   - TestPyPI token: https://test.pypi.org/manage/account/token/
   - PyPI token: https://pypi.org/manage/account/token/

3. Configure `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN-HERE

[pypi]
repository = https://pypi.org/legacy/
username = __token__
password = pypi-YOUR-PYPI-TOKEN-HERE
```

Replace `pypi-YOUR-TESTPYPI-TOKEN-HERE` and `pypi-YOUR-PYPI-TOKEN-HERE` with your actual tokens.

**Publishing**

For testing, publish to TestPyPI first:

```bash
twine upload --repository testpypi dist/*
```

Once verified, publish to PyPI:

```bash
twine upload dist/*
```

### Developing locally against PyTorch Docs and Tutorials

To be able to modify and preview the theme locally against the PyTorch Docs and/or the PyTorch Tutorials first clone the repositories:

```bash
git clone https://github.com/pytorch/pytorch
git clone https://github.com/pytorch/tutorials
```

Then follow the instructions in each repository to make the docs.

Once the docs have been successfully generated you should be able to run the following to create an html build.

#### pytorch/pytorch/docs

```bash
cd pytorch/docs
make html
```

#### Tutorials

```bash
cd tutorials
make html
```

Once these are successful, navigate to the `conf.py` file in each project. In the Docs these are at `./docs/source`. The Tutorials one can be found in the root directory.

In `conf.py` change the html theme to `pytorch_sphinx_theme` and point the html theme path to this repo's local folder, which will end up looking something like:

```
html_theme = 'pytorch_sphinx_theme'
html_theme_path = ["../../../pytorch_sphinx_theme"]
```

Next create a file `.env.json` in the root of this repo with some keys/values referencing the local folders of the Docs and Tutorials repos:

```json
{
  "TUTORIALS_DIR": "../tutorials",
  "DOCS_DIR": "../pytorch/docs/source"
}
```

You can then build the Docs or Tutorials by running

```bash
grunt --project=docs
```
or

```bash
grunt --project=tutorials
```

These will generate a live-reloaded local build for the respective projects available at `localhost:1919`.

Note that while live reloading works these two projects are hefty and will take a few seconds to build and reload, especially the Docs.

### Built-in Stylesheets and Fonts

There are a couple of stylesheets and fonts inside the Docs and Tutorials repos themselves meant to override the existing theme. To ensure the most accurate styles we should comment out those files until the maintainers of those repos remove them:

#### pytorch/pytorch/docs

```python
# ./docs/source/conf.py

html_context = {
    # 'css_files': [
    #     'https://fonts.googleapis.com/css?family=Lato',
    #     '_static/css/pytorch_theme.css'
    # ],
}
```

#### pytorch/tutorials

```python
# ./conf.py

# app.add_stylesheet('css/pytorch_theme.css')
# app.add_stylesheet('https://fonts.googleapis.com/css?family=Lato')
```

### Top/Mobile Navigation

The top navigation and mobile menu expect an "active" state for one of the menu items. To ensure that either "Docs" or "Tutorials" is marked as active, set the following config value in the respective `conf.py`, where `{project}` is either `"docs"` or `"tutorials"`.

```
html_theme_options = {
  ...
  'pytorch_project': {project}
  ...
}
```
