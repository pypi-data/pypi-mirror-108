# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chanim']

package_data = \
{'': ['*']}

install_requires = \
['manim>=0.7.0']

entry_points = \
{'manim.plugins': ['chanim = chanim']}

setup_kwargs = {
    'name': 'chanim',
    'version': '1.0.0',
    'description': 'Manim extension for making chemistry videos',
    'long_description': None,
    'author': 'kilacoda',
    'author_email': 'kilacoda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
