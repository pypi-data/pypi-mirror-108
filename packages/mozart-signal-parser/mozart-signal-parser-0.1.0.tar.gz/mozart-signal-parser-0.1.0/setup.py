# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mozart_signal_parser']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=4.5.2,<5.0.0', 'pytesseract>=0.3.7,<0.4.0']

setup_kwargs = {
    'name': 'mozart-signal-parser',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sergey Anufrienko',
    'author_email': 'serg@anufrienko.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
