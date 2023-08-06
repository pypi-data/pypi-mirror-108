#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.
"""
O-RAN.WG3.E2AP-v02.00.02
"""

import dataclasses
import enum
from typing import List, Optional


class RICActionType(enum.IntEnum):
    """An :class:`~.enum.IntEnum` defining possible RIC actions.

    Attributes:
        REPORT
        INSERT
        POLICY
    """

    REPORT = 0
    INSERT = 1
    POLICY = 2


class RICControlAckRequest(enum.IntEnum):
    """An :class:`~.enum.IntEnum` defining circumstances in which the E2 node
    can/should reply to a RIC control acknowledge message.

    Attributes:
        ACK
        NO_ACK
        NACK
    """

    ACK = 0
    NO_ACK = 1
    NACK = 2


class RICSubsequentActionType(enum.IntEnum):
    """An :class:`~.enum.IntEnum` defining the valid actions that can be taken after
    completing a particular :class:`~.RICAction`.

    Attributes:
        CONTINUE
        WAIT
    """

    CONTINUE = 0
    WAIT = 1


class RICTimeToWait(enum.IntEnum):
    """An :class:`~.enum.IntEnum` defining the time to wait after completing a
    particular :class:`~.RICAction`.

    Attributes:
        ZERO
        W1MS
        W2MS
        W5MS
        W10MS
        W20MS
        W30MS
        W40MS
        W50MS
        W100MS
        W200MS
        W500MS
        W1S
        W2S
        W5S
        W10S
        W20S
        W60S
    """

    ZERO = 0
    W1MS = 1
    W2MS = 2
    W5MS = 3
    W10MS = 4
    W20MS = 5
    W30MS = 6
    W40MS = 7
    W50MS = 8
    W100MS = 9
    W200MS = 10
    W500MS = 11
    W1S = 12
    W2S = 13
    W5S = 14
    W10S = 15
    W20S = 16
    W60S = 17


@dataclasses.dataclass
class RICSubsequentAction:
    """The subsequent action to take once the action is complete.

    Args:
        type: The subsequent action type.
        time_to_wait: Time to wait before performing the subsequent action.
    """

    type: RICSubsequentActionType
    time_to_wait: RICTimeToWait


@dataclasses.dataclass
class RICAction:
    """An action to be taken in a :meth:`~.E2Client.subscribe` request.

    Args:
        id: The RIC action ID.
        type: The action type to be executed.
        subsequent_action: The subsequent action to take once the action is complete.
        definition: Parameters used when executing a report, insert, or policy service.
    """

    id: int
    type: RICActionType
    subsequent_action: Optional[RICSubsequentAction] = None
    definition: Optional[bytes] = None

    def __post_init__(self) -> None:
        if self.type == RICActionType.INSERT and self.subsequent_action is None:
            raise ValueError(
                "subsequent_action must be present when RICActionType is set to 'INSERT'"
            )


@dataclasses.dataclass
class RanFunction:
    """The function corresponding to a specific E2 service model.

    Args:
        id: The RAN function ID.
        oid: The RAN function object ID.
        definition: An octet string corresponding to a specific E2 service model.
        revision: The RAN function revision.
    """

    id: str
    oid: str
    definition: bytes
    revision: Optional[int] = None


@dataclasses.dataclass
class E2Node:
    """A logical node terminating E2 interface.

    Args:
        id: The E2 node ID.
        ran_functions: The list of RAN functions supported by this E2 node.
    """

    id: str
    ran_functions: List[RanFunction]
