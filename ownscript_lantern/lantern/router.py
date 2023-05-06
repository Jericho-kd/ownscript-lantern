from dataclasses import dataclass, field
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ownscript_lantern.lantern_handler import LanternHandler


router = APIRouter(
    prefix="/lantern",
    tags=["Lantern"]
)


@dataclass
class ConnectionManager:
    active_connections: list[WebSocket] = field(default_factory=list)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


manager = ConnectionManager()
lantern = LanternHandler()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            result = await lantern.dispatch(data)
            await manager.send_message(result, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
