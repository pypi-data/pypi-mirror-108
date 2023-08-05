"""
Type annotations for codeguruprofiler service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_codeguruprofiler import CodeGuruProfilerClient
    from mypy_boto3_codeguruprofiler.paginator import (
        ListProfileTimesPaginator,
    )

    client: CodeGuruProfilerClient = boto3.client("codeguruprofiler")

    list_profile_times_paginator: ListProfileTimesPaginator = client.get_paginator("list_profile_times")
    ```
"""
from datetime import datetime
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .literals import AggregationPeriodType, OrderByType
from .type_defs import ListProfileTimesResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListProfileTimesPaginator",)


class ListProfileTimesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.86/reference/services/codeguruprofiler.html#CodeGuruProfiler.Paginator.ListProfileTimes)[Show boto3-stubs documentation](./paginators.md#listprofiletimespaginator)
    """

    def paginate(
        self,
        endTime: datetime,
        period: AggregationPeriodType,
        profilingGroupName: str,
        startTime: datetime,
        orderBy: OrderByType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListProfileTimesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.86/reference/services/codeguruprofiler.html#CodeGuruProfiler.Paginator.ListProfileTimes.paginate)
        [Show boto3-stubs documentation](./paginators.md#listprofiletimespaginator)
        """
