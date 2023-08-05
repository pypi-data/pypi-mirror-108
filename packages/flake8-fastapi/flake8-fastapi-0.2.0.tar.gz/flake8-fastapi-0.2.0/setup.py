# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_fastapi', 'flake8_fastapi.visitors']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.65.1,<0.66.0', 'flake8-pytest-style>=1.4.2,<2.0.0']

entry_points = \
{'flake8.extension': ['CF = flake8_fastapi.plugin:FastAPIPlugin']}

setup_kwargs = {
    'name': 'flake8-fastapi',
    'version': '0.2.0',
    'description': 'flake8 plugin that checks FastAPI code against opiniated style rules 🤓',
    'long_description': '<h1 align="center">\n    <strong>flake8-fastapi</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/flake8-fastapi" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/flake8-fastapi" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/flake8-fastapi/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/flake8-fastapi">\n    <br />\n    <a href="https://pypi.org/project/flake8-fastapi" target="_blank">\n        <img src="https://img.shields.io/pypi/v/flake8-fastapi" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/flake8-fastapi">\n    <img src="https://img.shields.io/github/license/Kludex/flake8-fastapi">\n</p>\n\n\n## Installation\n\n``` bash\npip install flake8-fastapi\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/flake8-fastapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
