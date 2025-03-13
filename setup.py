from setuptools import find_packages, setup

setup(
    name="pytorch_sphinx_theme2",
    version="0.1.0",
    install_requires=["pydata-sphinx-theme"],
    packages=["pytorch_sphinx_theme2"],
    include_package_data=True,
    package_data={
        "pytorch_sphinx_theme2": [
            "theme.conf",
            "*.html",
            "templates/*.html",
            "templates/sections/*.html",
            "static/css/*.css",
            "static/js/*.js",
            "static/img/*",
            "static/scss/*.scss",
            "theme_variables.jinja",
            "links.json",
        ],
    },
)
