# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phygitalism_config']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'phygitalism-config',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Phygitalism',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
