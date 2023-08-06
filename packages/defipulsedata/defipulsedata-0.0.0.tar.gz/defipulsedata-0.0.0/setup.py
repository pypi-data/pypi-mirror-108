# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['defipulsedata']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'minilog>=2.0,<3.0', 'responses>=0.13.3,<0.14.0']

entry_points = \
{'console_scripts': ['defipulsedata = defipulsedata.cli:main']}

setup_kwargs = {
    'name': 'defipulsedata',
    'version': '0.0.0',
    'description': 'Unofficial SDK for DeFi Pulse Data',
    'long_description': '# Overview\n\nAn unofficial Python SDK for the [DeFi Pulse Data](https://docs.defipulse.com/) project and\neach of its partner service providers. This project provides a lightweight Python\nclient for each service provider.\n\nCurrently, the DeFi Pulse Data service providers include:\n\n- [DeFi Pulse](https://defipulse.com/)\n- [ETH Gas Station](https://ethgasstation.info/)\n- [DEX.AG](https://dex.ag/)\n- [Rek.to](https://app.rek.to/)\n- [Pools.fyi](https://pools.fyi/#/)\n\nThe goals of this package are to empower Python programmers to make use of DeFi Pulse Data services,\nto enrich the broader DeFi developer ecosystem, and to reduce overall developer effort by providing\na packaged developer SDK so that developers do not need to reinvent the wheel for each project they make.\n\nThis project bears no official relationship to the DeFi Pulse Data project, or the\n[Concourse Open Community](https://concourseopen.com/) project.\n\n# Setup\n\n## Requirements\n\n* Python 3.7+\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install defipulsedata\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add defipulsedata\n```\n\n# Usage\n\nAfter installation, the package can imported.\n\nEach module below corresponds to a single, logical data provider service defined in\nthe [DeFi Pulse Data documentation](https://docs.defipulse.com/).\n\n```python\nfrom defipulsedata import RekTo, EthGasStation, DefiPulse, DexAg, PoolsFyi\n\nkey=\'REPLACE-WITH-YOUR-KEY\'\n\n# Example requests for each client.\n\n# Rek.to\nrekto = RekTo(api_key=key)\nrekto.get_events()\n\n# DeFi Pulse\ndp = DefiPulse(api_key=key)\ndp.get_projects()\n\n# ETH Gas Station\negs = EthGasStation(api_key=key)\negs.get_gas_price()\n\n# DEX.AG\ndexag = DexAg(api_key=key)\ndexag.get_markets()\n\n# Pools.Fyi\npools = PoolsFyi(api_key=key)\npools.get_exchanges()\n```\n\n# Contributing and Filing Issues\n\nDetails for local development dependencies and useful Make targets can be found in `contributing.md`\n\nContributions, suggestions, bug reports, are welcome and encouraged.\n\nIf you have a bug or issue, please file a GitHub issue on the project describing the expected behavior and the actual behavior, with steps to reproduce the issue.\n\nIf you have a feature request, please file a GitHub issue on the project describing the feature you want, and why you want it.\n\n# License\n\n**The MIT License (MIT)**\n\nCopyright &copy; 2021, James Boyle\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in\nall copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\nTHE SOFTWARE.\n',
    'author': 'James Boyle',
    'author_email': 'pydefipulsedata@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/defipulsedata',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
