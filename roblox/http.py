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

import sys
from types import TracebackType
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Self, Type, Union

import aiohttp

from . import __version__
from .errors import (
    Forbidden,
    GamepassAlreadyOwned,
    GamepassAlreadyRevoked,
    InternalServerError,
    NotEnoughFunds,
    NotFound,
    PendingTransactionAlreadyExists,
    Unauthorized,
    UnknownStatus,
)
from .gamepass import Gamepass, PartialGamepass
from .user import PartialUser, User

if TYPE_CHECKING:
    from . import abc

__all__ = ('Client',)


class Route:

    def __init__(self, method: str, module: str, path: tuple[str, ...]):
        self.method: str = method

        self.module: str = module
        self.path: tuple[str, ...] = path

    def __str__(self):
        return self.url

    @property
    def base(self) -> str:
        # don't include a trailing slash here to avoid double '//' when joining paths
        return f'https://{self.module}.roblox.com'

    @property
    def url(self) -> str:
        return self.base + '/' + '/'.join(self.path)


class Http:

    def __init__(self, *, authorization: Optional[str] = None):
        self.__session: Optional[aiohttp.ClientSession] = aiohttp.ClientSession()
        self.__authorization: Optional[str] = authorization

        if self.__authorization:
            self.__session.headers.update({'Cookie': f'.ROBLOSECURITY={self.__authorization}'})
        self.__session.headers.update({'User-Agent': self.__str__()})

    def __str__(self) -> str:
        return f'RobloxPy (https://github.com/Gwarded/roblox.py {__version__}) Python/{sys.version_info[0]} aiohttp/{aiohttp.__version__}'

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Type[BaseException], exc_value: BaseException, traceback: TracebackType) -> None:
        await self.close()

    async def close(self):
        assert self.__session is not None
        await self.__session.close()
        self.__session = None

    async def request(self, route: Route, *, data: Optional[Union[dict, list]] = None) -> tuple[Any, int]:
        assert self.__session is not None
        async with self.__session.request(
            method=route.method,
            json=data,
            url=route.url,
        ) as response:
            status = response.status

            if status >= 300 and status <= 399:
                raise UnknownStatus(response.status)

            if response.status == 401:
                raise Unauthorized()

            if response.status == 403:
                if response.headers.get('x-csrf-token') is not None:
                    self.__session.headers.add('X-CSRF-TOKEN', response.headers['x-csrf-token'])
                    return await self.request(route=route, data=data)

                payload: Dict[Literal['errors'], List[Dict[Literal['code', 'message'], Union[str, int]]]] = (
                    await response.json()
                )
                error = payload['errors'][0]

                raise Forbidden(str(error['message']))

            if response.status == 404:
                raise NotFound()

            if response.status >= 500:
                raise InternalServerError()

            if response.content_type != 'application/json':
                return await response.text(), response.status

            return await response.json(), response.status


class Client(Http):

    async def get_user_by_name(self, name: str) -> abc.PartialUser:
        payload, _ = await self.request(
            Route(
                'POST',
                'users',
                (
                    'v1',
                    'usernames',
                    'users',
                ),
            ),
            data={'usernames': [name], 'excludeBannedUsers': True},
        )

        if not payload.get('data'):
            raise NotFound()

        return PartialUser(payload.get('data')[0])

    async def get_user_by_id(self, id: int) -> abc.User:
        payload, _ = await self.request(
            Route(
                'GET',
                'users',
                ('v1', 'users', str(id)),
            ),
        )

        return User(self, payload)

    async def get_gamepass_by_id(self, id: int) -> abc.Gamepass:
        payload, _ = await self.request(
            Route(
                'GET',
                'apis',
                ('game-passes', 'v1', 'game-passes', str(id), 'product-info'),
            ),
        )

        return Gamepass(self, payload)

    async def get_user_gamepass_ownership(self, user_id: int, gamepass_id: int) -> bool:
        payload, _ = await self.request(
            Route(
                'GET',
                'inventory',
                ('v1', 'users', str(user_id), 'items', 'GamePass', str(gamepass_id)),
            ),
        )

        if not payload.get('data'):
            return False

        return True

    async def get_user_gamepasses(self, id: int) -> List[abc.PartialGamepass]:
        payload, _ = await self.request(Route('GET', 'apis', ('game-passes', 'v1', 'users', str(id), 'game-passes')))

        gamepasses: List[abc.PartialGamepass] = list()
        for gamepass in payload.get('gamePasses'):
            gamepasses.append(PartialGamepass(self, gamepass))

        return gamepasses

    async def get_authenticated_user(self) -> abc.PartialUser:
        payload, _ = await self.request(Route('GET', 'users', ('v1', 'users', 'authenticated')))

        self._authenticated_user = PartialUser(payload)

        return PartialUser(payload)

    async def purchase_gamepass(self, product_id: int, expected_price: int, expected_seller_id: int) -> None:
        payload, _ = await self.request(
            Route(
                'POST',
                'apis',
                ('game-passes', 'v1', 'game-passes', str(product_id), 'purchase'),
            ),
            data={
                'expectedCurrency': 1,
                'expectedPrice': expected_price,
                'expectedSellerId': expected_seller_id,
            },
        )

        if payload.get('reason') == 'AlreadyOwned':
            raise GamepassAlreadyOwned()

        short_fall_price = payload.get('shortfallPrice')

        if short_fall_price is not None and short_fall_price > 0:
            raise NotEnoughFunds()

        if payload.get('reason') == 'PendingTransactionAlreadyExists':
            raise PendingTransactionAlreadyExists()

    async def revoke_gamepass_ownership(self, id: int, expected_price: int, expected_seller_id: int) -> None:
        payload, _ = await self.request(
            Route('POST', 'apis', ('game-passes', 'v1', 'game-passes', str(id) + ':revokeownership')),
            data={
                'expectedCurrency': 1,
                'expectedPrice': expected_price,
                'expectedSellerId': expected_seller_id,
            },
        )

        if not isinstance(payload, str) and payload.get('errorCode') == 'PassAlreadyRevoked':
            raise GamepassAlreadyRevoked()
