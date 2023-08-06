# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['radiacode', 'radiacode.decoders', 'radiacode.transports']

package_data = \
{'': ['*']}

install_requires = \
['bluepy>=1.3.0,<2.0.0', 'pyusb>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'radiacode',
    'version': '0.1.0',
    'description': 'Library for RadiaCode-101',
    'long_description': '## RadiaCode\n\nБиблиотека для работы с дозиметром [RadiaCode-101](https://scan-electronics.com/dosimeters/radiacode/radiacode-101)\n\nНаходится в разработке, доступны базовые команды: получение спектра, управление звуком и выбро, получение истории измерений и т.п.\n\nAPI пока не стабилен и возможны большие изменения!\n\n![screenshot](./screenshot.png)\n\n### Как запустить\n- Установить [python poetry](https://python-poetry.org/docs/#installation)\n- Склонировать репозиторий, установить и запустить:\n```\n$ git clone https://github.com/cdump/radiacode.git\n$ cd radiacode\n$ poetry install\n$ poetry run python3 example.py --bluetooth-mac 52:43:01:02:03:04\n```\nБез указания `--bluetooth-mac` будет использоваться USB подключение.\n',
    'author': 'Maxim Andreev',
    'author_email': 'andreevmaxim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cdump/radiacode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
