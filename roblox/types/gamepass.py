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

from typing import TYPE_CHECKING, Optional, TypedDict

if TYPE_CHECKING:
    from .user import Creator


__all__ = ('Gamepass', 'PartialGamepass')


class PartialGamepass(TypedDict):
    gamePassId: int
    iconAssetId: int
    name: str
    description: str
    isForSale: bool
    price: Optional[int]
    creator: Creator


class Gamepass(TypedDict):
    TargetId: int
    ProductType: str
    AssetId: int
    ProductId: int
    Name: str
    Description: str
    AssetTypeId: int
    Creator: Creator
    IconImageAssetId: int
    Created: str
    Updated: str
    PriceInRobux: Optional[int]
    PriceInTickets: Optional[int]
    Sales: int
    IsNew: bool
    IsForSale: bool
    IsPublicDomain: bool
    IsLimited: bool
    IsLimitedUnique: bool
    Remaining: Optional[int]
    MinimumMembershipLevel: int
