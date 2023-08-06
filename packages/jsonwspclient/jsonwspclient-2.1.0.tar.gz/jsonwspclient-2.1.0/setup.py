# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonwspclient']

package_data = \
{'': ['*']}

install_requires = \
['requests']

setup_kwargs = {
    'name': 'jsonwspclient',
    'version': '2.1.0',
    'description': 'Flexible JSON-WSP client.',
    'long_description': None,
    'author': 'ellethee',
    'author_email': 'luca800@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/ellethee/jsonwspclient',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
