"""Usage: view <file>"""

import os
import sys
import shutil
from click import echo_via_pager
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import TextLexer
from pygments.lexers import guess_lexer
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import Terminal256Formatter


def main():
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print(__doc__)
        exit(0)

    if 'LESS' not in os.environ:
        os.environ['LESS'] = 'FRX'

    filename = sys.argv[1]
    with open(filename) as f:
        data = f.read()

    formatter = Terminal256Formatter(style='friendly')

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

    # Highlight! :-)
    out = highlight(data, lexer, formatter)
    echo_via_pager(out)

