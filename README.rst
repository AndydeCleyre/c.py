c.py
====

``c.py`` is replacement for ``cat``. ``c.py`` is written in a few lines of
Python code and provides automatic syntax highlighting with pygments. Paging
support is provided by a shell wrapper called ``c``. See the manpages |c(1)|_
and |c.py(1)|_ for more information. A short introduction can be read here_.

Install
-------

On Arch Linux there is an `AUR package`_ available. ``c.py`` can be installed
using your favorite AUR helper, such as pacaur_.

.. code-block:: bash

    $ pacaur -S cpy


If you like installing the script the hard, manual and **unsupported** way you
can just drop the ``c.py`` and ``c`` files somewhere into your ``$PATH``.
Make sure that the pygments_ library is installed for python3.

.. |c(1)| replace:: ``c(1)``
.. |c.py(1)| replace:: ``c.py(1)``

.. _c(1): https://docs.sevenbyte.org/c.py/c.1.html
.. _c.py(1): https://docs.sevenbyte.org/c.py/c.py.1.html
.. _here: https://blog.sevenbyte.org/2016/05/15/cat-with-syntax-highlighting.html
.. _AUR package: https://aur.archlinux.org/packages/cpy
.. _pacaur: https://github.com/rmarquis/pacaur
.. _pygments: https://bitbucket.org/birkenfeld/pygments-main
