r"""The hugoexporter module.

The docstring for a module should generally list the classes, exceptions and
functions (and any other objects) that are exported by the module, with a
one-line summary of each. (These summaries generally give less detail than the
summary line in the object's docstring.)
"""
import os.path

from .hugopreprocessor import HugoPreprocessor

from nbconvert.exporters.markdown import MarkdownExporter
from traitlets import default


class HugoExporter(MarkdownExporter):
    r"""The HugoExporter Class.

    The docstring for a class should summarize its behavior and list the public
    methods and instance variables. If the class is intended to be subclassed,
    and has an additional interface for subclasses, this interface should be
    listed separately (in the docstring). The class constructor should be
    documented in the docstring for its __init__ method. Individual methods
    should be documented by their own docstring.

    If a class subclasses another class and its behavior is mostly inherited
    from that class, its docstring should mention this and summarize the
    differences. Use the verb "override" to indicate that a subclass method
    replaces a superclass method and does not call the superclass method; use
    the verb "extend" to indicate that a subclass method calls the superclass
    method (in addition to its own behavior).  A Preprocessor to handle
    exporting to Hugo.
    """

    @property
    def template_path(self):
        r"""Return the path of the template file."""
        return super().template_path + [os.path.dirname(__file__)]

    @default('template_file')
    def _template_file_default(self):
        r"""Return the name of the template file."""
        return 'hugo_markdown.tpl'

    @property
    def preprocessors(self):
        r"""Return the list of preprocessors for this exporter."""
        return [HugoPreprocessor]
