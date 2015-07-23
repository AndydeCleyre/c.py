"""
Usage: c [--no-pager] [--lexer LEXER] [--theme THEME] <file>

Options:
  --no-pager                Disable paging
  -l LEXER, --lexer LEXER   Specify a particular lexer [default: auto]
  -t THEME, --theme THEME   Specify a particular theme [default: friendly]
"""


import os
from click import echo_via_pager
from docopt import docopt
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import TextLexer
from pygments.lexers import guess_lexer
from pygments.lexers import guess_lexer_for_filename
from pygments.lexers import get_lexer_by_name
from pygments.formatters import Terminal256Formatter


def get_lexer(filename, data, lexer='auto'):
    """
    Return a particular lexer instance.

    This method wraps pygments' methods guess_lexer_for_filename()
    and guess_lexer(). First guess_lexer_for_filename() is invoked;
    if there is no result the presence of a shebang is checked.
    If the subsequent call to guess_lexer() does not bring any
    results the fallback value TextLexer() is returned.

    Args:
        filename    The name of the file to be displayed
        data        The content of the file (utf-8 encoded)
        lexer       Specifying another value than 'auto' skips any
                    guess_lexer() calls. The pygments method
                    get_lexer_by_name() is used to find a particular
                    lexer class. If nothing has been found, c.py
                    fails.
    """
    if lexer == 'auto':
        try:
            lexer_cls = guess_lexer_for_filename(filename, data)
        except ClassNotFound:
            # Check if there is any shebang.
            if data[0:2] == '#!':
                lexer_cls = guess_lexer(data)
            else:
                lexer_cls = TextLexer()
        except TypeError:
            lexer_cls = TextLexer()
    else:
        try:
            lexer_cls = get_lexer_by_name(lexer)
        except ClassNotFound:
            print('Error: Invalid lexer!')
            exit(1)

    return lexer_cls


def get_formatter(theme):
    """
    Returns a Terminal256Formatter class with the
    supplied theme enabled.

    This method wraps the instantiation of Terminal256Formatter.
    If the supplied theme is invalid c.py fails.

    Arg:
        theme   The name of the theme as a string. Check out
                http://pygments.org to get a list of supported
                themes.
    """
    try:
        return Terminal256Formatter(style=theme)
    except ClassNotFound:
        print('Error: Invalid theme!')
        exit(1)


def cli(args):
    filename = args['<file>']
    with open(filename) as f:
        data = f.read()

    formatter = get_formatter(args['--theme'])
    lexer = get_lexer(filename, data, args['--lexer'])

    # Highlight! :-)
    out = highlight(data, lexer, formatter)

    if args['--no-pager']:
        print(out)
    else:
        # This behaviour is similar to that what git does:
        # https://github.com/git/git/blob/master/Documentation/config.txt#L646
        if 'LESS' not in os.environ:
            os.environ['LESS'] = 'FRX'
        echo_via_pager(out)


def main():
    """Main entry point; needed for setuptools"""
    cli(docopt(__doc__))
