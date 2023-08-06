# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hajkr_facebook_scraper']

package_data = \
{'': ['*']}

install_requires = \
['facebook-scraper>=0.2.41,<0.3.0']

setup_kwargs = {
    'name': 'hajkr-facebook-scraper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tadej Hribar',
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
