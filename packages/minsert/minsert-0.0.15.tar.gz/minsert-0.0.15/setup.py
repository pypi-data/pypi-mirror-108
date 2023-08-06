# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minsert']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'minsert',
    'version': '0.0.15',
    'description': 'Insert dynamic content in markdown, without using a separate template file.',
    'long_description': "# minsert\n\nInsert dynamic content in markdown, without using a separate template file.\n\n## Motivation\n\nInspired by jinja. 😂\n\nYour actual markdown file is the template file itself.\nJust make a block of content just by using comments, which indicate the start and\nend of the block.\n\nThis is really great for GitHub repo README. No hassle of creating a separate\ntemplate file.\n\n## Installation\n\n```shell\npip install minsert\n```\n\n## Syntax\n\nStart a block : `<!-- start: thing -->`\n\nEnd of a block: `<!-- end -->`\n\nYou must end current block before starting a new one.\n\n## Usage\n\n```python\nfrom minsert import MarkdownFile\nfile = MarkdownFile('test.md')\nthings = {'thing1': 'hi hello',\n          'thing2': 'ping pong',\n          }\nfile.insert(things)\n\n```\n\n## Example\n\nTake a long hard look at this gif!\n\n![minsert](https://user-images.githubusercontent.com/66209958/99037312-7bb39700-25a9-11eb-9d1e-2a15d76a8d10.gif)\n",
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
