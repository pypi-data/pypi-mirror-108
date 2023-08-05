# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stonehenge',
 'stonehenge.admin',
 'stonehenge.auth',
 'stonehenge.cms',
 'stonehenge.components',
 'stonehenge.components.html',
 'stonehenge.components.ui',
 'stonehenge.db',
 'stonehenge.db.migrations',
 'stonehenge.handlers',
 'stonehenge.middlewares',
 'stonehenge.migrations',
 'stonehenge.modules',
 'stonehenge.requests',
 'stonehenge.responses',
 'stonehenge.routers',
 'stonehenge.server']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'uvicorn>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'stonehenge',
    'version': '0.1.0',
    'description': 'A fast, flexible, and fully-featured web framework',
    'long_description': None,
    'author': 'Robert Townley',
    'author_email': 'me@roberttownley.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
