"""Pytorch Sphinx theme.

From https://github.com/shiftlab/pytorch_sphinx_theme.

"""
import docutils.nodes as nodes
import docutils.parsers.rst.directives.admonitions as admonitions
from docutils.parsers.rst.roles import set_classes

from os import path

__version__ = '0.0.24'
__version_full__ = __version__


def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = path.abspath(path.dirname(path.dirname(__file__)))
    return cur_dir

class Deprecated(admonitions.BaseAdmonition):

    node_class = nodes.admonition

    def run(self):
        set_classes(self.options)
        self.assert_has_content()
        text = '\n'.join(self.content)
        admonition_node = self.node_class(text, **self.options)
        self.add_name(admonition_node)

        title_text = 'Deprecation'
        textnodes, messages = self.state.inline_text(title_text,
                                                        self.lineno)
        title = nodes.title(title_text, '', *textnodes)
        title.source, title.line = (
                self.state_machine.get_source_and_line(self.lineno))
        admonition_node += title
        admonition_node += messages
        if not 'classes' in self.options:
            admonition_node['classes'] += [nodes.make_id(title_text)]

        self.state.nested_parse(self.content, self.content_offset,
                                admonition_node)
        return [admonition_node]

# See http://www.sphinx-doc.org/en/stable/theming.html#distribute-your-theme-as-a-python-package
def setup(app):
    app.add_html_theme('pytorch_sphinx_theme', path.abspath(path.dirname(__file__)))
    app.add_directive('deprecated', Deprecated, override=True)
