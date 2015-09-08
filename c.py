"""
Usage: c [--number] [--show-lexer] [--no-pager] [--no-pygments] [--lexer LEXER]
         [--theme THEME] [--] [<file>...]

Options:
  -n, --number              Number all output lines
  --show-lexer              Show determined lexer and exit
  --no-pager                Disable paging
  --no-pygments             Skip pygments, behave like cat
  -l LEXER, --lexer LEXER   Specify a particular lexer        [default: auto]
  -t THEME, --theme THEME   Choose a theme: 'light' or 'dark' [default: dark]
"""


import os
import sys
from click import echo, echo_via_pager
from docopt import docopt
from pygments import highlight
from pygments.util import ClassNotFound, OptionError
from pygments.lexers import TextLexer
from pygments.lexers import guess_lexer
from pygments.lexers import guess_lexer_for_filename
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter


PAGER = os.getenv('PAGER', 'cat')
# This behaviour is similar to git:
# https://github.com/git/git/blob/master/Documentation/config.txt#L646
if 'LESS' not in os.environ:
    os.environ['LESS'] = 'FRX'
C_PYGMENTS_THEME_DEFAULT = 'dark'
C_PYGMENTS_THEME = os.getenv('C_PYGMENTS_THEME', 'dark')
C_NO_PAGER = True if 'C_NO_PAGER' in os.environ else False
C_DEBUG = True if 'C_DEBUG' in os.environ else False
__version__ = '0.2.0'


def debug(msg):
    """
    When the environment variable 'C_DEBUG' is set to a non empty
    value, print the supplied message and prefix it with '[Debug] '.
    """
    if C_DEBUG:
        echo('[Debug] {}'.format(msg))


def read_file(filename):
    """
    Return the content of 'filename'.

    If any error occurs this method prints an appropriate error
    message and causes 'c.py' to exit with return code 1.
    """
    try:
        if filename == '-':
            debug('Reading stdin')
            return sys.stdin.read()
        else:
            debug("Reading file: '{}'".format(filename))
            with open(filename) as f:
                return f.read()
    except Exception as e:
        echo(e, err=True)
        exit(1)


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
        debug("Trying to guess lexer for filename: '{}'".format(filename))
        try:
            lexer_cls = guess_lexer_for_filename(filename, data)
        except ClassNotFound:
            if data[0:2] == '#!':
                debug("Shebang '{}' present".format(data[0:2]))
                lexer_cls = guess_lexer(data)
            elif filename == '-':
                try:
                    debug("Have read from 'stdin'; guessing lexer for content")
                    lexer_cls = guess_lexer(data)
                except ClassNotFound:
                    debug('Guessing failed, using fallback lexer')
                    lexer_cls = TextLexer()
            else:
                debug('No shebang present, using fallback lexer')
                lexer_cls = TextLexer()
        except TypeError:
            debug('Guessing failed, using fallback lexer')
            lexer_cls = TextLexer()
    else:
        try:
            debug("Trying to find lexer: '{}'".format(lexer))
            lexer_cls = get_lexer_by_name(lexer)
        except ClassNotFound:
            echo("[Error] No lexer found: '{}'".format(lexer), err=True)
            exit(1)

    debug('Using lexer: {}'.format(lexer_cls))
    return lexer_cls


def get_formatter(theme, linenos=False):
    """
    Return a TerminalFormatter class with the
    supplied theme enabled.

    This method wraps the instantiation of Terminal256Formatter.
    If the supplied theme is invalid c.py fails.

    Arg:
        theme     The name of the theme as a string.
                  'light' or 'dark' is supported.
        linenos   Prefix every line with its line number.
                  Has to be True or False.
    """
    debug('Choosing theme')
    # Check whether C_PYGMENTS_THEME is set and whether
    # it is NOT equal to the default theme. In that case
    # it can be overwritten by the command line switch
    # "--theme THEME".
    if C_PYGMENTS_THEME != C_PYGMENTS_THEME_DEFAULT:
        if theme != C_PYGMENTS_THEME_DEFAULT:
            used_theme = theme
        else:
            used_theme = C_PYGMENTS_THEME
    else:
        used_theme = theme

    debug("Using theme '{}'".format(used_theme))

    try:
        return TerminalFormatter(bg=used_theme, linenos=linenos)
    except OptionError:
        echo("[Error] Invalid theme: '{}'".format(used_theme), err=True)
        exit(1)


def cli(args):
    filenames = args['<file>'] if args['<file>'] else '-'
    lexer = None
    out = ''

    for filename in filenames:
        data = read_file(filename)
        if args['--no-pygments']:
            # Skip the whole pygments magic.
            debug('Skipping pygments')
            out += data
        else:
            # The formatter needs to be reinitialized. Otherwise
            # the line numbers are continued over several files.
            debug('Initializing pygments')
            formatter = get_formatter(args['--theme'], args['--number'])
            lexer = get_lexer(filename, data, args['--lexer'])
            out += highlight(data, lexer, formatter)

    if args['--show-lexer']:
        if lexer:
            echo(lexer)
        else:
            echo('pygments skipped')
        exit(0)
    if args['--no-pager'] or C_NO_PAGER or PAGER == 'cat':
        echo(out, color=True)
    else:
        echo_via_pager(out, color=True)


def main():
    """Main entry point; needed for setuptools"""
    cli(docopt(__doc__, version=__version__))


if __name__ == '__main__':
    main()
