import asyncio
import os
from time import sleep

import dotenv

from roblox import Roblox, errors

dotenv.load_dotenv('.env')

AUTHORIZATION = os.environ.get('AUTHORIZATION', None)


async def main():
    assert AUTHORIZATION is not None

    async with Roblox(authorization=AUTHORIZATION) as client:
        try:
            gamepass = await client.get_gamepass(target=215673674)
        except errors.NotFound:
            print('Pass not found')
            return

        try:
            client_user = await client.get_self()
        except errors.Unauthorized:
            print('Incorrect authorization token')
            return

        client_user_owns_gamepass = await gamepass.has_user(client_user.id)

        if client_user_owns_gamepass:
            print('Removing from inventory: ', gamepass.name)
            await gamepass.revoke()

            print('Pass removed, waiting for pending transaction')
            sleep(61)

        print('Purchasing: ', gamepass.name)
        try:
            await gamepass.purchase()
        except errors.NotEnoughFunds:
            print('Not enough balance')


asyncio.run(main())
