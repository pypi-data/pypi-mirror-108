"""
Type annotations for nimble service client paginators.

[Open documentation](./paginators.md)

Usage::

    ```python
    import boto3

    from mypy_boto3_nimble import NimbleStudioClient
    from mypy_boto3_nimble.paginator import (
        ListEulaAcceptancesPaginator,
        ListEulasPaginator,
        ListLaunchProfileMembersPaginator,
        ListLaunchProfilesPaginator,
        ListStreamingImagesPaginator,
        ListStreamingSessionsPaginator,
        ListStudioComponentsPaginator,
        ListStudioMembersPaginator,
        ListStudiosPaginator,
    )

    client: NimbleStudioClient = boto3.client("nimble")

    list_eula_acceptances_paginator: ListEulaAcceptancesPaginator = client.get_paginator("list_eula_acceptances")
    list_eulas_paginator: ListEulasPaginator = client.get_paginator("list_eulas")
    list_launch_profile_members_paginator: ListLaunchProfileMembersPaginator = client.get_paginator("list_launch_profile_members")
    list_launch_profiles_paginator: ListLaunchProfilesPaginator = client.get_paginator("list_launch_profiles")
    list_streaming_images_paginator: ListStreamingImagesPaginator = client.get_paginator("list_streaming_images")
    list_streaming_sessions_paginator: ListStreamingSessionsPaginator = client.get_paginator("list_streaming_sessions")
    list_studio_components_paginator: ListStudioComponentsPaginator = client.get_paginator("list_studio_components")
    list_studio_members_paginator: ListStudioMembersPaginator = client.get_paginator("list_studio_members")
    list_studios_paginator: ListStudiosPaginator = client.get_paginator("list_studios")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListEulaAcceptancesResponseTypeDef,
    ListEulasResponseTypeDef,
    ListLaunchProfileMembersResponseTypeDef,
    ListLaunchProfilesResponseTypeDef,
    ListStreamingImagesResponseTypeDef,
    ListStreamingSessionsResponseTypeDef,
    ListStudioComponentsResponseTypeDef,
    ListStudioMembersResponseTypeDef,
    ListStudiosResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListEulaAcceptancesPaginator",
    "ListEulasPaginator",
    "ListLaunchProfileMembersPaginator",
    "ListLaunchProfilesPaginator",
    "ListStreamingImagesPaginator",
    "ListStreamingSessionsPaginator",
    "ListStudioComponentsPaginator",
    "ListStudioMembersPaginator",
    "ListStudiosPaginator",
)


class ListEulaAcceptancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListEulaAcceptances)[Show boto3-stubs documentation](./paginators.md#listeulaacceptancespaginator)
    """

    def paginate(
        self,
        studioId: str,
        eulaIds: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListEulaAcceptancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListEulaAcceptances.paginate)
        [Show boto3-stubs documentation](./paginators.md#listeulaacceptancespaginator)
        """


class ListEulasPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListEulas)[Show boto3-stubs documentation](./paginators.md#listeulaspaginator)
    """

    def paginate(
        self, eulaIds: List[str] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListEulasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListEulas.paginate)
        [Show boto3-stubs documentation](./paginators.md#listeulaspaginator)
        """


class ListLaunchProfileMembersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListLaunchProfileMembers)[Show boto3-stubs documentation](./paginators.md#listlaunchprofilememberspaginator)
    """

    def paginate(
        self, launchProfileId: str, studioId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListLaunchProfileMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListLaunchProfileMembers.paginate)
        [Show boto3-stubs documentation](./paginators.md#listlaunchprofilememberspaginator)
        """


class ListLaunchProfilesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListLaunchProfiles)[Show boto3-stubs documentation](./paginators.md#listlaunchprofilespaginator)
    """

    def paginate(
        self,
        studioId: str,
        principalId: str = None,
        states: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListLaunchProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListLaunchProfiles.paginate)
        [Show boto3-stubs documentation](./paginators.md#listlaunchprofilespaginator)
        """


class ListStreamingImagesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListStreamingImages)[Show boto3-stubs documentation](./paginators.md#liststreamingimagespaginator)
    """

    def paginate(
        self, studioId: str, owner: str = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListStreamingImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListStreamingImages.paginate)
        [Show boto3-stubs documentation](./paginators.md#liststreamingimagespaginator)
        """


class ListStreamingSessionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListStreamingSessions)[Show boto3-stubs documentation](./paginators.md#liststreamingsessionspaginator)
    """

    def paginate(
        self,
        studioId: str,
        createdBy: str = None,
        sessionIds: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListStreamingSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListStreamingSessions.paginate)
        [Show boto3-stubs documentation](./paginators.md#liststreamingsessionspaginator)
        """


class ListStudioComponentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListStudioComponents)[Show boto3-stubs documentation](./paginators.md#liststudiocomponentspaginator)
    """

    def paginate(
        self,
        studioId: str,
        states: List[str] = None,
        types: List[str] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListStudioComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListStudioComponents.paginate)
        [Show boto3-stubs documentation](./paginators.md#liststudiocomponentspaginator)
        """


class ListStudioMembersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListStudioMembers)[Show boto3-stubs documentation](./paginators.md#liststudiomemberspaginator)
    """

    def paginate(
        self, studioId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListStudioMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListStudioMembers.paginate)
        [Show boto3-stubs documentation](./paginators.md#liststudiomemberspaginator)
        """


class ListStudiosPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListStudios)[Show boto3-stubs documentation](./paginators.md#liststudiospaginator)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListStudiosResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.87/reference/services/nimble.html#NimbleStudio.Paginator.ListStudios.paginate)
        [Show boto3-stubs documentation](./paginators.md#liststudiospaginator)
        """
