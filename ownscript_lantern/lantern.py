import asyncio
import json
from dataclasses import dataclass, field


@dataclass
class Lantern:
    host: str = field(default='127.0.0.1', repr=True)
    port: str = field(default='9999', repr=True)
    color: str = field(default='White', repr=True)
    reader: asyncio.StreamReader | None  = field(default=None, repr=False)
    writer: asyncio.StreamWriter | None = field(default=None, repr=False)


    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(host=self.host, port=self.port)


    async def send_command(self, command: str, metadata: str | None = None) -> None:
        data = {
            'command': command,
            'metadata': metadata
        }

        message = json.dumps(data).encode()
        self.writer.write(message)
        await self.writer.drain()
