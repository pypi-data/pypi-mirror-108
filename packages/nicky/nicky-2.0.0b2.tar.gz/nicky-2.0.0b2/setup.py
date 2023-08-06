# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nicky', 'nicky.commands']

package_data = \
{'': ['*'], 'nicky': ['nicknames/en/*', 'nicknames/jp/*', 'nicknames/ko/*']}

install_requires = \
['click==7.0.0']

entry_points = \
{'console_scripts': ['nicky = nicky.cli:cli']}

setup_kwargs = {
    'name': 'nicky',
    'version': '2.0.0b2',
    'description': 'Nicky the nicknamer',
    'long_description': "Nicky\n-------------\n.. image:: https://badge.fury.io/py/nicky.svg\n    :target: https://badge.fury.io/py/nicky\n\n\nNicky is the nicknamer. You can make funny nickname with nicky!\n\nHow to use\n==============\n\n1. with pip\n^^^^^^^^^^^^\n\n.. code::\n\n    # install local env\n    pip install nicky\n\n    # or install globally.\n    pip install --user nicky\n\n    nicky name\n    > 향긋한 까치\n\n    nicky name 5\n    > 신성한 스콘\n    > 똘망똘망한 오미자차\n    > 향긋한 스테이크\n    > 활기찬 사탕\n    > 엄청난 순대\n..\n\n2. with code\n^^^^^^^^^^^^\n\n.. code::\n\n    from nicky import Nicky\n\n    n = Nicky(lang='ko')\n    n.get_nicknames(3)\n    > ['신성한 스콘', '똘망똘망한 오미자차', '향긋한 스테이크']\n..\n\nIf you want more, just type :code:`nicky [command] --help`\n\n\nLocalization and more nicknames\n-----------------------------------\n\nFolk and clone this project. and add your language code folder in :code:`nicky/nicknames`\n\nAfter then, you can use :code:`nicky-cli.py` to add your nickname prefix and suffix.\n\n.. code::\n\n    python3 nicky-cli.py add [prefix|suffix|pre|suf|p|s] {values} [-l|--lang] {language}\n..\n\n    You can add multiple values. Separate your values with comma like :code:`a,b,c`. Remember, there's no space.\n\n**example)**\n\n.. code::\n\n    python3 nicky-cli.py add pre melon,potato,tomato --lang en\n..\n\nAfter all, pull requests to master branch.",
    'author': 'jrog612',
    'author_email': 'jrog612@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jrog612/nicky',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
