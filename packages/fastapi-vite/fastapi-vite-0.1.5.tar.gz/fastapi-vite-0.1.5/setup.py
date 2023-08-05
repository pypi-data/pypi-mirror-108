# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_vite']

package_data = \
{'': ['*']}

install_requires = \
['fastapi[all]>=0.65.1,<0.66.0']

setup_kwargs = {
    'name': 'fastapi-vite',
    'version': '0.1.5',
    'description': 'Helper Utilities for loading assets genated from Vite manifests',
    'long_description': '',
    'author': 'Cody Fincher',
    'author_email': 'cody.fincher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cofin/fastapi-vite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
