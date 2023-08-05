# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_gitignore']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['py-gitignore = py_gitignore.py_gitignore:main']}

setup_kwargs = {
    'name': 'py-gitignore',
    'version': '0.1.1',
    'description': 'cli to add gitignore file',
    'long_description': None,
    'author': 'bdista',
    'author_email': 'bdista@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
