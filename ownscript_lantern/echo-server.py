import asyncio

async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 9999)

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client())