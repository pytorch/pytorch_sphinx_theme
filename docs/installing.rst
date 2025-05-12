.. meta::
   :description: This page describes hot instal pytorch_sphinx_theme in your project


************
Installation
************

Via Git or Download
===================

Symlink or subtree the ``pytorch_sphinx_theme`` repository into your documentation at
``docs/_themes/pytorch_sphinx_theme`` then add the following two settings to your Sphinx
``conf.py`` file:

.. code:: python

    html_theme = "pytorch_sphinx_theme"
    html_theme_path = ["_themes", ]

