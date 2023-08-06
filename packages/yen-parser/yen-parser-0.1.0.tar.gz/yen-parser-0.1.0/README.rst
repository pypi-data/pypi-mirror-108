

Yen currency string parser.

============
Installation
============

::

    pip install yen-parser

=====
Usage
=====

-----------
Basic usage
-----------

::

    >>> from yen_parser import parse_yen
    >>> parse_yen("¥45,000")
    45000

---------------
Supported cases
---------------

parse-yen function accepts string in the very rough format::

    >>> parse_yen("45000")
    45000

    >>> parse_yen("45,000")
    45000

    >>> parse_yen("¥45,000")
    45000

====
Note
====

As the name of this library `yen-parsr` describes, only support Japanese yen currency format.
If you want to deal with other currency, there are more nicely library exists on PyPI, e.g.
price-parser

========
Disclaim
========

This library is not intended to be used for important and/or critical work like financial situation.
