"""
:copyright: (c) 2025-present MrCingo
:license: MIT, see LICENSE for more details.
"""

__title__ = 'roblox.py'
__author__ = 'Gwarded'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015-present Gwarded'
__version__ = '1.0.0a'


from . import abc as abc
from .client import Roblox
from .errors import (
    Forbidden,
    InternalServerError,
    NotFound,
    PendingTransactionAlreadyExists,
    Unauthorized,
    UnknownStatus,
    WrongDataPassed,
)
from .gamepass import Gamepass, PartialGamepass
from .user import PartialUser, User

__all__ = (
    'Roblox',
    'Unauthorized',
    'NotFound',
    'UnknownStatus',
    'InternalServerError',
    'WrongDataPassed',
    'Gamepass',
    'PartialUser',
    'User',
    'PartialGamepass',
    'Forbidden',
    'PendingTransactionAlreadyExists',
)
