# socketio_instance.py
from fastapi_socketio import SocketManager
from fastapi import FastAPI
from xact.utils.log import logger

# Initialize FastAPI app and Socket.IO manager
app = FastAPI()
socket_manager = SocketManager(app=app, cors_allowed_origins="*")



async def emit_agent(channel, content, log=True):
    """Emit a message to a Socket.IO channel with logging."""
    try:
        await socket_manager.emit(channel, content)
        if log:
            logger.info(f"SOCKET {channel} MESSAGE: {content}")
        return True
    except Exception as e:
        logger.error(f"SOCKET {channel} ERROR: {str(e)}")
        return False
