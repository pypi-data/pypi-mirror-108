# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['rsbcli']
install_requires = \
['PyQt5>=5.15.4,<6.0.0', 'PyQtWebEngine>=5.15.4,<6.0.0', 'click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['rcb = RSBCLI:main']}

setup_kwargs = {
    'name': 'rsbcli',
    'version': '0.1.1',
    'description': 'A RAM saving cli to run web applications',
    'long_description': '# RSB\n\n## A RAM saving cli to run web applications\n\n### Note : It is my first cli, so please inform me if somethingn is wrong\n\n\nSoftwares used\n\nVisual Studio Code - https://github.com/Microsoft/vscode\n\nPython 3.9.1\n\nSpecial Thanks to https://github.com/arghyagod-coder\n\n',
    'author': 'Avanindra Chakraborty',
    'author_email': 'avanindra.d2.chakraborty@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AvanindraC/RSB',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
