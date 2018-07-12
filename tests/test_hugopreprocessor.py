"""Tests for nbhugoexporter.hugoppreprocessory."""
import pytest

from nbhugoexporter.hugopreprocessor import HugoPreprocessor


@pytest.fixture
def hp():
    """Shorthand fixture."""
    return HugoPreprocessor()


def test_quote_underscores_in_latex(hp):
    """Underscores properly quoted in substrings."""
    latex = '$x_1 + x_2$'
    quoted_latex = r'$x\_1 + x\_2$'
    text = f'_This_ is latex: {latex}.'
    expected = rf'_This_ is latex: {quoted_latex}.'
    actual = hp._quote_underscores_in_latex(text, latex)
    assert actual == expected

    text2 = f'More latex: {latex} {latex}.'
    expected2 = f'More latex: {quoted_latex} {quoted_latex}.'
    partial2 = hp._quote_underscores_in_latex(text2, latex)
    actual2 = hp._quote_underscores_in_latex(partial2, latex)
    assert actual2 == expected2


def test_extract_latex(hp):
    """Extract display and inline latex."""
    markdown = r"""
    This is a line with no latex: $1.00.

    This is another line with no latex: $2.00.

    This is a third line with no latex: \$1.00 -- \$2.00.

    This is a line with inline latex: $e^{i \pi} + 1 = 0$.

    This is some display latex:
    $$
    1
    2
    3
    $$
    """
    expected = ['$$\n    1\n    2\n    3\n    $$', r'$e^{i \pi} + 1 = 0$']
    actual = hp._extract_latex(markdown)
    assert actual == expected


def test_insert_newline_before_lists(hp):
    """Test inserting newlines."""
    text = r"""
This is not a list item
* This is a list item
* So is this
This is not anymore
* And this is a new list

On the other hand:

* This list item is fine.
* And so is this one.
"""
    expected = r"""
This is not a list item

* This is a list item
* So is this
This is not anymore

* And this is a new list

On the other hand:

* This list item is fine.
* And so is this one.
"""
    actual = hp._insert_newline_before_lists(text)
    assert actual == expected
