"""
Type annotations for sagemaker-a2i-runtime service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_sagemaker_a2i_runtime import AugmentedAIRuntimeClient

    client: AugmentedAIRuntimeClient = boto3.client("sagemaker-a2i-runtime")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Type

from botocore.client import ClientMeta

from .literals import SortOrderType
from .paginator import ListHumanLoopsPaginator
from .type_defs import (
    DescribeHumanLoopResponseTypeDef,
    HumanLoopDataAttributesTypeDef,
    HumanLoopInputTypeDef,
    ListHumanLoopsResponseTypeDef,
    StartHumanLoopResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AugmentedAIRuntimeClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class AugmentedAIRuntimeClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can_paginate)
        """

    def delete_human_loop(self, HumanLoopName: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.delete_human_loop)
        [Show boto3-stubs documentation](./client.md#delete_human_loop)
        """

    def describe_human_loop(self, HumanLoopName: str) -> DescribeHumanLoopResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.describe_human_loop)
        [Show boto3-stubs documentation](./client.md#describe_human_loop)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate_presigned_url)
        """

    def list_human_loops(
        self,
        FlowDefinitionArn: str,
        CreationTimeAfter: datetime = None,
        CreationTimeBefore: datetime = None,
        SortOrder: SortOrderType = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ListHumanLoopsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.list_human_loops)
        [Show boto3-stubs documentation](./client.md#list_human_loops)
        """

    def start_human_loop(
        self,
        HumanLoopName: str,
        FlowDefinitionArn: str,
        HumanLoopInput: HumanLoopInputTypeDef,
        DataAttributes: HumanLoopDataAttributesTypeDef = None,
    ) -> StartHumanLoopResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.start_human_loop)
        [Show boto3-stubs documentation](./client.md#start_human_loop)
        """

    def stop_human_loop(self, HumanLoopName: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.stop_human_loop)
        [Show boto3-stubs documentation](./client.md#stop_human_loop)
        """

    def get_paginator(self, operation_name: Literal["list_human_loops"]) -> ListHumanLoopsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Paginator.ListHumanLoops)[Show boto3-stubs documentation](./paginators.md#listhumanloopspaginator)
        """
