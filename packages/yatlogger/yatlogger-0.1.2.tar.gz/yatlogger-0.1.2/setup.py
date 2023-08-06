# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yatlogger']

package_data = \
{'': ['*']}

install_requires = \
['python-telegram-bot>=13.6,<14.0']

setup_kwargs = {
    'name': 'yatlogger',
    'version': '0.1.2',
    'description': 'Yet another telegram logger',
    'long_description': '# Yet Another Telegram Logger\n\n## Setup\n\n### 1. Create a bot\n\nFirst, [create a new bot](https://core.telegram.org/bots#creating-a-new-bot). It\'s basically sending some messages to [@BotFather](https://t.me/botfather).\n\n### 2. Create a config file (`.yatlogger.json`)\n\nNext, create a file named `.yatlogger.json` and place it in the same directory as your code or in a one of the parent directories. The file must look like this:\n\n``` json\n{\n    "token": "<your api key>"\n}\n```\n\nReplace `<your api key>` with the API key you got from the BotFather.\n\n### 3. Register chats\n\nYour bot must know to which chats it should send the logs. So the next step is to register receiving chats.\n\nRun `python -m yatlogger` to start the register service. As long as this service is running, you can register new chats.\n\nTo register a chat, start a chat with your bot and enter the 6 digit pin you see on the logging machine.\n\n![register a new chat](https://raw.githubusercontent.com/cyd3r/yatlogger/main/docs/register_chat.jpg)\n\nWhen you are done, you can simply interrupt the register service with <kbd>Ctrl</kbd> + <kbd>C</kbd>\n\n## Usage\n\nyatlogger registers itself as a handler for the `logging` module. Here is an example:\n\n``` python\nimport logging\nimport yatlogger\n\nlogger = yatlogger.register()\nlogger.setLevel(logging.INFO)\n\nlogger.info("Read this on your phone!")\n\nraise ValueError("This unhandled exception will be sent to Telegram, too!")\n\n```\n\n![log messages on telegram](https://raw.githubusercontent.com/cyd3r/yatlogger/main/docs/logs.jpg)\n',
    'author': 'cyd3r',
    'author_email': 'cyd3rhacker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cyd3r/yatlogger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
