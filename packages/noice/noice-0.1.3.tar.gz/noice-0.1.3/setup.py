# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noice']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'click>=8.0.1,<9.0.0',
 'cookiecutter>=1.7.3,<2.0.0',
 'python-fire>=0.1.0,<0.2.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=10.2.2,<11.0.0',
 'sendgrid>=6.7.0,<7.0.0']

setup_kwargs = {
    'name': 'noice',
    'version': '0.1.3',
    'description': 'Data Engineering tools.',
    'long_description': '# Noice\n\nTools for Data people.\n',
    'author': 'Jordan',
    'author_email': 'jordan.wallace.williams@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Mashey/noice',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
