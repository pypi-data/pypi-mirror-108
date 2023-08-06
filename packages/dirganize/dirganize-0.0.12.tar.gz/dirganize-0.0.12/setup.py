# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dirganize']

package_data = \
{'': ['*']}

install_requires = \
['rich>=10.2.2,<11.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['dirganize = dirganize.cli:app']}

setup_kwargs = {
    'name': 'dirganize',
    'version': '0.0.12',
    'description': 'Declutter you folders and get peace of mind. A command-line tool to organize files into category directories.',
    'long_description': '# dirganize\n\nDeclutter you folders and get peace of mind.\nA command-line tool to organize files into category directories.\n\n## Installation\n\n```shell\npip install dirganize\n```\n\n## Usage\n\nMove into your desired directory and run `dirganize`.\n\nIt will put all files into their respective category folders, based on the\ndefault configuration.\n\nYou can put a `.dirganize.yml` file ( inside the folder you want to dirganize )\nto override the default configuration.\n\nBasically you have the folder name, followed by file types to put in that folder.\n\nYou can also specify which folder to organize:\n\n```shell\ndirganize --path ~/Downloads\n```\n',
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aahnik/dirganize',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
