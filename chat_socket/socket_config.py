from socketio import AsyncServer
from socketio import ASGIApp

sio=AsyncServer(cors_allowed_origins='*',async_mode='asgi')
#wrap with ASGI application
socket_app = ASGIApp(sio,socketio_path="/")