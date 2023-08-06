# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nginx_language_server', 'nginx_language_server.parser']

package_data = \
{'': ['*'], 'nginx_language_server': ['data/*']}

install_requires = \
['crossplane>=0.5.7,<0.6.0', 'pydantic>=1.7.3,<2.0.0', 'pygls>=0.10.3,<0.11.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.8"': ['importlib-metadata>=3.10.0,<4.0.0']}

entry_points = \
{'console_scripts': ['nginx-language-server = nginx_language_server.cli:cli']}

setup_kwargs = {
    'name': 'nginx-language-server',
    'version': '0.7.0',
    'description': 'A language server for nginx.conf',
    'long_description': '# Nginx Language Server\n\n[![image-version](https://img.shields.io/pypi/v/nginx-language-server.svg)](https://python.org/pypi/nginx-language-server)\n[![image-license](https://img.shields.io/badge/license-GPL%203.0--only-orange)](https://python.org/pypi/jedi-language-server)\n[![image-python-versions](https://img.shields.io/badge/python->=3.6-blue)](https://python.org/pypi/jedi-language-server)\n\nA [Language Server](https://microsoft.github.io/language-server-protocol/) for `nginx.conf`.\n\nStill under construction, expect big / potentially breaking changes for a while.\n\n## Capabilities\n\nnginx-language-server currently partially supports the following Language Server capabilities with more to be added in the future.\n\n### Language Features\n\n- [textDocument/completion](https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_completion)\n- [textDocument/hover](https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_hover)\n\n## Installation\n\nFrom your command line (bash / zsh), run:\n\n```bash\npip install -U nginx-language-server\n```\n\n`-U` ensures that you\'re pulling the latest version from pypi.\n\nAlternatively, consider using [pipx](https://github.com/pipxproject/pipx) to keep nginx-language-server isolated from your other Python dependencies.\n\n## Editor Setup\n\nThe following instructions show how to use nginx-language-server with your development tooling. The instructions assume you have already installed nginx-language-server.\n\n### Vim / Neovim\n\nWith [coc.nvim](https://github.com/neoclide/coc.nvim), put the following in `coc-settings.json`:\n\n```json\n  "languageserver": {\n    "nginx-language-server": {\n      "command": "nginx-language-server",\n      "filetypes": ["nginx"],\n      "rootPatterns": ["nginx.conf", ".git"]\n    }\n  },\n```\n\nIn your vimrc, I recommend putting in the following lines to ensure variables complete / hover correcty:\n\n```vim\naugroup custom_nginx\n  autocmd!\n  autocmd FileType nginx setlocal iskeyword+=$\n  autocmd FileType nginx let b:coc_additional_keywords = [\'$\']\naugroup end\n```\n\nNote: this list is non-exhaustive. If you know of a great choice not included in this list, please submit a PR!\n\n## Command line\n\nnginx-language-server can be run directly from the command line.\n\n```console\n$ nginx-language-server --help\nusage: nginx-language-server [-h] [--version] [--tcp] [--host HOST]\n                             [--port PORT] [--log-file LOG_FILE] [-v]\n\nNginx language server: an LSP server for nginx.conf.\n\noptional arguments:\n  -h, --help           show this help message and exit\n  --version            display version information and exit\n  --tcp                use TCP server instead of stdio\n  --host HOST          host for TCP server (default 127.0.0.1)\n  --port PORT          port for TCP server (default 2088)\n  --log-file LOG_FILE  redirect logs to the given file instead of writing to\n                       stderr\n  -v, --verbose        increase verbosity of log output\n\nExamples:\n\n    Run from stdio: nginx-language-server\n```\n\n## Inspiration\n\nThe useful language data for nginx is ported from [vscode-nginx-conf-hint](https://github.com/hangxingliu/vscode-nginx-conf-hint). I would have used this library directly, but alas! It\'s written only for VSCode and I use Neovim.\n\n## Written by\n\nSamuel Roeca _samuel.roeca@gmail.com_\n',
    'author': 'Sam Roeca',
    'author_email': 'samuel.roeca@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pappasam/nginx-language-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
