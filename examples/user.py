import asyncio

from roblox import Roblox
from roblox.abc import User


async def main():

    async with Roblox() as client:
        user: User = await client.get_user(7437887983)

        print('User description: ', user.description)


asyncio.run(main())
