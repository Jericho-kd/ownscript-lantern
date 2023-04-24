import asyncio
import json
from dataclasses import dataclass, field


@dataclass
class Lantern:
    host: str = field(default='127.0.0.1', repr=True)
    port: int = field(default=9999, repr=True)
    color: str = field(default='White', repr=True)


    async def send_message(self, writer: asyncio.StreamWriter, message: str) -> None:
        '''
        Method for sending messages to client
        '''

        writer.write(message.encode())
        await writer.drain()


    async def process_command(self, writer: asyncio.StreamWriter,
                              command: str, metadata: str | None = None) -> None:
        '''
        Command processing method
        '''

        if command == 'ON':
            await self.send_message(writer, 'Lantern is ON\n')
        elif command == 'OFF':
            await self.send_message(writer, 'Lantern is OFF\n')
           
            writer.close() # close connection after lantern is OFF
            await writer.wait_closed()
        elif command == 'COLOR':
            self.color = metadata
            await self.send_message(writer, f'Lantern color now is {self.color}\n')
        else:
            await self.send_message(writer, "Can't process unknown command\n")


    async def run(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        '''
        Method for receiving data from client
        '''
        
        await self.send_message(writer, "Please provide data in following format {\"command\":\"your command\", \"metadata\": \"your metadata\"}\n")

        while True:         
            data = await reader.readline()
            if not data:
                break
            try:
                message = json.loads(data.decode())
                command = message.get('command')
                metadata = message.get('metadata')
                await self.process_command(writer, command, metadata)
            except Exception as e:
                await self.send_message(writer, 'Provide some valid data\n')
                print(f'Exception: {e}')


async def main():
    lantern = Lantern()
    server = await asyncio.start_server(lantern.run, lantern.host, lantern.port)

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
