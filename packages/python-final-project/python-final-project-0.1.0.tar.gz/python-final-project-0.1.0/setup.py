# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_final_project']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0', 'fire>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['main = python_final_project.cli:main']}

setup_kwargs = {
    'name': 'python-final-project',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Will Lane',
    'author_email': 'williamlane923@gmail.com',
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
