# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hackwithharsha']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['hackwithharsha = hackwithharsha.main:hello']}

setup_kwargs = {
    'name': 'hackwithharsha',
    'version': '0.1.0',
    'description': '',
    'long_description': '# HackwithHarsha\n\n- HelloWorld Project for publishing to PyPi using `Poetry` and `Typer`.\n',
    'author': 'HackWithHarsha',
    'author_email': 'hackwithharsha@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
