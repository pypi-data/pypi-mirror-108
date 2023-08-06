# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dirganize']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'rich>=10.2.2,<11.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['dirganize = dirganize.cli:app']}

setup_kwargs = {
    'name': 'dirganize',
    'version': '0.1.0',
    'description': 'Declutter you folders and get peace of mind. A command-line tool to organize files into category directories.',
    'long_description': "# dirganize\n\nDeclutter you folders and get peace of mind.\nA command-line tool to organize files into category directories.\n\n[![Tests](https://github.com/aahnik/dirganize/actions/workflows/test.yml/badge.svg)](https://github.com/aahnik/dirganize/actions/workflows/test.yml)\n[![Code Quality](https://github.com/aahnik/dirganize/actions/workflows/quality.yml/badge.svg)](https://github.com/aahnik/dirganize/actions/workflows/quality.yml)\n[![codecov](https://codecov.io/gh/aahnik/dirganize/branch/main/graph/badge.svg?token=2SRYMBMAHH)](https://codecov.io/gh/aahnik/dirganize)\n\n## Installation\n\n```shell\npip install dirganize\n```\n\n## Usage\n\nDirganize has an ultra simple command-line interface.\nJust move into the directory you want to organize, and run `dirganize`.\n\nYou can also specify which folder to organize by using the `path` option.\n\n```shell\ndirganize --path ~/Downloads\n```\n\nIf no path is specified, dirganize works on the current directory.\n\n## Configuration\n\nBy default `dirganize` determines the destination folder for a particular file by\nguessing its type from its extension.\nThe\n[`guess_type`](https://docs.python.org/3/library/mimetypes.html#mimetypes.guess_type)\nfunction of python's inbuilt module\n[`mimetypes`](https://docs.python.org/3/library/mimetypes.html)\nis used for this purpose.\n\n> ***NOTE*** Dotfiles are not affected by dirganize.\n\nYou can put a `.dirganize.yml` file ( inside the folder you want to dirganize )\nto provide a custom configuration.\n\n```yaml\n# .dirganize.yml\n# folder: [ext1,ext2, ...]\nAnimations: [gif]\nBinaries: [bin,dat]\n```\n\nBasically you have the folder name,\nmapped to the list of file types to put in that folder.\n\nDirganize will first try to determine the destination directory from the `.dirganize.yml`.\nWhen the yaml configuration file is absent or\nthe folder for an encountered file type is not defined in the configuration,\n`dirganize` will fallback to the default technique.\n",
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
