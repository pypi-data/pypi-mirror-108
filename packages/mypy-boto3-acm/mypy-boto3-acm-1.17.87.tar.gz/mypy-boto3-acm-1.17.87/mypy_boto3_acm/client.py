"""
Type annotations for acm service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_acm import ACMClient

    client: ACMClient = boto3.client("acm")
    ```
"""
import sys
from typing import IO, Any, Dict, List, Type, Union

from botocore.client import ClientMeta

from .literals import CertificateStatusType, ValidationMethodType
from .paginator import ListCertificatesPaginator
from .type_defs import (
    CertificateOptionsTypeDef,
    DescribeCertificateResponseTypeDef,
    DomainValidationOptionTypeDef,
    ExpiryEventsConfigurationTypeDef,
    ExportCertificateResponseTypeDef,
    FiltersTypeDef,
    GetAccountConfigurationResponseTypeDef,
    GetCertificateResponseTypeDef,
    ImportCertificateResponseTypeDef,
    ListCertificatesResponseTypeDef,
    ListTagsForCertificateResponseTypeDef,
    RequestCertificateResponseTypeDef,
    TagTypeDef,
)
from .waiter import CertificateValidatedWaiter

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ACMClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InvalidArgsException: Type[BotocoreClientError]
    InvalidArnException: Type[BotocoreClientError]
    InvalidDomainValidationOptionsException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    InvalidTagException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    RequestInProgressException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TagPolicyException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ACMClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def add_tags_to_certificate(self, CertificateArn: str, Tags: List["TagTypeDef"]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.add_tags_to_certificate)
        [Show boto3-stubs documentation](./client.md#add_tags_to_certificate)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can_paginate)
        """

    def delete_certificate(self, CertificateArn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.delete_certificate)
        [Show boto3-stubs documentation](./client.md#delete_certificate)
        """

    def describe_certificate(self, CertificateArn: str) -> DescribeCertificateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.describe_certificate)
        [Show boto3-stubs documentation](./client.md#describe_certificate)
        """

    def export_certificate(
        self, CertificateArn: str, Passphrase: Union[bytes, IO[bytes]]
    ) -> ExportCertificateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.export_certificate)
        [Show boto3-stubs documentation](./client.md#export_certificate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate_presigned_url)
        """

    def get_account_configuration(self) -> GetAccountConfigurationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.get_account_configuration)
        [Show boto3-stubs documentation](./client.md#get_account_configuration)
        """

    def get_certificate(self, CertificateArn: str) -> GetCertificateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.get_certificate)
        [Show boto3-stubs documentation](./client.md#get_certificate)
        """

    def import_certificate(
        self,
        Certificate: Union[bytes, IO[bytes]],
        PrivateKey: Union[bytes, IO[bytes]],
        CertificateArn: str = None,
        CertificateChain: Union[bytes, IO[bytes]] = None,
        Tags: List["TagTypeDef"] = None,
    ) -> ImportCertificateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.import_certificate)
        [Show boto3-stubs documentation](./client.md#import_certificate)
        """

    def list_certificates(
        self,
        CertificateStatuses: List[CertificateStatusType] = None,
        Includes: FiltersTypeDef = None,
        NextToken: str = None,
        MaxItems: int = None,
    ) -> ListCertificatesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.list_certificates)
        [Show boto3-stubs documentation](./client.md#list_certificates)
        """

    def list_tags_for_certificate(
        self, CertificateArn: str
    ) -> ListTagsForCertificateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.list_tags_for_certificate)
        [Show boto3-stubs documentation](./client.md#list_tags_for_certificate)
        """

    def put_account_configuration(
        self, IdempotencyToken: str, ExpiryEvents: "ExpiryEventsConfigurationTypeDef" = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.put_account_configuration)
        [Show boto3-stubs documentation](./client.md#put_account_configuration)
        """

    def remove_tags_from_certificate(self, CertificateArn: str, Tags: List["TagTypeDef"]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.remove_tags_from_certificate)
        [Show boto3-stubs documentation](./client.md#remove_tags_from_certificate)
        """

    def renew_certificate(self, CertificateArn: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.renew_certificate)
        [Show boto3-stubs documentation](./client.md#renew_certificate)
        """

    def request_certificate(
        self,
        DomainName: str,
        ValidationMethod: ValidationMethodType = None,
        SubjectAlternativeNames: List[str] = None,
        IdempotencyToken: str = None,
        DomainValidationOptions: List[DomainValidationOptionTypeDef] = None,
        Options: "CertificateOptionsTypeDef" = None,
        CertificateAuthorityArn: str = None,
        Tags: List["TagTypeDef"] = None,
    ) -> RequestCertificateResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.request_certificate)
        [Show boto3-stubs documentation](./client.md#request_certificate)
        """

    def resend_validation_email(
        self, CertificateArn: str, Domain: str, ValidationDomain: str
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.resend_validation_email)
        [Show boto3-stubs documentation](./client.md#resend_validation_email)
        """

    def update_certificate_options(
        self, CertificateArn: str, Options: "CertificateOptionsTypeDef"
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Client.update_certificate_options)
        [Show boto3-stubs documentation](./client.md#update_certificate_options)
        """

    def get_paginator(
        self, operation_name: Literal["list_certificates"]
    ) -> ListCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Paginator.ListCertificates)[Show boto3-stubs documentation](./paginators.md#listcertificatespaginator)
        """

    def get_waiter(
        self, waiter_name: Literal["certificate_validated"]
    ) -> CertificateValidatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/acm.html#ACM.Waiter.certificate_validated)[Show boto3-stubs documentation](./waiters.md#certificatevalidatedwaiter)
        """
