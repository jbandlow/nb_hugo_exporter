import os.path
import re

from nbconvert.exporters.markdown import MarkdownExporter
from nbconvert.preprocessors import Preprocessor

from traitlets import default
from traitlets.config import Config

class UnderscorePreprocessor(Preprocessor):
    """
    A Preprocessor to quote underscores in math mode. See
    https://gohugo.io/content-management/formats/#issues-with-markdown for
    more context on the problem. This resolves the issue with the "tedious"
    solution of quoting all underscores.
    """
    def quote_underscores_in_latex(self, string, latex):
        """
        Return a modified `string`, where all '_' in `latex` have been quoted.

        Args:
            string: A string which contains `latex` as a substring
            latex: A substring of `string` consisting of actual Latex

        Returns: A copy of `string`, where every underscore inside `latex` is
                 replaced by '\_'
        """
        quoted_latex = latex.replace(r'_', r'\_')
        return string.replace(latex, quoted_latex)


    def extract_latex(self, markdown):
        """
        A list of the blocks of latex occurring in `markdown`.

        Args:
            markdown: A string

        Returns: A list of the strings of latex, including delimiters.
        """
        # TODO: The other possible latex delimiters.

        # "$$ but not \$$" "anything not ending in \"  "$$".
        display_math = re.compile(r'[^\\](\$\$.*?[^\\]\$\$)')
        out = re.findall(display_math, markdown, re.DOTALL)

        # "$ but not \$ or $$"  "anything not ending in \"  "$".
        inline_math =  re.compile(r'[^\$\\](\$.*?[^\\]\$)')
        # Inline math cannot span two newlines.
        for block in markdown.split('\n\n'):
            out += re.findall(inline_math, block, re.DOTALL)

        return out


    def preprocess_cell(self, cell, resources, cell_index):
        """
        Quote the underscores in Latex appearing in the cell.

        Args: See the `nbconvert.preprocessors.Preprocessor` documentation
        Returns: The tuple `(cell, resources)`, where `cell` has been modified
                 so that every '_' in Latex that is part of a markdown cell or
                 output of type 'text/latex' is preceded by '\'.
        """
        if cell.cell_type == 'markdown':
            latex_segments = self.extract_latex(cell.source)
            for latex in latex_segments:
                cell.source = self.quote_underscores_in_latex(cell.source, latex)

        elif cell.cell_type == 'code':
            for o in cell.outputs or []:
                latex = o.get('data', {}).get('text/latex')
                if latex:
                    o['data']['text/latex'] = self.quote_underscores_in_latex(latex, latex)
        return cell, resources


    def preprocess(self, nb, resources):
        """
        """
        metadata = resources['metadata']
        if metadata.get('hugo') is None:
            metadata['hugo'] = {}
        hugo = metadata['hugo']
        file_path = os.path.join(metadata['path'], metadata['name'] + '.ipynb')

        # Set default metadata
        hugo['date'] = hugo.get('date') or os.path.getmtime(file_path) # TODO: Format
        hugo['title'] = (hugo.get('title') or
            ' '.join(_.capitalize() for _ in metadata['name'].split('_'))
        hugo['draft'] = hugo.get('draft') or True

        for index, cell in enumerate(nb.cells):
            nb.cells[index], resources = self.preprocess_cell(cell, resources, index)
        return nb, resources


class HugoExporter(MarkdownExporter):
    @property
    def template_path(self):
        return super().template_path + [os.path.dirname(__file__)]

    @default('template_file')
    def _template_file_default(self):
        return 'hugo_markdown.tpl'

    @property
    def preprocessors(self):
        return [UnderscorePreprocessor]
