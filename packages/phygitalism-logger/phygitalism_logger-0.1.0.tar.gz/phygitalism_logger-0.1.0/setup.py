# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phygitalism_logger']

package_data = \
{'': ['*']}

install_requires = \
['phygitalism-config>=0.1.8,<0.2.0', 'pygelf>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'phygitalism-logger',
    'version': '0.1.0',
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
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
