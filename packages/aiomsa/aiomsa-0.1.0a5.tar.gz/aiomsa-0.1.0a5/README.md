# aiomsa
[![build](https://github.com/facebookexternal/aiomsa/actions/workflows/build.yml/badge.svg)](https://github.com/facebookexternal/aiomsa/actions/workflows/build.yml)
[![style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI - Downloads](https://img.shields.io/pypi/dw/aiomsa)

*aiomsa* is a Python 3.7+ framework built using `asyncio`. At its core, *aiomsa*
provides a simple and standardized way to write xApps that can be deployed as
microservices in Python.

## Installation
*aiomsa* can be installed from PyPI.
```bash
pip install aiomsa
```

You can also get the latest code from GitHub.
```bash
poetry add git+https://github.com/facebookexternal/aiomsa
```

## Getting Started
The follwing example shows how to use *aiomsa* to create a simple xApp for subscribing
to the E2T service for a particular custom service model.

```python
import aiomsa
from aiomsa.models import (
    RICAction,
    RICActionType,
    RICSubsequentActionType,
    RICTimeToWait,
)
from onos_ric_sdk_py.e2 import E2Client

from .servicemodels import MyModel


async def main():
   async with E2Client(
      app_id="my_app", e2t_endpoint="e2t:5150", e2sub_endpoint="e2sub:5150"
   ) as e2:
      nodes = await e2.list_nodes()
      subscription = await e2.subscribe(
         e2_node_id=nodes[0].id,
         service_model_name="my_model",
         service_model_version="v1",
         trigger=bytes(MyModel(param="foo")),
         actions=[
            RICAction(
               id=1,
               type=RICActionType.REPORT,
               subsequent_action_type=RICSubsequentActionType.CONTINUE,
               time_to_wait=RICTimeToWait.ZERO,
            )
         ],
      )

      async for (_header, message) in subscription:
         print(message)


if __name__ == "__main__":
   aiomsa.run(main())
```
