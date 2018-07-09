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
        r"""Extend the template_path to include this library's directory."""
        return super().template_path + [os.path.dirname(__file__)]

    @default('template_file')
    def _template_file_default(self):
        r"""Override and return the traitlet template_file."""
        return 'hugo_markdown.tpl'

    @property
    def preprocessors(self):
        r"""Extend the list of preprocessors to include HugoPreprocessor."""
        return super().preprocessors + [HugoPreprocessor]

    def _init_resources(self, resources):
        r"""Extend resources dictionary initialization.

        - Make sure the primary output filename is `index.md`
        - Do not create a subdirectory for output files, use the `output-dir`
          directory.
        """
        resources = super()._init_resources(resources)
        resources['unique_key'] = 'index'
        resources['output_files_dir'] = '.'
        return resources
