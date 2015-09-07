"""
Usage: c [--no-pager] [--number] [--lexer LEXER] [--theme THEME] <file>

Options:
  --no-pager                Disable paging
  -n, --number              Number all output lines
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
LESS = os.getenv('LESS', 'FRX')
C_PYGMENTS_THEME_DEFAULT = 'dark'
C_NO_PAGER = True if 'C_NO_PAGER' in os.environ else False
C_DEBUG = True if 'C_DEBUG' in os.environ else False
__version__ = '0.1.0'


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
        debug('Guessing lexer')
        try:
            lexer_cls = guess_lexer_for_filename(filename, data)
        except ClassNotFound:
            debug('Guessing failed, looking for a shebang line')
            if data[0:2] == '#!':
                debug("Shebang '{}' present".format(data[0:2]))
                lexer_cls = guess_lexer(data)
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
        theme   The name of the theme as a string. Check out
                http://pygments.org to get a list of supported
                themes.
    """
    debug('Choosing theme')
    theme_from_env = os.getenv('C_PYGMENTS_THEME')
    # Check whether C_PYGMENTS_THEME is set and whether
    # it is NOT equal to the default theme. In that case
    # it can be overwritten by the command line switch
    # "--theme THEME".
    if theme_from_env and theme_from_env != C_PYGMENTS_THEME_DEFAULT:
        if theme != C_PYGMENTS_THEME_DEFAULT:
            used_theme = theme
        else:
            used_theme = theme_from_env
    else:
        used_theme = theme

    debug("Using theme '{}'".format(used_theme))

    try:
        return TerminalFormatter(bg=used_theme, linenos=linenos)
    except OptionError:
        echo("[Error] Invalid theme: '{}'".format(used_theme), err=True)
        exit(1)


def cli(args):
    filename = args['<file>']
    data = read_file(filename)
    formatter = get_formatter(args['--theme'], args['--number'])
    lexer = get_lexer(filename, data, args['--lexer'])
    out = highlight(data, lexer, formatter)

    if args['--no-pager'] or C_NO_PAGER or PAGER == 'cat':
        echo(out)
    else:
        echo_via_pager(out)


def main():
    """Main entry point; needed for setuptools"""
    cli(docopt(__doc__, version=__version__))


if __name__ == '__main__':
    main()
