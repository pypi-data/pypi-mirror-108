# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['termitext']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'termitext',
    'version': '0.1.3',
    'description': 'Color and format text in the console',
    'long_description': None,
    'author': 'Yek',
    'author_email': 'gwojtysiak34@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
