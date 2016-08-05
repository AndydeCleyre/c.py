#!/usr/bin/env python3

import argparse
import os
import sys
import signal
from pygments import highlight
from pygments.util import ClassNotFound, OptionError
from pygments.lexers import TextLexer
from pygments.lexers import guess_lexer
from pygments.lexers import guess_lexer_for_filename
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalTrueColorFormatter


C_PYGMENTS_THEME_DEFAULT = 'fruity'
C_PYGMENTS_THEME = os.getenv('C_PYGMENTS_THEME', 'fruity')
C_DEBUG = True if 'C_DEBUG' in os.environ else False
__version__ = '0.5.2'


def debug(msg):
    """
    When the environment variable 'C_DEBUG' is set to a non empty
    value, print the supplied message and prefix it with '[Debug] '.
    """
    if C_DEBUG:
        print('[Debug] {}'.format(msg))


def read_file(filename):
    """
    Return the content of 'filename'.

    If any error occurs this method prints an appropriate error
    message and causes 'c.py' to exit with return code 1.
    """
    try:
        debug("Reading file: '{}'".format(filename))
        with open(filename, 'rb') as f:
            return f.read()
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)


def read_stdin():
    """
    Read the content from sys.stdin.

    If any error occurs this method prints an appropriate error
    message and causes 'c.py' to exit with return code 1.
    """
    try:
        debug('Reading stdin')
        return sys.stdin.read()
    except Exception as e:
        print(e, file=sys.stderr)
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
    filename = filename if filename else '-'
    if lexer == 'auto':
        debug("Trying to guess lexer for filename: '{}'".format(filename))
        try:
            lexer_cls = guess_lexer_for_filename(filename, data)
        except ClassNotFound:
            if data[0:2] == b'#!':
                debug("Shebang '{}' present".format(data.splitlines()[0]))
                lexer_cls = guess_lexer(data.decode())
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
            print("[Error] No lexer found: '{}'".format(lexer), file=sys.stderr)
            exit(1)

    debug('Using lexer: {}'.format(lexer_cls))
    return lexer_cls


def get_formatter(theme):
    """
    Return a TerminalFormatter class with the
    supplied theme enabled.

    This method wraps the instantiation of Terminal256Formatter.
    If the supplied theme is invalid c.py fails.

    Args:
        theme     The name of the theme as a string.
                  'light' or 'dark' is supported.
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
        return TerminalTrueColorFormatter(style=used_theme)
    except OptionError:
        print("[Error] Invalid theme: '{}'".format(used_theme), file=sys.stderr)
        exit(1)


def process_data(data, filename, args):
    """
    Process, i.e. hightlight the provided data.

    Args:
        data        The data to be highlighed.
        filename    The filename; used for guessing
                    the correct language
        args        The args namespace object, which
                    includes the command line options
    """
    if args.skip_pygments:
        # Skip the whole pygments magic.
        debug('Skipping pygments')
        print(data.decode())
    else:
        # The formatter needs to be reinitialized. Otherwise
        # the line numbers are continued over several files.
        debug('Initializing pygments')
        formatter = get_formatter(args.theme)
        lexer = get_lexer(filename, data, args.lexer)
        if args.show_lexer:
            print('{}: {}'.format(filename, lexer))
        else:
            highlight(data, lexer, formatter, outfile=sys.stdout)


def sigpipe_handler(signo, frame):
    """
    Signal handler for SIGPIPE. Needed to perform a clean exit
    when the connected pager is closed by the user.
    """
    exit(0)


def main():
    # Ignore broken pipe errors when writing to a pager.
    if not sys.stdout.isatty():
        signal.signal(signal.SIGPIPE, sigpipe_handler)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file',
        nargs='*',
        help='file(list) to read; "-" means stdin',
    )
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument(
        '-f',
        '--filename',
        help='filename to be passed to pygments when reading from stdin',
    )
    parser.add_argument(
        '-l',
        '--lexer',
        default='auto',
        help='force a particular lexer',
    )
    parser.add_argument(
        '-t',
        '--theme',
        default='fruity',
        help='specify pygments theme',
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='show debug output',
    )
    parser.add_argument(
        '--skip-pygments',
        action='store_true',
        help='skip pygments; do not perform any synthax highlighting',
    )
    parser.add_argument(
        '--show-lexer',
        action='store_true',
        help='show determined lexer',
    )
    parser.add_argument(
        '--show-themes',
        action='store_true',
        help='show all available themes',
    )
    args = parser.parse_args()

    if args.debug:
        global C_DEBUG
        C_DEBUG = True
        debug(args)

    try:
        if args.show_themes:
            from pygments.styles import get_all_styles
            from pprint import pprint
            pprint(list(get_all_styles()))
            exit(0)

        # Handle no arguments
        if not args.file:
            data = read_stdin()
            process_data(data, args.filename, args)

        for filename in args.file:
            if filename == '-':
                data = read_stdin()
            else:
                data = read_file(filename)
            process_data(data, filename, args)

    except KeyboardInterrupt:
        exit(1)


if __name__ == '__main__':
    main()
