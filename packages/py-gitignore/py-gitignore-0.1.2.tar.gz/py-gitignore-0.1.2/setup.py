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
    'version': '0.1.2',
    'description': 'cli to add gitignore file',
    'long_description': 'py-gitignore\n=============\n\nAdd python gitignore file to current directory.\n\nUsage\n-----\n\n.. code-block:: text\n\n    $ py-gitignore\n\nThis will create in the current directory a ``.gitignore`` file with the content defined in `template.py <py_gitignore/template.py>`_\n\nTODO\n----\n\n- option if ``.gitignore`` file already exists\n- option to provide alternative path\n',
    'author': 'bdista',
    'author_email': 'bdista@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bdista/py-gitignore',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
