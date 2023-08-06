# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiomsa', 'aiomsa.mock', 'aiomsa.mock.e2']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-swagger>=1.0.9,<2.0.0',
 'aiohttp>=3.5.4,<4.0.0',
 'prometheus-async>=19.2.0,<20.0.0']

extras_require = \
{'docs': ['furo>=2021.2.21b25,<2022.0.0',
          'sphinx>=3.4.3,<4.0.0',
          'sphinx-autodoc-typehints>=1.11.1,<2.0.0',
          'sphinxcontrib-openapi>=0.7.0,<0.8.0']}

setup_kwargs = {
    'name': 'aiomsa',
    'version': '0.1.0a5',
    'description': 'Asynchronous xApp framework',
    'long_description': '# aiomsa\n[![build](https://github.com/facebookexternal/aiomsa/actions/workflows/build.yml/badge.svg)](https://github.com/facebookexternal/aiomsa/actions/workflows/build.yml)\n[![style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/aiomsa)\n\n*aiomsa* is a Python 3.7+ framework built using `asyncio`. At its core, *aiomsa*\nprovides a simple and standardized way to write xApps that can be deployed as\nmicroservices in Python.\n\n## Installation\n*aiomsa* can be installed from PyPI.\n```bash\npip install aiomsa\n```\n\nYou can also get the latest code from GitHub.\n```bash\npoetry add git+https://github.com/facebookexternal/aiomsa\n```\n\n## Getting Started\nThe follwing example shows how to use *aiomsa* to create a simple xApp for subscribing\nto the E2T service for a particular custom service model.\n\n```python\nimport aiomsa\nfrom aiomsa.models import (\n    RICAction,\n    RICActionType,\n    RICSubsequentActionType,\n    RICTimeToWait,\n)\nfrom onos_ric_sdk_py.e2 import E2Client\n\nfrom .servicemodels import MyModel\n\n\nasync def main():\n   async with E2Client(\n      app_id="my_app", e2t_endpoint="e2t:5150", e2sub_endpoint="e2sub:5150"\n   ) as e2:\n      nodes = await e2.list_nodes()\n      subscription = await e2.subscribe(\n         e2_node_id=nodes[0].id,\n         service_model_name="my_model",\n         service_model_version="v1",\n         trigger=bytes(MyModel(param="foo")),\n         actions=[\n            RICAction(\n               id=1,\n               type=RICActionType.REPORT,\n               subsequent_action_type=RICSubsequentActionType.CONTINUE,\n               time_to_wait=RICTimeToWait.ZERO,\n            )\n         ],\n      )\n\n      async for (_header, message) in subscription:\n         print(message)\n\n\nif __name__ == "__main__":\n   aiomsa.run(main())\n```\n',
    'author': 'Facebook Connectivity',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/facebookexternal/aiomsa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
