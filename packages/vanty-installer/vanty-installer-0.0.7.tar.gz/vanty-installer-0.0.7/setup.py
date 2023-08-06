# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vanty_installer']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'cookiecutter>=1.7.2,<2.0.0']

entry_points = \
{'console_scripts': ['poetry = poetry.console:run'],
 'vanty_installer': ['vanty = .__main__']}

setup_kwargs = {
    'name': 'vanty-installer',
    'version': '0.0.7',
    'description': 'Installer for the Vanty StarterKit.',
    'long_description': '# Vanty Installer\n\n\n<a href="https://docs.advantch.com/vanty-installer" style="margin-right:10px">\n    <img src="https://img.shields.io/badge/vanty docs-docs.advantch.com-brightgreen.svg" alt="Documentation" />\n</a>\n\n<a href="https://docs.advantch.com/vanty-installer">\n    <img src="https://img.shields.io/badge/version-0.0.7-orange.svg" alt="Documentation" />\n</a>\n<br>\n<br>\n\nThis is the installer for the [Vanty StarterKit](https://www.advantch.com/).\n\n\n### 1. Getting started\n\n```\n$ pip install vanty-installer\n```\n\n### 2. Installing the Vanty StarterKit\n\nSee the docs on how to install the [Vanty Starterkit](https://docs.advantch.com)\n\n',
    'author': 'Themba',
    'author_email': 'themba@advantch.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.advantch.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
