# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yen_parser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'yen-parser',
    'version': '0.1.0',
    'description': 'Yen currency string parser.',
    'long_description': '\n\nYen currency string parser.\n\n============\nInstallation\n============\n\n::\n\n    pip install yen-parser\n\n=====\nUsage\n=====\n\n-----------\nBasic usage\n-----------\n\n::\n\n    >>> from yen_parser import parse_yen\n    >>> parse_yen("¥45,000")\n    45000\n\n---------------\nSupported cases\n---------------\n\nparse-yen function accepts string in the very rough format::\n\n    >>> parse_yen("45000")\n    45000\n\n    >>> parse_yen("45,000")\n    45000\n\n    >>> parse_yen("¥45,000")\n    45000\n\n====\nNote\n====\n\nAs the name of this library `yen-parsr` describes, only support Japanese yen currency format.\nIf you want to deal with other currency, there are more nicely library exists on PyPI, e.g.\nprice-parser\n\n========\nDisclaim\n========\n\nThis library is not intended to be used for important and/or critical work like financial situation.\n',
    'author': 'kenjimaru',
    'author_email': 'kendimaru2@gmail.com',
    'maintainer': 'kenjimaru',
    'maintainer_email': 'kendimaru2@gmail.com',
    'url': 'https://github.com/kendimaru/yen-parser',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
