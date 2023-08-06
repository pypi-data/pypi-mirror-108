# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdcast']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16.5', 'pandas>=0.24']

setup_kwargs = {
    'name': 'pandas-downcast',
    'version': '0.1.0.dev1',
    'description': 'Automated downcasting for Pandas DataFrames.',
    'long_description': None,
    'author': 'Dominic Thorn',
    'author_email': 'dominic.thorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
