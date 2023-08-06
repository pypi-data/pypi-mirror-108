"""
Adapted from PyLatex (c) 2014 by Jelte Fennema, MIT-License
https://github.com/JelteF/PyLaTeX/blob/v1.3.2/pylatex/utils.py#L68-L100
"""

_latex_special_chars = {
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\^{}',
    '\\': r'\textbackslash{}',
    '\n': '\\newline%\n',
    '-': r'{-}',
    '\xA0': '~',  # Non-breaking space
    '[': r'{[}',
    ']': r'{]}',
}

def escape_latex(s: str) -> str:
    """
    Escapes a string to be valid latex. Possibly necessary for using the quick-setup which
    applies latex to the column names.
    :param s: The string with potentially bad symbols
    :return: A string that can be compiled by latex
    """
    return ''.join(_latex_special_chars.get(c, c) for c in str(s))
