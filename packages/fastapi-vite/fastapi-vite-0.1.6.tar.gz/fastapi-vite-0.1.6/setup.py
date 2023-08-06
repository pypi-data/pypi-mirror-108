# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_vite']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2', 'fastapi', 'starlette']

setup_kwargs = {
    'name': 'fastapi-vite',
    'version': '0.1.6',
    'description': 'Helper Utilities for loading assets genated from Vite manifests',
    'long_description': '# fastapi-vite\n\nIntegration for FastAPI and Vite JS\n\n## what?\n\nThis package is designed to make working with javascript assets easier.\n\nfastapi-vite enables the jinja filters required to render asset URLs to jinja templates\n\n## installation\n\nInstall using pip\n\n```shell\npip install fastapi-vite\n```\n\n## Usage\n\nConfigure Jinja templating for FastAPI\n\n```python\ntemplates = Jinja2Templates(directory=\'templates\')\ntemplates.env.globals[\'render_vite_hmr_client\'] = fastapi_vite.render_vite_hmr_client\ntemplates.env.globals[\'asset_url\'] = fastapi_vite.asset_url\n\n```\n\n### Configure Vite\n\n### Configure Static Assets\n\n### Configure Templates\n\n\\*render_vite_hmr no-op when in production.\n\n```html\n{{ render_vite_hmr_client() }}\n\n<script\n  type="text/javascript"\n  defer\n  src="{{ asset_url(\'javascript/main.tsx\') }}"\n></script>\n```\n',
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
