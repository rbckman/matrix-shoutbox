import asyncio
from nio import (AsyncClient, RoomMessageText)
import config

open('msg.txt', 'w').close()

async def message_cb(room, event):
    if room.display_name == config.display_name:
        print("{}: {}".format(room.user_name(event.sender), event.body))
        msg_file = open('msg.txt', 'a')
        msg_file.write(room.user_name(event.sender) + ': ' + event.body + '\n')

async def main():
    client = AsyncClient(config.matrixserver, config.username)
    client.add_event_callback(message_cb, RoomMessageText)

    await client.login(config.password)
    await client.sync_forever(timeout=30000)

asyncio.get_event_loop().run_until_complete(main())
