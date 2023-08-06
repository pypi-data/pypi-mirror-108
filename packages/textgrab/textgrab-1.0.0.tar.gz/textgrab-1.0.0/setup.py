# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textgrab']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0',
 'PySide6',
 'appdirs>=1.4.4,<2.0.0',
 'docopt-ng>=0.7.2,<0.8.0',
 'pytesseract>=0.3.7,<0.4.0']

entry_points = \
{'console_scripts': ['textgrab = textgrab.run:main']}

setup_kwargs = {
    'name': 'textgrab',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'PowerSnail',
    'author_email': 'hj@powersnail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
