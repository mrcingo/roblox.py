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
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .http import Connection
    from .types.user import Creator as CreatorPayload
    from .types.user import CreatorType
    from .types.user import PartialUser as PartialUserPayload
    from .types.user import User as UserPayload


__all__ = ('PartialUser', 'User')


class PartialUser:
    __slots__ = (
        'display_name',
        'has_verified_badge',
        'id',
        'name',
    )

    if TYPE_CHECKING:
        display_name: str
        has_verified_badge: Optional[bool]
        id: int
        name: str

    def __init__(self, data: PartialUserPayload):
        self.display_name = data.get('displayName')
        self.has_verified_badge = data.get('hasVerifiedBadge')
        self.id = data.get('id')
        self.name = data.get('name')

    def __str__(self) -> str:
        return f'{self.name}'


class User:
    __slots__ = (
        'connection',
        'data',
        'raw_created',
        'description',
        'display_name',
        'external_app_display_name',
        'has_verified_badge',
        'id',
        'is_banned',
        'name',
    )

    if TYPE_CHECKING:
        connection: Connection

        data: UserPayload

        raw_created_time: str
        description: str
        display_name: str
        external_app_display_name: Optional[str]
        has_verified_badge: Optional[bool]
        id: int
        is_banned: bool
        name: str

    def __init__(self, connection: Connection, data: UserPayload):
        self.connection = connection

        self.data = data

        self.description = data.get('description')
        self.display_name = data.get('displayName')
        self.external_app_display_name = data.get('externalAppDisplayName')
        self.has_verified_badge = data.get('hasVerifiedBadge')
        self.id = data.get('id')
        self.is_banned = data.get('isBanned')
        self.name = data.get('name')

    def __str__(self) -> str:
        return f'{self.name}'

    @property
    def created(self) -> datetime:
        return datetime.fromisoformat(self.data.get('created').replace('Z', '+00:00'))


class Creator:
    __slots__ = ('id', 'name', 'creator_type', 'creator_target_id')

    if TYPE_CHECKING:
        id: int
        name: str
        creator_type: CreatorType
        creator_target_id: Optional[int]

    def __init__(self, data: CreatorPayload):
        self.id = data.get('Id')
        self.name = data.get('Name')
        self.creator_type = data.get('CreatorType')
        self.creator_target_id = data.get('CreatorTargetId')

    def __str__(self) -> str:
        return self.name
