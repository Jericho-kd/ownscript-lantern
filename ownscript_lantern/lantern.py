import asyncio
import json
from dataclasses import dataclass, field
from typing import Coroutine


class LanternHandler:
    async def send_message(self, writer: asyncio.StreamWriter, message: str) -> None:
        '''Method for sending messages to client'''

        writer.write(message.encode())
        await writer.drain()


    async def process_command(self, writer: asyncio.StreamWriter,
                              command: str, metadata: str | None = None) -> None:
        '''
        Process commands
        '''
        commands = {
            'ON': self.turn_on,
            'OFF': self.turn_off,
            'COLOR': self.switch_color,
            'END': self.end_session
        }
        function: Coroutine = commands.get(command, None)

        if function is None:
            await self.send_message(writer, "Can't process unknown command\n")
        try:
            await function(writer, metadata)
        except Exception as error:
            await self.send_message(writer, 'An error occurred while processing the command\n')
            print(f'Error has occurred: {error}')


    async def turn_on(self, writer: asyncio.StreamWriter, metadata: str | None = None):
        '''
        Turn on lantern
        '''
        await self.send_message(writer, 'Lantern turned ON\n')


    async def turn_off(self, writer: asyncio.StreamWriter, metadata: str | None = None):
        '''
        Turn off lantern
        '''
        await self.send_message(writer, 'Lantern turned OFF\n')


    async def switch_color(self, writer: asyncio.StreamWriter, metadata: str):
        '''
        Switch lantern color
        '''
        if not metadata:
            await self.send_message(writer, f'Color switch command must contain'
                                    f' desired color in the metadata field.'
                                    f' Please try again.\n')
            return
        await self.send_message(writer, f'Lantern color is now {metadata}\n')


    async def end_session(self, writer: asyncio.StreamWriter, metadata: str | None = None):
        '''
        Disconnect from server
        '''
        await self.send_message(writer, "You're disconnected from server\n")
        writer.close()
        await writer.wait_closed()


    async def dispatch(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        '''
        Receive data from client
        '''
        
        await self.send_message(writer, "Please provide data in the following format"
                                " {\"command\":\"your command\", \"metadata\": \"your metadata\"}.\n"
                                "Field 'metadata' is optional (only use to switch lantern colors).\n")

        while True:         
            data = await reader.readline()
            if not data:
                break
            try:
                message = json.loads(data.decode())
                command = message.get('command')
                metadata = message.get('metadata', None)
                await self.process_command(writer, command, metadata)
            except Exception as e:
                await self.send_message(writer, 'Provide some valid data\n')
                print(f'Exception: {e}')


async def run_server(host: str = '0.0.0.0', port: int = 9999):
    assert 1 < port <= 65535, 'Port must be in range 1-65535'
    lantern = LanternHandler()
    server = await asyncio.start_server(lantern.dispatch, host, port)

    async with server:
        await server.serve_forever()
