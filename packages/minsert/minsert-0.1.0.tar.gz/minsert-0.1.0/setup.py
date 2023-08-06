# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minsert']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'minsert',
    'version': '0.1.0',
    'description': 'Insert dynamic content in markdown, without using a separate template file.',
    'long_description': '# minsert\n\nInsert dynamic content in markdown, without using a separate template file.\n\n[![Tests](https://github.com/aahnik/minsert/actions/workflows/test.yml/badge.svg)](https://github.com/aahnik/minsert/actions/workflows/test.yml)\n[![Code Quality](https://github.com/aahnik/minsert/actions/workflows/quality.yml/badge.svg)](https://github.com/aahnik/minsert/actions/workflows/quality.yml)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/minsert)\n[![codecov](https://codecov.io/gh/aahnik/minsert/branch/main/graph/badge.svg?token=Q1XROUHDRM)](https://codecov.io/gh/aahnik/minsert)\n\n## Motivation\n\nInspired by jinja.\n\nYour actual markdown file is the template file itself.\nJust make a block of content just by using comments, which indicate the start and\nend of the block.\n\nThis is really great for making a dynamic GitHub README.\nNo hassle of creating a separate template file.\nUsing a simple python script and GitHub Actions,\nyou can automatically update the contents of the markdown file.\n\n## Installation\n\n```shell\npip install minsert\n```\n\n## Syntax\n\nUsing minsert is easy. Just write normal markdown.\nThe start and end of named blocks are marked by special comments.\n\nStart a block named `my_block`\n\n```markdown\n<!-- start my_block -->\n```\n\nEnd a block\n\n```markdown\n<!-- end -->\n```\n\nYou must end the current block before starting a new one.\n\n## Usage\n\nFor example you have a markdown file `test.md` like this.\n\n```markdown\nhello\n<!-- start thing1 -->\n<!-- end -->\nwhat is happening\n<!-- start thing2 -->\n<!-- end -->\nBye!\n```\n\nCreate a simple script `update.py` for updating the markdown file.\n\n```python\n# update.py\n\nfrom minsert import MarkdownFile\n\nfile = MarkdownFile("test.md")\nthings = {\n    "thing1": "hi hello",\n    "thing2": "ping pong",\n}\nfile.insert(things)\n\n```\n\nThe markdown file gets updated with the value of the blocks.\n\n```markdown\nhello\n<!-- start thing1 -->\nhi hello\n<!-- end -->\nwhat is happening\n<!-- start thing2 -->\nping pong\n<!-- end -->\nBye!\n```\n\nNow try running `update.py` after changing the values in the `things` dictionary.\nYou will see that minsert will neatly update the `test.md` without fail.\n',
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aahnik/minsert',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
