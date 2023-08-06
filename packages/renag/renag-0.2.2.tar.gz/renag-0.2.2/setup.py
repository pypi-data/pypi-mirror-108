# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['renag', 'renag.tests']

package_data = \
{'': ['*']}

install_requires = \
['iregex>=0.1.16,<0.2.0']

entry_points = \
{'console_scripts': ['renag = renag.__main__:main']}

setup_kwargs = {
    'name': 'renag',
    'version': '0.2.2',
    'description': 'A Regex based linter tool that works for any language and works exclusively with custom linting rules.',
    'long_description': None,
    'author': 'Ryan',
    'author_email': 'ryanpeach@icloud.com',
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
