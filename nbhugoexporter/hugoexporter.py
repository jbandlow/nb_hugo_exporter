import os.path

from .hugopreprocessor import HugoPreprocessor

from nbconvert.exporters.markdown import MarkdownExporter
from traitlets import default


class HugoExporter(MarkdownExporter):
    @property
    def template_path(self):
        return super().template_path + [os.path.dirname(__file__)]

    @default('template_file')
    def _template_file_default(self):
        return 'hugo_markdown.tpl'

    @property
    def preprocessors(self):
        return [HugoPreprocessor]
