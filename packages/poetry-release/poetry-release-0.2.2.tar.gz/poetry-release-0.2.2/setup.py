# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_release']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0a1,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['poetry-release = '
                               'poetry_release.plugin:ReleasePlugin']}

setup_kwargs = {
    'name': 'poetry-release',
    'version': '0.2.2',
    'description': 'Plugin for release management in projects based on Poetry',
    'long_description': '# Poetry release\n\nRelease managment plugin for poetry\n\nInspired by [cargo-release](https://github.com/sunng87/cargo-release)\n\n## Features\n- [x] [Semver](https://semver.org/) support\n- [x] Creating git tag and commits after release\n- [ ] [Changelog](https://keepachangelog.com/en/1.0.0/) support\n',
    'author': 'Denis Kayshev',
    'author_email': 'topenkoff@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/topenkoff/poetry-release',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
