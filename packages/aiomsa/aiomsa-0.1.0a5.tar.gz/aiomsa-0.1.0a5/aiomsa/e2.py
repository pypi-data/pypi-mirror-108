#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

import abc
from types import TracebackType
from typing import List, Optional, Tuple, Type

from .models import E2Node, RICAction, RICControlAckRequest


class Subscription(abc.ABC):
    @property
    @abc.abstractmethod
    def id(self) -> str:
        """Return an identifier for the subscription."""
        pass

    @abc.abstractmethod
    def __aiter__(self) -> "Subscription":
        """Initialize any resources, if needed."""
        pass

    @abc.abstractmethod
    async def __anext__(self) -> Optional[Tuple[bytes, bytes]]:
        """Return the next indication in the subscription.

        Returns:
            The next indication header and message, if available.

        Raises:
            StopAsyncIteration: The subscription has been exhausted.
        """
        pass


class E2Client(abc.ABC):
    @abc.abstractmethod
    async def list_nodes(self, oid: Optional[str] = None) -> List[E2Node]:
        """Fetch a list of available E2 nodes.

        Args:
            oid: RAN function object identifier used to filter E2 nodes.

        Returns:
            A list of avilable E2 nodes.
        """
        pass

    @abc.abstractmethod
    async def control(
        self,
        e2_node_id: str,
        service_model_name: str,
        service_model_version: str,
        header: bytes,
        message: bytes,
        control_ack_request: RICControlAckRequest,
    ) -> Optional[bytes]:
        """Send a control message to the RIC to initiate or resume some functionality.

        Args:
            e2_node_id: The target E2 node ID.
            service_model_name: The service model name.
            service_model_version: The service model version.
            header: The RIC control header.
            message: The RIC control message.
            control_ack_request: Instruct whether/how the E2 node should reply.

        Returns:
            The control outcome, if specifically requested via ``control_ack_request``,
            else ``None``.

        Raises:
            E2ClientError: The control outcome is failure or missing.
        """
        pass

    @abc.abstractmethod
    async def subscribe(
        self,
        e2_node_id: str,
        service_model_name: str,
        service_model_version: str,
        trigger: bytes,
        actions: List[RICAction],
    ) -> Subscription:
        """Establish an E2 subscription.

        Args:
            e2_node_id: The target E2 node ID.
            service_model_name: The service model name.
            service_model_version: The service model version.
            trigger: The event trigger.
            actions: A sequence of RIC service actions.

        Returns:
            The created subscription.
        """
        pass

    @abc.abstractmethod
    async def unsubscribe(self, subscription_id: str) -> None:
        """Delete an E2 subscription.

        Args:
            subscription_id: The ID of the subscription to delete.
        """
        pass

    @abc.abstractmethod
    async def __aenter__(self) -> "E2Client":
        """Create any underlying resources required for the client to run."""
        pass

    @abc.abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Cleanly stop all underlying resources used by the client."""
        pass
