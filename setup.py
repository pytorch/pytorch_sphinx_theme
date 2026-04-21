from setuptools import setup  # noqa: F401

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pytorch_sphinx_theme2",
    description="PyTorch Sphinx Theme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="PyTorch Team",
    author_email="svekars@meta.com",
    url="https://github.com/pytorch/pytorch_sphinx_theme",
    license="MIT",
    version="0.4.8",
    install_requires=[
        "pydata-sphinx-theme==0.15.4",
        "sphinx>=5.3.0,<=7.2.6",
    ],
    packages=["pytorch_sphinx_theme2"],
    include_package_data=True,
    package_data={
        "pytorch_sphinx_theme2": [
            "theme.conf",
            "*.html",
            "templates/*.html",
            "templates/sections/*.html",
            "templates/components/*.html",
            "static/css/*.css",
            "static/js/*.js",
            "static/img/*",
            "static/scss/*.scss",
            "theme_variables.jinja",
            "links.json",
        ],
    },
    entry_points={
        "sphinx.html_themes": [
            "pytorch_sphinx_theme2 = pytorch_sphinx_theme2",
        ],
    },
    python_requires=">=3.7",
)
