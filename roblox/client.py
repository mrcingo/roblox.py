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

from types import TracebackType
from typing import TYPE_CHECKING, Literal, Self, Type, Union, overload

from .http import Client

if TYPE_CHECKING:
    from .abc import Gamepass, PartialUser, User


__all__ = ('Roblox',)


class Roblox:

    def __init__(self, *, authorization=None):
        self._client = Client(authorization=authorization)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Type[BaseException], exc_value: BaseException, traceback: TracebackType) -> None:
        await self._client.close()

    @overload
    async def get_user(self, target: int) -> User:
        pass

    @overload
    async def get_user(self, target: str, *, partial: Literal[True] = ...) -> PartialUser:
        pass

    @overload
    async def get_user(self, target: str, *, partial: Literal[False] = ...) -> User:
        pass

    async def get_user(self, target: Union[str, int], *, partial: bool = True) -> Union[User, PartialUser]:
        if isinstance(target, int):
            return await self._client.get_user_by_id(int(target))

        partial_user = await self._client.get_user_by_name(target)

        if not partial:
            return await self._client.get_user_by_id(partial_user.id)

        return partial_user

    @overload
    async def get_self(self, *, partial: Literal[True] = ...) -> PartialUser:
        pass

    @overload
    async def get_self(self, *, partial: Literal[False] = ...) -> User:
        pass

    async def get_self(self, *, partial: bool = True) -> Union[User, PartialUser]:
        authenticated_user = await self._client.get_authenticated_user()

        if not partial:
            return await self._client.get_user_by_id(authenticated_user.id)

        return authenticated_user

    async def get_gamepass(self, target: int) -> Gamepass:
        return await self._client.get_gamepass_by_id(target)
