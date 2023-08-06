# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mailru_im_command_bot']

package_data = \
{'': ['*']}

install_requires = \
['mailru-im-bot>=0.0.18',
 'mypy-extensions>=0.4.3,<0.5.0',
 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'mailru-im-command-bot',
    'version': '0.1.9',
    'description': 'Tiny lib for icq/myteam command bots',
    'long_description': '# mailru_im_command_bot\n[![PyPI](https://img.shields.io/pypi/v/mailru-im-command-bot?style=for-the-badge)](https://pypi.org/project/mailru-im-command-bot)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mailru-im-command-bot?style=for-the-badge)\n![tests](https://img.shields.io/github/workflow/status/dedefer/mailru-im-command-bot/lint%20and%20test/main?label=tests&style=for-the-badge)\n![coverage](https://img.shields.io/codecov/c/github/dedefer/mailru-im-command-bot?color=green&style=for-the-badge)\n\nmailru_im_command_bot is convenient library for generic myteam/icq bots.\nIn fact it is a wrapper for mailru-im-bot.\n\nIt uses type annotations for help method and transforming arguments.\n\nIt is fully tested and production-ready)\n\n[Pypi link](https://pypi.org/project/mailru-im-command-bot)\n\n## Usage\n\nYou can create your bot with following code:\n\n```python\nimport logging\n\nfrom mailru_im_command_bot import CommandBot, MessageEnv\n\nlogging.basicConfig(level=logging.INFO)\n\nbot = CommandBot(\n    token=\'your_token\',\n    help_message=\'this is simple hello world bot\'\n)\n\n\n@bot.command(\'hello\')\ndef hello(env: MessageEnv, name=\'world\') -> str:\n    return f\'hello {name}\'\n\n\nbot.start()\n```\n\nBot will response you:\n\n```text\nyou: /hello\nbot: hello world\n\nyou: /hello danila\nbot: hello danila\n```\n\nHelp message will be:\n\n```text\nthis is simple hello world bot\n\nlist of commands:\n/hello\n  args:\n    name: str = world\n```\n\n## Advanced Usage\n\nBot can automatically parse int, float, bool, any enum.Enum\nand also any type that implements mailru_im_command_bot.CustomParam protocol:\n\n```python\nimport enum\nimport logging\nfrom logging import getLogger\n\nfrom mailru_im_command_bot import BadArg, CommandBot, MessageEnv\n\nlogging.basicConfig(level=logging.INFO)\n\n\nclass Email(str):\n    @classmethod\n    def verbose_classname(cls) -> str:\n        return cls.__name__\n\n    @classmethod\n    def from_arg(cls, arg: str) -> \'Email\':\n        if \'@\' not in arg:\n            raise BadArg(f\'{arg} is invalid email\')\n        return cls(arg)\n\n    def to_arg(self) -> str:\n        return str(self)\n\n\nclass ExampleEnum(enum.Enum):\n    case_one = 1\n    case_two = 2\n\n\nbot = CommandBot(\n    token=\'tour_token\',\n    name=\'your_bot_name\',\n    version=\'1.0.0\',\n    logger=getLogger(__name__),\n    alert_to=[\'your_id\'],\n    help_message=\'your bot description\',\n)\n\n\n@bot.command(\'example_command\')\ndef example_command(\n    env: MessageEnv,\n    int_arg: int,  # required\n    float_arg: float = 1.0,  # optional\n    str_arg: str = \'test_str\',  # optional\n    enum_arg: ExampleEnum = ExampleEnum.case_one,  # optional\n    bool_arg: bool = True,  # optional\n    email_arg: Email = Email(\'ddf1998@gmail.com\'),  # optional\n) -> str:\n    """your function help message"""\n    ...\n    return \'response\'\n\n\nbot.start()\n```\n\nYou can also wrap existing bot:\n\n```python\nfrom bot import Bot\nfrom mailru_im_command_bot import CommandBot\nfrom logging import getLogger\n\nbase_bot = Bot(\n    token=\'your_token_here\',\n    name=\'your_bot_name\',\n    version=\'your_bot_version\',\n)\n\nbot = CommandBot(\n    from_bot=base_bot,\n    logger=getLogger(__name__),\n    alert_to=[\'danila.fomin@corp.mail.ru\'],\n    help_message=\'your bot description\',\n)\n\n```\n\nBot accepts messages like this:\n\n```text\n/example_command 1\n# you get int_arg = 1 and other arguments defaults\n\n/example_command 1 0\n# you get int_arg = 1, float_arg = 0.0 and other arguments defaults\n\n...etc\n```\n\nIt also can accept key-value arguments:\n\n```text\n/example_command int_arg=1\n/example_command 1 enum_arg=case_two\n/example_command int_arg=1 enum_arg=case_two\n```\n\nYour help message will be like this:\n\n```text\nyour bot description\n\nlist of commands:\n/example_command\n  your function help message\n  args:\n    int_arg: int\n    float_arg: float = 1.0\n    str_arg: str = test_str\n    enum_arg: case_one|case_two = case_one\n    bool_arg: True|False = True\n    email_arg: Email = ddf1998@gmail.com\n```\n\nBot automatically writes access log with provided logger.\n\n```text\n[ACCESS] [user_id]@[chat_id] /example_command elapsed=0.100s\n```\n\nIf an exception occurred bot will write the error into log, send `\'some exception occurred\'` to user and report error to users in `alert_to` list.\n',
    'author': 'Danila Fomin',
    'author_email': 'ddf1998@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dedefer/mailru-im-command-bot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
