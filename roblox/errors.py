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

__all__ = (
    'Unauthorized',
    'NotFound',
    'UnknownStatus',
    'InternalServerError',
    'WrongDataPassed',
    'GamepassNotForSale',
    'GamepassAlreadyOwned',
    'NotEnoughFunds',
    'GamepassAlreadyRevoked',
    'Forbidden',
    'PendingTransactionAlreadyExists',
)


class RobloxException(BaseException):
    pass


class HTTPException(RobloxException):
    pass


class ClientException(HTTPException):
    pass


class Unauthorized(ClientException):

    def __init__(self):
        super().__init__('Invalid ROBLOSECURITY or no authorization argument passed.')


class NotFound(RobloxException):

    def __init__(self):
        super().__init__('Nothing found.')


class UnknownStatus(HTTPException):

    def __init__(self, status: int):
        super().__init__(f'Unknown status given by the server: `{status}`.')


class InternalServerError(HTTPException):

    def __init__(self):
        super().__init__('Internal error.')


class Forbidden(HTTPException):

    def __init__(self, message: str):
        super().__init__(message)


class WrongDataPassed(RobloxException):

    def __init__(self):
        super().__init__('Content not accepted by the Roblox API.')


class GamepassNotForSale(RobloxException):

    def __init__(self):
        super().__init__('Gamepass is not for sale.')


class GamepassAlreadyOwned(RobloxException):

    def __init__(self):
        super().__init__('Gamepass already owned.')


class NotEnoughFunds(RobloxException):

    def __init__(self):
        super().__init__('Not enough funds.')


class GamepassAlreadyRevoked(RobloxException):

    def __init__(self):
        super().__init__('Gamepass already revoked.')


class PendingTransactionAlreadyExists(RobloxException):

    def __init__(self, *args):
        super().__init__('You have a pending transaction. Please wait 1 minute and try again.')
