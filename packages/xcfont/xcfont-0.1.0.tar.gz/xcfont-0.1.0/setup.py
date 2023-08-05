# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xcfont']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'fonttools>=4.24.4,<5.0.0', 'funcy>=1.16,<2.0']

setup_kwargs = {
    'name': 'xcfont',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'son.le',
    'author_email': 'anhsonleit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
