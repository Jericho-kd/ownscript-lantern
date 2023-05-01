from dataclasses import dataclass, field
from fastapi import APIRouter, WebSocket, WebSocketDisconnect


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
        await websocket.send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            await manager.send_message(data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
