# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['goli']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter>=1.7.3,<2.0.0']

entry_points = \
{'console_scripts': ['goli = goli.__main__:cli']}

setup_kwargs = {
    'name': 'goli',
    'version': '0.1.0',
    'description': 'The last boilerplate generator you will need (seriously)',
    'long_description': '# goli\n\n<div align="center">\n\n[![Build status](https://github.com/nidhaloff/goli/workflows/build/badge.svg?branch=master&event=push)](https://github.com/nidhaloff/goli/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/goli.svg)](https://pypi.org/project/goli/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/nidhaloff/goli/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/nidhaloff/goli/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/nidhaloff/goli/releases)\n\n[![License](https://img.shields.io/github/license/nidhaloff/goli)](https://github.com/nidhaloff/goli/blob/master/LICENSE)\n\nA sophisticated boilerplate generator based on best practices modern templates\n\n</div>\n\n> **_NOTE:_**  The project is heavily inspired by cookiecutter and aim to make a good collection of modern boilerplate templates that proven useful in the last years.\n\n\n## Installation\n\n```bash\npip install -U goli\n```\n\nor install with `Poetry`\n\n```bash\npoetry add goli\n```\n\nThen you can run `goli --help ` to show the help message on how to use the package\n\n```bash\n\nUsage: goli [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  languages  Show all supported programming languages\n  new        Generate new boilerplate code for your project\n  topics     Show all supported topics.\n```\nAs you can see, goli provides three commands. The languages and topics commands are additional to get more information about how to use the package. The new command is the most important and it is used to start a new project. More on that in the next section.\n\n## Usage\n\ngoli provides the new command, which is used to create a new boilerplate depending on two optional parameters that you need to provide. \n\n- The `language` parameter, which indicates the programming language you want to use or you will use for your project. You can check supported languages if you run `goli languages`\n\n- The `topic` parameter, which should indicate the topic of your project. You can check the topics supported by goli if you run `goli topics`\n\n```bash\ngoli new --language python --topic data-science\n```\nor the short version\n\n```bash\ngoli new -l python -t data-science\n```\n\nThis will pull the modern cookiecutter-data-science template (https://github.com/drivendata/cookiecutter-data-science) and execute it in your current working directory. So you don\'t have to search for templates since best practices are already built-in and being updated regularly. \n',
    'author': 'nidhaloff',
    'author_email': 'nidhalbacc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nidhaloff/goli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
