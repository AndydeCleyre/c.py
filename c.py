"""
Usage: view [--no-pager] [--lexer LEXER] <file>

Options:
  --no-pager                Disable paging
  -l LEXER, --lexer LEXER   Specify a particular lexer [default: auto]
"""


import os
import sys
from click import echo_via_pager
from docopt import docopt
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import TextLexer
from pygments.lexers import guess_lexer
from pygments.lexers import guess_lexer_for_filename
from pygments.lexers import get_lexer_by_name
from pygments.formatters import Terminal256Formatter


def determine_lexer(filename, data):
    try:
        lexer = guess_lexer_for_filename(filename, data)
    except ClassNotFound:
        # Check if there is any shebang.
        if data[0:2] == '#!':
            lexer = guess_lexer(data)
        else:
            lexer = TextLexer()
    except TypeError:
        lexer = TextLexer()

    return lexer


def cli(args):
    filename = args['<file>']
    with open(filename) as f:
        data = f.read()

    formatter = Terminal256Formatter(style='friendly', linenos=True)

    if args['--lexer'] == 'auto':
        lexer = determine_lexer(filename, data)
    else:
        lexer = get_lexer_by_name(args['--lexer'])

    # Highlight! :-)
    out = highlight(data, lexer, formatter)

    if args['--no-pager']:
        print(out)
    else:
        if 'LESS' not in os.environ:
            os.environ['LESS'] = 'FRX'

        echo_via_pager(out)


def main():
    """Main entry point; needed for setuptools"""
    cli(docopt(__doc__))
