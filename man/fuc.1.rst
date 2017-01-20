fuc
===

----------------------------------------------------------------
[fu]zzy [c]at; a shell wrapper for c(1) enabling fuzzy searching
----------------------------------------------------------------

:Manual section: 1

Synopsis
--------

fuc [-Vh] [additional_flags]

Description
-----------

fuc(1) is yet another small shell wrapper over c.py(1) which enables fuzzy
file searching using fzf(1). fuc(1) issues fzf(1) which reads the current
working directory into its buffer. The file to display can be fuzzy searched
using fzf's interactive interface. The chosen file is then opened via c(1).

Options
-------

All given options are forwarded to c(1) and c.py(1) respectively. There are
two exceptions:

\-V
    Show fc's version string and exit.

\-h
    Show helppage and exit.

.. include:: footer.rst

See also
--------

c(1), c.py(1), fzf(1)
