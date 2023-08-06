# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camelcalc']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['camelup = camelcalc.play:main']}

setup_kwargs = {
    'name': 'camelcalc',
    'version': '0.1.0',
    'description': 'A Camel Up simulator and optimizer',
    'long_description': "# camelcalc\n\n![Build and Publish](https://github.com/ArmaanT/camelcalc/workflows/Build%20and%20Publish/badge.svg)\n[![PyPi Package](https://img.shields.io/pypi/v/camelcalc.svg)](https://pypi.org/project/camelcalc/)\n\nA playable version of [Camel Up](https://en.wikipedia.org/wiki/Camel_Up). As well as a (soon to exist) calculator to help determine what move a team should make.\n\n## Requirements\n\n* Python 3.8+\n* Friends to play with\n\n## Installation\n\nInstall with pip `pip install camelcalc`\n\nThen play Camel Up by running `camelup`\n\n## Why?\n\nAt the end of every semester, the [CIS 120](https://www.seas.upenn.edu/~cis120/current/) TA staff play Camel Up. I've been telling myself that I wanted to attempt to build a calculator for it, so here's my attempt.\n\n## License\n\nSee [LICENSE](./LICENSE)\n",
    'author': 'Armaan Tobaccowalla',
    'author_email': 'armaan@tobaccowalla.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ArmaanT/camelcalc',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
