import json
from typing import Coroutine


class LanternHandler:
    @classmethod
    async def process_command(cls, command: str, metadata: str | None = None) -> str:
        '''
        Process commands
        '''

        commands = {
            'ON': cls.turn_on,
            'OFF': cls.turn_off,
            'COLOR': cls.switch_color
        }
        function: Coroutine = commands.get(command, None)

        if function is None:
            return "Can't process unknown command"
        try:
            return await function(metadata)
        except Exception:
            return 'An error occurred while processing the command'


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
            return (f'Color switch command must contain'
                    f' desired color in the metadata field.'
                    f' Please try again')
        return f'Lantern color is now {metadata}'


    @classmethod
    async def dispatch(cls, data: str | bytes) -> str:
        '''
        Receive data from client
        '''
        
        if not data:
            return "Provide some non-empty data"
        try:
            message = json.loads(data)
            command = message.get('command')
            metadata = message.get('metadata', None)

            return await cls.process_command(command, metadata)
        except Exception:
            return 'Provide valid json data'
