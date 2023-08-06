"""
Type annotations for appstream service client waiters.

[Open documentation](./waiters.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_appstream import AppStreamClient
    from mypy_boto3_appstream.waiter import (
        FleetStartedWaiter,
        FleetStoppedWaiter,
    )

    client: AppStreamClient = boto3.client("appstream")

    fleet_started_waiter: FleetStartedWaiter = client.get_waiter("fleet_started")
    fleet_stopped_waiter: FleetStoppedWaiter = client.get_waiter("fleet_stopped")
    ```
"""
from typing import List

from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("FleetStartedWaiter", "FleetStoppedWaiter")


class FleetStartedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/appstream.html#AppStream.Waiter.fleet_started)[Show boto3-stubs documentation](./waiters.md#fleetstartedwaiter)
    """

    def wait(
        self,
        Names: List[str] = None,
        NextToken: str = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/appstream.html#AppStream.Waiter.FleetStartedWaiter)
        [Show boto3-stubs documentation](./waiters.md#fleetstarted)
        """


class FleetStoppedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/appstream.html#AppStream.Waiter.fleet_stopped)[Show boto3-stubs documentation](./waiters.md#fleetstoppedwaiter)
    """

    def wait(
        self,
        Names: List[str] = None,
        NextToken: str = None,
        WaiterConfig: WaiterConfigTypeDef = None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/appstream.html#AppStream.Waiter.FleetStoppedWaiter)
        [Show boto3-stubs documentation](./waiters.md#fleetstopped)
        """
