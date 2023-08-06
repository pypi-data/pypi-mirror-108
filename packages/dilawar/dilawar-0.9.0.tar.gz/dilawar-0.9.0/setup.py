# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dilawar', 'dilawar.audio', 'dilawar.bin', 'dilawar.pandoc']

package_data = \
{'': ['*'], 'dilawar.pandoc': ['templates/*']}

install_requires = \
['Pint>=0.17,<0.18',
 'colorama>=0.4.4,<0.5.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.20.3,<2.0.0',
 'pandocfilters>=1.4.3,<2.0.0',
 'panflute>=2.1.0,<3.0.0',
 'pydot[graph]>=1.4.2,<2.0.0',
 'pygraphviz[graph]>=1.7,<2.0',
 'pypandoc>=1.5,<2.0']

setup_kwargs = {
    'name': 'dilawar',
    'version': '0.9.0',
    'description': 'Personal collection of utilities',
    'long_description': None,
    'author': 'Dilawar Singh',
    'author_email': 'dilawar.s.rajput@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
