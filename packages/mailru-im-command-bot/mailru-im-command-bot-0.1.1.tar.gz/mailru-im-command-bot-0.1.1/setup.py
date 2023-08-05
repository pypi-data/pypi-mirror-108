# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mailru_im_command_bot']

package_data = \
{'': ['*']}

install_requires = \
['mailru-im-bot>=0.0.18']

setup_kwargs = {
    'name': 'mailru-im-command-bot',
    'version': '0.1.1',
    'description': 'Tiny lib for icq/myteam command bots',
    'long_description': '# mailru_im_command_bot\n\nmailru_im_command_bot is convenient library for generic myteam/icq bots.\nIn fact it is wrapper for mailru-im-bot.\n\nIt uses type annotations for help method and transforming arguments.\n\nIt is fully tested and production-ready)\n\n## Usage\n\nYou can create your bot with following code:\n\n```python\nfrom mailru_im_command_bot import CommandBot, MessageEnv\nfrom logging import getLogger\nimport enum\n\n\nclass ExampleEnum(enum.Enum):\n    case_one = 1\n    case_two = 2\n\n\nbot = CommandBot(\n    # you can provide any bot.Bot kwargs\n    token=\'your_token_here\',\n    name=\'your_bot_name\',\n    version=\'your_bot_version\',\n    logger=getLogger(__name__),\n    alert_to=[\'danila.fomin@corp.mail.ru\'],\n    help_message=\'your bot description\',\n)\n\n@bot.command(\'example_command\')\ndef example_command(\n    env: MessageEnv,\n    int_arg: int,  # required\n    float_arg: float = 1.0,  # optional\n    str_arg: str = \'test_str\',  # optional\n    enum_arg: ExampleEnum = ExampleEnum.case_one,  # optional\n) -> str:\n    """your function help message"""\n    ...\n    return \'your result\'\n\nbot.start()\n```\n\nYou can also wrap existing bot:\n\n```python\nfrom bot import Bot\nfrom mailru_im_command_bot import CommandBot\nfrom logging import getLogger\n\nbase_bot = Bot(\n    token=\'your_token_here\',\n    name=\'your_bot_name\',\n    version=\'your_bot_version\',\n)\n\nbot = CommandBot(\n    from_bot=base_bot,\n    logger=getLogger(__name__),\n    alert_to=[\'danila.fomin@corp.mail.ru\'],\n    help_message=\'your bot description\',\n)\n\n...\n\nbase_bot.start_polling()\n```\n\nBot accepts messages like this:\n\n```text\n/example_command 1\n# you get int_arg = 1 and other arguments defaults\n\n/example_command 1 0\n# you get int_arg = 1, float_arg = 0.0 and other arguments defaults\n\n...etc\n```\n\nAs argument type you can use str, float, int and any enum.Enum. Library automatically validates and casts strings to your types.\n\nYour help message will be like this:\n\n```text\nyour bot description\n\nlist of commands:\n  /example_command\n    your function help message\n    args:\n      int_arg: int\n      float_arg: float = 1.0\n      str_arg: str = test_str\n      enum_arg: case_one|case_two = case_one\n```\n\nBot automatically writes access log with provided logger.\n\n```text\n[ACCESS] [user_id]@[chat_id] /example_command elapsed=0.1s\n```\n\nIf an exception occured bot will write the error into log, send `\'some error occured\'` to user and report error to users in `alert_to` list.\n',
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
