#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

import asyncio
import base64
import itertools
import json
from typing import Dict, List, Optional, Tuple

from aiomsa import e2, models


class Message:
    """Takes base64 encoded header and message and stores them as bytes."""

    def __init__(self, header: str, message: str, delay_ms: int = 0) -> None:
        self.header = base64.b64decode(header)
        self.message = base64.b64decode(message)
        self.delay_ms = delay_ms

    def dump(self) -> Tuple[bytes, bytes]:
        return self.header, self.message


class Stream:
    """A set of messages emitted by this module repeatedly."""

    def __init__(
        self,
        messages: List[Dict],
        repeat: int = 1,
    ) -> None:
        self.repeat = repeat
        self.messages = [Message(**message) for message in messages]


class StaticNode(models.E2Node):
    """A mock E2Node for E2 message playback."""

    def __init__(self, e2_node_id: str, streams: List[Stream]) -> None:
        super().__init__(e2_node_id, [])
        self.streams = streams


class Subscription(e2.Subscription):
    def __init__(self, node: StaticNode) -> None:
        self.node = node
        self.message_iter = itertools.chain.from_iterable(
            [
                itertools.chain.from_iterable(
                    itertools.repeat(stream.messages, stream.repeat)
                )
                for stream in node.streams
            ]
        )

    async def getmessage(self) -> Optional[Tuple[bytes, bytes]]:
        try:
            message = next(self.message_iter)
            await asyncio.sleep(message.delay_ms / 1000)
            return message.dump()
        except StopIteration:
            raise StopAsyncIteration

    @property
    def id(self) -> str:
        return self.node.id

    def __aiter__(self) -> "Subscription":
        return self

    async def __anext__(self) -> Optional[Tuple[bytes, bytes]]:
        while True:
            return await self.getmessage()


class E2Client(e2.E2Client):
    def __init__(self, staticfile: str) -> None:
        self.e2nodes = {}

        with open(staticfile) as f:
            static_data = json.loads(f.read())

        for k, v in static_data["nodes"].items():
            streams = [Stream(**s) for s in v["streams"]]
            self.e2nodes[k] = StaticNode(k, streams)

    async def list_nodes(self, oid: Optional[str] = None) -> List[models.E2Node]:
        return list(self.e2nodes.values())

    async def control(
        self,
        e2_node_id: str,
        service_model_name: str,
        service_model_version: str,
        header: bytes,
        message: bytes,
        control_ack_request: models.RICControlAckRequest,
    ) -> Optional[bytes]:
        pass

    async def subscribe(
        self,
        e2_node_id: str,
        service_model_name: str,
        service_model_version: str,
        trigger: bytes,
        actions: List[models.RICAction],
    ) -> Subscription:
        return Subscription(self.e2nodes[e2_node_id])

    async def unsubscribe(self, subscription_id: str) -> None:
        pass

    async def __aenter__(self) -> "E2Client":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass
