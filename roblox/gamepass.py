"""
MIT License

Copyright (c) 2025 Gwarded

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal, Optional, Union, overload

from . import abc
from .user import Creator

if TYPE_CHECKING:
    from .http import Connection
    from .types import Gamepass as GamepassPayload
    from .types import PartialGamepass as PartialGamepassPayload

    User = Union[abc.User, abc.PartialUser]

__all__ = ('Gamepass',)


class PartialGamepass:
    __slots__ = (
        'connection',
        'data',
        'id',
        'asset_id',
        'name',
        'description',
        'is_for_sale',
        'price_in_robux',
    )

    if TYPE_CHECKING:
        connection: Connection

        data: PartialGamepassPayload

        asset_id: int
        name: str
        description: str
        price_in_robux: Optional[int]
        is_for_sale: bool

    def __init__(self, connection: Connection, data: PartialGamepassPayload):
        self.connection = connection

        self.data = data

        self.id = data.get('gamePassId')
        self.asset_id = data.get('iconAssetId')
        self.name = data.get('name')
        self.description = data.get('description')
        self.price_in_robux = data.get('price')
        self.is_for_sale = data.get('isForSale')

    def __str__(self) -> str:
        return f'{self.name}'

    @property
    def creator(self) -> abc.Creator:
        return Creator(self.data.get('creator'))


class Gamepass:
    __slots__ = (
        'connection',
        'data',
        'id',
        'target_id',
        'product_type',
        'asset_id',
        'product_id',
        'name',
        'description',
        'asset_type_id',
        'icon_image_asset_id',
        'price_in_robux',
        'price_in_tickets',
        'sales',
        'is_new',
        'is_for_sale',
        'is_public_domain',
        'is_limited',
        'is_limited_unique',
        'remaining',
        'minimum_membership_level',
    )

    if TYPE_CHECKING:
        connection: Connection

        data: GamepassPayload

        target_id: int
        product_type: str
        asset_id: int
        product_id: int
        name: str
        description: str
        asset_type_id: int
        icon_image_asset_id: int
        price_in_robux: Optional[int]
        price_in_tickets: Optional[int]
        sales: int
        is_new: bool
        is_for_sale: bool
        is_public_domain: bool
        is_limited: bool
        is_limited_unique: bool
        remaining: Optional[int]
        minimum_membership_level: int

    def __init__(self, connection: Connection, data: GamepassPayload):
        self.connection = connection

        self.data = data

        self.id = data.get('TargetId')
        self.product_type = data.get('ProductType')
        self.asset_id = data.get('AssetId')
        self.product_id = data.get('ProductId')
        self.name = data.get('Name')
        self.description = data.get('Description')
        self.asset_type_id = data.get('AssetTypeId')
        self.icon_image_asset_id = data.get('IconImageAssetId')
        self.price_in_robux = data.get('PriceInRobux')
        self.price_in_tickets = data.get('PriceInTickets')
        self.sales = data.get('Sales')
        self.is_new = data.get('IsNew')
        self.is_for_sale = data.get('IsForSale')
        self.is_public_domain = data.get('IsPublicDomain')
        self.is_limited = data.get('IsLimited')
        self.is_limited_unique = data.get('IsLimitedUnique')
        self.remaining = data.get('Remaining')
        self.minimum_membership_level = data.get('MinimumMembershipLevel')

    def __str__(self) -> str:
        return f'{self.name}'

    @property
    def created(self) -> datetime:
        return datetime.fromisoformat(self.data.get('Created').replace('Z', '+00:00'))

    @property
    def updated(self) -> datetime:
        return datetime.fromisoformat(self.data.get('Updated').replace('Z', '+00:00'))

    @overload
    async def creator(self, *, partial: Literal[True] = ...) -> abc.Creator:
        pass

    @overload
    async def creator(self, *, partial: Literal[False] = ...) -> abc.User:
        pass

    async def creator(self, *, partial: bool = True) -> Union[abc.User, abc.Creator]:
        creator_payload = self.data.get('Creator')

        assert creator_payload['CreatorType'] == 'User'

        if partial is True:
            return Creator(creator_payload)
        else:
            return await self.connection.get_user_by_id(creator_payload['Id'])

    async def purchase(self) -> None:
        assert self.price_in_robux is not None

        expected_seller = await self.creator()

        await self.connection.purchase_gamepass(self.product_id, self.price_in_robux, expected_seller.id)

    async def revoke(self) -> None:
        assert self.price_in_robux is not None

        expected_seller = await self.creator()

        await self.connection.revoke_gamepass_ownership(self.id, self.price_in_robux, expected_seller.id)

    async def has_user(self, target: Union[abc.User, abc.PartialUser, abc.Creator, int]) -> bool:
        user_id: Optional[int] = None

        if isinstance(target, abc.Object):
            user_id = target.id

        elif isinstance(target, int):
            user_id = target

        assert user_id is not None

        return await self.connection.get_user_gamepass_ownership(user_id, self.id)
