# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['disclist']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'disclist',
    'version': '0.0.2',
    'description': 'A simple asynchronous/synchronous wrapper for https://disclist.noxitb.repl.co/ Bot List.',
    'long_description': '# Guides:\nHere are guides of how to use this Python Wrapper.\n\n## Initiating your Client:\n```py\nfrom disclist import Client\n\nclient = Client(token="...", sync=True) # sync is a kwarg to set if functions need to be async or not. Defaults to True.\n```\n\n## Posting Stats:\n```py\n# If you set sync to True, it will not need to be awaited\n# Else, it needs to.\n# You can check it using `client.sync` or see the kwarg you set\n# if you are unsure.\n\n# For synchronous:\nclient.post_stats(server_count=1) # Set your server count to 1.\n\n# For asynchronous:\nawait client.post_stats(server_count=1) # Set your server count to 1.\n```\n\n## For checking if user has voted or not:\n```py\n# For synchronous:\nhas_voted = client.has_voted(user_id=1234567890)\n\n# For asynchronous:\nhas_voted = await client.has_voted(user_id=1234567890)\n\nprint(has_voted) # True/False\n```\n\n## For searching a bot using it\'s ID:\n```py\n# For synchronous:\nresult = client.search(bot_id=1234567890)\n\n# For asynchronous:\nresult = await client.search(bot_id=1234567890)\n\nprint(result) # {\'...\': ...}, Returns a dict.\n```\n\n# Where should I ask help?\nJoin our [discord](https://discord.gg/nZPaZbzYsb) to ask for help!\n\n# License:\nMIT',
    'author': 'proguy914629',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
