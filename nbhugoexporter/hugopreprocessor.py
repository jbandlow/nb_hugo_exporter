r"""Preprocessor Module for Hugo.

This module exports a single class.

    HugoPreprocessor: An `nbconvert` `Preprocessor` for exporting notebooks
        to a Markdown format compatible with [Hugo](https://gohugo.io)

"""
import datetime
import os.path
import re

from nbconvert.preprocessors import Preprocessor


class HugoPreprocessor(Preprocessor):
    r"""Preprocessor class for Hugo.

    This class overrides the `preprocess` and `preprocess_cell` methods of
    the `nbcovert` `Preprocessor` class, to accomplish the following tasks:

    1.  Properly quote underscores in math mode. See
        https://gohugo.io/content-management/formats/#issues-with-markdown for
        more context on the problem. This resolves the issue with the
        "tedious" solution of quoting all underscores.

    2.  Set default values for metadata (date, title, and draft).
    """

    def _quote_underscores_in_latex(self, text, latex):
        r"""
        Return a modified `text`, where all '_' in `latex` have been quoted.

        Args:
            text: A string which contains `latex` as a substring
            latex: A substring of `text` consisting of actual Latex

        Returns: A copy of `text`, where every underscore inside `latex` is
                 replaced by '\_'.

        """
        quoted_latex = latex.replace(r'_', r'\_')
        return text.replace(latex, quoted_latex)

    def _extract_latex(self, markdown):
        r"""
        Return a list of the blocks of latex occurring in `markdown`.

        Args:
            markdown: A string

        Returns: A list of the strings of latex occurring in `markdown`,
                 including delimiters.

        """
        # '$$ but not \$$' 'anything not ending in \'  '$$'.
        display_math = re.compile(r'[^\\](\$\$.*?[^\\]\$\$)', re.DOTALL)
        out = re.findall(display_math, markdown)

        # '$ but not \$ or $$'  'anything not ending in \'  '$'.
        inline_math = re.compile(r'[^\$\\](\$.*?[^\\]\$)', re.DOTALL)
        # Inline math cannot span two newlines.
        for block in markdown.split('\n\n'):
            out += re.findall(inline_math, block)

        return out

    def _time_format_hugo(self, ts):
        r"""Return a string in the ISO-8601 flavor that Hugo uses."""
        local_tz = datetime.datetime.now(
            datetime.timezone.utc).astimezone().tzinfo
        out = ts.astimezone(local_tz).strftime('%Y-%m-%dT%H:%M:%S%z')
        # %z is [+-]HHMM, but we want [+-]HH:MM
        return out[:-2] + ':' + out[-2:]

    def preprocess_cell(self, cell, resources, cell_index):
        r"""
        Quote the underscores in Latex appearing in the cell.

        Args: See the `nbconvert.preprocessors.Preprocessor` documentation.

        Returns: The tuple `(cell, resources)`, where `cell` has been modified
                 so that every '_' in Latex that is part of a markdown cell or
                 output of type 'text/latex' is preceded by '\'.

        """
        if cell.cell_type == 'markdown':
            latex_segments = self._extract_latex(cell.source)
            for latex in latex_segments:
                cell.source = self._quote_underscores_in_latex(
                    cell.source, latex)

        elif cell.cell_type == 'code':
            for o in cell.outputs or []:
                latex = o.get('data', {}).get('text/latex')
                if latex:
                    o['data']['text/latex'] = self._quote_underscores_in_latex(
                        latex, latex)
        return cell, resources

    def preprocess(self, nb, resources):
        r"""
        Set metadata defaults, process underscores, and set output file paths.

        Args: See the `nbconvert.preprocessors.Preprocessor` documentation.

        Returns: (nb, resources) where these have been fully processed.

        """
        metadata = resources['metadata']
        if metadata.get('hugo') is None:
            metadata['hugo'] = {}
        hugo = metadata['hugo']

        # Set default metadata
        file_path = os.path.join(metadata['path'], metadata['name'] + '.ipynb')
        ts = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        hugo['date'] = hugo.get('date') or self._time_format_hugo(ts)

        title = ' '.join(_.capitalize() for _ in metadata['name'].split('_'))
        hugo['title'] = hugo.get('title') or title

        hugo['draft'] = hugo.get('draft') or True

        # Process the cells
        for index, cell in enumerate(nb.cells):
            nb.cells[index], resources = self.preprocess_cell(
                cell, resources, index)

        return nb, resources
