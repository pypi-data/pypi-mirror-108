# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pythondev_example']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.12.1,<4.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['pythondev-example = pythondev_example.console:main']}

setup_kwargs = {
    'name': 'pythondev-example',
    'version': '0.1.0',
    'description': 'An example python project that follows guidelines to modernize Python develpoment.',
    'long_description': "# pythondev-example\n[![Tests](https://github.com/dtherrick/pythondev-example/workflows/Tests/badge.svg)](https://github.com/dtherrick/pythondev-example/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/dtherrick/pythondev-example/branch/master/graph/badge.svg)](https://codecov.io/gh/dtherrick/pythondev-example)\n[![PyPI](https://img.shields.io/pypi/v/pythondev-example.svg)](https://pypi.org/project/pythondev-example/)\n\nBuilt from the hypermodern python guide, I'm using this to build out a coding style for my team at work.\n",
    'author': 'Damian Herrick',
    'author_email': 'damian.herrick@sas.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dtherrick/pythondev-example',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
