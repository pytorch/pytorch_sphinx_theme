# PyTorch Sphinx Theme

Sphinx theme for [PyTorch Docs](PyTorch documentation — PyTorch master documentation) and [PyTorch Tutorials](https://pytorch.org/tutorials) based on the [Read the Docs Sphinx Theme](https://sphinx-rtd-theme.readthedocs.io/en/latest).

## Local Development (preliminary)

Clone the repo:

```
git clone git@github.com:shiftlab/pytorch_sphinx_theme.git
```

Run python setup:

```
python setup.py install
pip install pytorch_sphinx_theme
```

In the root directory install the `package.json`:

```
# node version 8.4.0
yarn install
```

Run grunt to build the html site and enable live reloading of the demo app at `localhost:1919`:

```
grunt
```

The resulting site is a demo.

### Modifying against PyTorch Docs and Tutorials

To modify the theme against the PyTorch Docs and/or the PyTorch Tutorials first clone the repositories:

- [PyTorch (Docs)](https://github.com/pytorch/pytorch)
- [PyTorch Tutorials](https://github.com/pytorch/tutorials)

Then follow the instructions in each repository to make the docs.

Once the docs have been successfully generated you should be able to run the following to create an html build.

#### Docs

```
# in ./docs
make html
```

#### Tutorials

```
# root directory
make html
```

Once these are successful, navigate to the `conf.py` file in each project. In the Docs these are at `./docs/source`. The Tutorials one can be found in the root directory.

In `conf.py` change the html theme to `pytorch_sphinx_theme` and point the html theme path to this repo's local folder, which will end up looking something like:

```
html_theme = 'pytorch_sphinx_theme'
html_theme_path = ["../../../pytorch_sphinx_theme"]
```

Next create a file `.env.json` in the root of this repo with some keys/values referencing the local folders of the Docs and Tutorials repos:

```
{
  "TUTORIALS_DIR": "../tutorials",
  "DOCS_DIR": "../pytorch/docs/source"
}

```

You can then build the Docs or Tutorials by running

```
grunt --project=docs
```
or

```
grunt --project=tutorials
```

These will generate a live-reloaded local build for the respective projects available at `localhost:1919`.

Note that while live reloading works these two projects are hefty and will take a few seconds to build and reload, especially the Docs.

### Built-in Stylesheets and Fonts

There are a couple of stylesheets and fonts inside the Docs and Tutorials repos themselves meant to override the existing theme. To ensure the most accurate styles we should comment out those files until the maintainers of those repos remove them:

#### Docs

```
# ./docs/source/conf.py

html_context = {
    # 'css_files': [
    #     'https://fonts.googleapis.com/css?family=Lato',
    #     '_static/css/pytorch_theme.css'
    # ],
}
```

#### Tutorials

```
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
