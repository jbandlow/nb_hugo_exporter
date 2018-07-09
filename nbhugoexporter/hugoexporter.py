r"""The hugoexporter module.

This module exports a single class:

    HugoExporter: An `nbconvert` `MarkdownExporter` for exporting notebooks
        to a Markdown format compatible with [Hugo](https://gohugo.io)

"""
import os.path

from .hugopreprocessor import HugoPreprocessor

from nbconvert.exporters.markdown import MarkdownExporter
from traitlets import default


class HugoExporter(MarkdownExporter):
    r"""The HugoExporter class.

    This class overrides the `MarkdownExporter` of `nbconvert` to use a custom
    template and preprocessor. It is registered as an `entry_point` in
    `setup.py` as follows
    ```
        'nbconvert.exporters': [
            'hugo = nbhugoexporter.hugoexporter:HugoExporter',
        ]
    ```
    """

    @property
    def template_path(self):
        r"""Override and return the path of the template file."""
        return super().template_path + [os.path.dirname(__file__)]

    @default('template_file')
    def _template_file_default(self):
        r"""Override and return the name of the template file."""
        return 'hugo_markdown.tpl'

    @property
    def preprocessors(self):
        r"""Override and eturn the list of preprocessors for this exporter."""
        return [HugoPreprocessor]
