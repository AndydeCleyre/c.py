c.py
====

c.py is (not yet) a drop in replacement for cat. c.py is written in a few lines
of Python code and provides additional features, for instance automatic syntax
highlighting with pygments and paging support. See the manpage [c(1)][1] for more
information.

Install
-------

pip can be used to install c.py from pypi:

    $ [sudo] pip install [--user] c.py

Use either `sudo` to install c.py system wide or `--user` to install it in
`$HOME/.local`.

On Arch Linux there is an [AUR package][2] available. c.py can be installed
using your favorite AUR helper, such as [pacaur][3].

    $ pacaur -S cpy

If you like installing the script the hard, manual and *unsupported* way you can
just drop the `c.py` file somewhere into your `$PATH` and rename it to `c`. Make
sure that the following python libraries are importable: [docopt][4], [click][5],
[pygments][6].

[1]: https://docs.sevenbyte.org/c.py/c.1.html
[2]: https://aur.archlinux.org/packages/cpy
[3]: https://github.com/rmarquis/pacaur
[4]: https://github.com/docopt/docopt
[5]: https://github.com/mitsuhiko/click
[6]: https://bitbucket.org/birkenfeld/pygments-main
