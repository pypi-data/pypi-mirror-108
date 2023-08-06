"""
Type annotations for ram service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_ram import RAMClient
    from mypy_boto3_ram.paginator import (
        GetResourcePoliciesPaginator,
        GetResourceShareAssociationsPaginator,
        GetResourceShareInvitationsPaginator,
        GetResourceSharesPaginator,
        ListPrincipalsPaginator,
        ListResourcesPaginator,
    )

    client: RAMClient = boto3.client("ram")

    get_resource_policies_paginator: GetResourcePoliciesPaginator = client.get_paginator("get_resource_policies")
    get_resource_share_associations_paginator: GetResourceShareAssociationsPaginator = client.get_paginator("get_resource_share_associations")
    get_resource_share_invitations_paginator: GetResourceShareInvitationsPaginator = client.get_paginator("get_resource_share_invitations")
    get_resource_shares_paginator: GetResourceSharesPaginator = client.get_paginator("get_resource_shares")
    list_principals_paginator: ListPrincipalsPaginator = client.get_paginator("list_principals")
    list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    ResourceOwnerType,
    ResourceShareAssociationStatusType,
    ResourceShareAssociationTypeType,
    ResourceShareStatusType,
)
from .type_defs import (
    GetResourcePoliciesResponseTypeDef,
    GetResourceShareAssociationsResponseTypeDef,
    GetResourceShareInvitationsResponseTypeDef,
    GetResourceSharesResponseTypeDef,
    ListPrincipalsResponseTypeDef,
    ListResourcesResponseTypeDef,
    PaginatorConfigTypeDef,
    TagFilterTypeDef,
)

__all__ = (
    "GetResourcePoliciesPaginator",
    "GetResourceShareAssociationsPaginator",
    "GetResourceShareInvitationsPaginator",
    "GetResourceSharesPaginator",
    "ListPrincipalsPaginator",
    "ListResourcesPaginator",
)


class GetResourcePoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/ram.html#RAM.Paginator.GetResourcePolicies)[Show boto3-stubs documentation](./paginators.md#getresourcepoliciespaginator)
    """

    def paginate(
        self,
        resourceArns: List[str],
        principal: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[GetResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/ram.html#RAM.Paginator.GetResourcePolicies.paginate)
        [Show boto3-stubs documentation](./paginators.md#getresourcepoliciespaginator)
        """


class GetResourceShareAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/ram.html#RAM.Paginator.GetResourceShareAssociations)[Show boto3-stubs documentation](./paginators.md#getresourceshareassociationspaginator)
    """

    def paginate(
        self,
        associationType: ResourceShareAssociationTypeType,
        resourceShareArns: List[str] = None,
        resourceArn: str = None,
        principal: str = None,
        associationStatus: ResourceShareAssociationStatusType = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[GetResourceShareAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/ram.html#RAM.Paginator.GetResourceShareAssociations.paginate)
        [Show boto3-stubs documentation](./paginators.md#getresourceshareassociationspaginator)
        """


class GetResourceShareInvitationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/ram.html#RAM.Paginator.GetResourceShareInvitations)[Show boto3-stubs documentation](./paginators.md#getresourceshareinvitationspaginator)
    """

    def paginate(
        self,
        resourceShareInvitationArns: List[str] = None,
        resourceShareArns: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[GetResourceShareInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/ram.html#RAM.Paginator.GetResourceShareInvitations.paginate)
        [Show boto3-stubs documentation](./paginators.md#getresourceshareinvitationspaginator)
        """


class GetResourceSharesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/ram.html#RAM.Paginator.GetResourceShares)[Show boto3-stubs documentation](./paginators.md#getresourcesharespaginator)
    """

    def paginate(
        self,
        resourceOwner: ResourceOwnerType,
        resourceShareArns: List[str] = None,
        resourceShareStatus: ResourceShareStatusType = None,
        name: str = None,
        tagFilters: List[TagFilterTypeDef] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[GetResourceSharesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/ram.html#RAM.Paginator.GetResourceShares.paginate)
        [Show boto3-stubs documentation](./paginators.md#getresourcesharespaginator)
        """


class ListPrincipalsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/ram.html#RAM.Paginator.ListPrincipals)[Show boto3-stubs documentation](./paginators.md#listprincipalspaginator)
    """

    def paginate(
        self,
        resourceOwner: ResourceOwnerType,
        resourceArn: str = None,
        principals: List[str] = None,
        resourceType: str = None,
        resourceShareArns: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/ram.html#RAM.Paginator.ListPrincipals.paginate)
        [Show boto3-stubs documentation](./paginators.md#listprincipalspaginator)
        """


class ListResourcesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/ram.html#RAM.Paginator.ListResources)[Show boto3-stubs documentation](./paginators.md#listresourcespaginator)
    """

    def paginate(
        self,
        resourceOwner: ResourceOwnerType,
        principal: str = None,
        resourceType: str = None,
        resourceArns: List[str] = None,
        resourceShareArns: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.88/reference/services/ram.html#RAM.Paginator.ListResources.paginate)
        [Show boto3-stubs documentation](./paginators.md#listresourcespaginator)
        """
