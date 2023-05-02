import asyncio
import json
from typing import Coroutine


class LanternHandler:
    @classmethod
    async def send_message(cls, writer: asyncio.StreamWriter, message: str) -> None:
        '''Method for sending messages to client'''

        writer.write(message.encode())
        await writer.drain()


    @classmethod
    async def process_command(cls, writer: asyncio.StreamWriter,
                              command: str, metadata: str | None = None) -> None:
        '''
        Process commands
        '''
        commands = {
            'ON': cls.turn_on,
            'OFF': cls.turn_off,
            'COLOR': cls.switch_color,
            'END': cls.end_session
        }
        function: Coroutine = commands.get(command, None)

        if function is None:
            await cls.send_message(writer, "Can't process unknown command\n")
        try:
            await function(writer, metadata)
        except Exception as error:
            await cls.send_message(writer, 'An error occurred while processing the command\n')
            print(f'Error has occurred: {error}')

    @classmethod
    async def turn_on(cls, writer: asyncio.StreamWriter, metadata: str | None = None):
        '''
        Turn on lantern
        '''
        await self.send_message(writer, 'Lantern turned ON\n')


    @classmethod
    async def turn_off(cls, writer: asyncio.StreamWriter, metadata: str | None = None):
        '''
        Turn off lantern
        '''
        await cls.send_message(writer, 'Lantern turned OFF\n')


    @classmethod
    async def switch_color(cls, writer: asyncio.StreamWriter, metadata: str):
        '''
        Switch lantern color
        '''
        if not metadata:
            await cls.send_message(writer, f'Color switch command must contain'
                                    f' desired color in the metadata field.'
                                    f' Please try again.\n')
            return
        await cls.send_message(writer, f'Lantern color is now {metadata}\n')


    @classmethod
    async def end_session(cls, writer: asyncio.StreamWriter, metadata: str | None = None):
        '''
        Disconnect from server
        '''
        await cls.send_message(writer, "You're disconnected from server\n")
        writer.close()
        await writer.wait_closed()


    @classmethod
    async def dispatch(cls, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        '''
        Receive data from client
        '''
        
        await cls.send_message(writer, "Please provide data in the following format"
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
                await cls.process_command(writer, command, metadata)
            except Exception as e:
                await cls.send_message(writer, 'Provide some valid data\n')
                print(f'Exception: {e}')
