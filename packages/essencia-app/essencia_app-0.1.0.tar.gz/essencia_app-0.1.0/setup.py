# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['essencia_app',
 'essencia_app.endpoints',
 'essencia_app.endpoints.handlers',
 'essencia_app.utils']

package_data = \
{'': ['*'], 'essencia_app': ['static/css/*', 'templates/*']}

install_requires = \
['deta>=0.8,<0.9', 'starlette>=0.14.2,<0.15.0']

setup_kwargs = {
    'name': 'essencia-app',
    'version': '0.1.0',
    'description': 'MIT',
    'long_description': None,
    'author': 'arantesdv',
    'author_email': 'arantesdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
