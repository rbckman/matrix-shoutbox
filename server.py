import asyncio
from nio import AsyncClient
import config

async def handle_echo(reader, writer):
    client = AsyncClient(config.matrixserver, config.username)
    await client.login(config.password)

    data = await reader.read(512)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))
    writer.write(data)
    await writer.drain()
    print("Send: %r" % message)
    print("Close the client socket")
    writer.close()
    print('sending msg to matrix')
    await client.room_send(
        room_id=config.room_id,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": message
        }
    )
    await client.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
