# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twiscrap', 'twiscrap.spiders']

package_data = \
{'': ['*']}

install_requires = \
['Scrapy>=2.5.0,<3.0.0', 'scrapy-selenium>=0.0.7,<0.0.8']

setup_kwargs = {
    'name': 'twiscrap',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
