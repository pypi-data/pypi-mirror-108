==================================
Welcome to aiomsa's documentation!
==================================

.. toctree::
   :hidden:
   :maxdepth: 2

   reference
   misc

*aiomsa* is a Python 3.7+ framework built using :mod:`asyncio` and :mod:`aiohttp.web`.
At its core, *aiomsa* provides a simple and standardized way to write xApps that can be
deployed as microservices in Python.

In addition, *aiomsa* creates an HTTP server with
:doc:`preregistered endpoints<./routes>` for xApp configuration and Prometheus metric
exposition. Developers can add their own endpoints to this server for their own
application logic.

Usage
=====

The entrypoint for the *aiomsa* framework is the :func:`~.run` function.

.. autofunction:: aiomsa.run

Quickstart
----------

The follwing example shows how to use *aiomsa* to create a simple microservice for
consuming and printing indication messages from an E2T subscription.

.. code-block:: python

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

Installation
============

*aiomsa* can be installed from PyPI.

.. code-block:: bash

    $ pip install aiomsa

You can also get the latest code from GitHub.

.. code-block:: bash

    $ poetry add git+https://github.com/facebookexternal/aiomsa

Dependencies
============

* Python 3.7+
* aiohttp
* aiohttp-swagger
* prometheus-async
