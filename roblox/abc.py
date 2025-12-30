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
from typing import TYPE_CHECKING, Literal, Optional, Protocol, Union, overload, runtime_checkable

if TYPE_CHECKING:
    from roblox.types import CreatorType


__all__ = ('Object', 'PartialUser', 'User', 'Gamepass', 'PartialGamepass')


@runtime_checkable
class Object(Protocol):
    id: int


@runtime_checkable
class PartialUser(Object, Protocol):
    display_name: str
    has_verified_badge: Optional[bool]
    id: int
    name: str


@runtime_checkable
class User(Object, Protocol):
    description: str
    display_name: str
    external_app_display_name: Optional[str]
    has_verified_badge: bool
    id: int
    is_banned: bool
    name: str

    @property
    def created(self) -> datetime:
        raise NotImplementedError


@runtime_checkable
class Creator(Object, Protocol):
    name: str
    creator_type: CreatorType
    creator_target_id: Optional[int]


@runtime_checkable
class PartialGamepass(Object, Protocol):
    asset_id: int
    name: str
    description: str
    is_for_sale: bool
    price_in_robux: Optional[int]

    @property
    def creator(self) -> Creator:
        raise NotImplementedError


@runtime_checkable
class Gamepass(Object, Protocol):
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

    @property
    def created(self) -> datetime:
        raise NotImplementedError

    @property
    def updated(self) -> datetime:
        raise NotImplementedError

    @overload
    async def creator(self, *, partial: Literal[True] = ...) -> Creator:
        pass

    @overload
    async def creator(self, *, partial: Literal[False] = ...) -> User:
        pass

    async def creator(self, *, partial: bool = True) -> Union[User, Creator]:
        raise NotImplementedError

    async def purchase(self) -> None:
        raise NotImplementedError

    async def revoke(self) -> None:
        raise NotImplementedError

    async def has_user(self, target: Union[User, PartialUser, int]) -> bool:
        raise NotImplementedError
