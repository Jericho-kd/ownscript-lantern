import asyncio
import json
from typing import Coroutine


class LanternHandler:
    @classmethod
    async def send_message(cls, message: str) -> None:
        '''Method for sending messages to client'''

        print(message)


    @classmethod
    async def process_command(cls, writer: asyncio.StreamWriter,
                              command: str, metadata: str | None = None) -> str:
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
            await cls.send_message("Can't process unknown command\n")
        try:
            result: str = await function(metadata)
            return result
        except Exception as error:
            await cls.send_message('An error occurred while processing the command\n')
            print(f'Error has occurred: {error}')

    @classmethod
    async def turn_on(cls, metadata: str | None = None) -> str:
        '''
        Turn on lantern
        '''
        return 'Lantern turned ON'


    @classmethod
    async def turn_off(cls, metadata: str | None = None) -> str:
        '''
        Turn off lantern
        '''
        return 'Lantern turned OFF'


    @classmethod
    async def switch_color(cls, metadata: str) -> str:
        '''
        Switch lantern color
        '''
        if not metadata:
            await cls.send_message(f'Color switch command must contain'
                                    f' desired color in the metadata field.'
                                    f' Please try again.\n')
        return f'Lantern color is now {metadata}'


    @classmethod
    async def end_session(cls, metadata: str | None = None):
        '''
        Disconnect from server
        '''
        return "You're disconnected from server"


    @classmethod
    async def dispatch(cls, data: str | bytes) -> str:
        '''
        Receive data from client
        '''
        
        if not data:
            return "Provide some data"
        try:
            message = json.loads(data)
            command = message.get('command')
            metadata = message.get('metadata', None)
            return await cls.process_command(command, metadata)
        except Exception as e:
            await cls.send_message('Provide some valid data\n')
            print(f'Exception: {e}')
