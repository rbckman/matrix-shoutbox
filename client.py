import asyncio
import sys

async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888, loop=loop)
    print('Send: %r' % message)
    writer.write(message.encode())
    data = await reader.read(1000)
    print('Received: %r' % data.decode())
    print('Close the socket')
    writer.close()

message = sys.argv[1]
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()
