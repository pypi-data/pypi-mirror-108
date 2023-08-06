# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seesv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'seesv',
    'version': '0.1.0',
    'description': 'A Python library providing fast access to data in very large delimited data files (CSV, TSV, pipe-delimited, etc).',
    'long_description': None,
    'author': 'David Alexis',
    'author_email': 'dalexis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
