# from faster_whisper import WhisperModel
from aiohttp import web
import socketio
from client_manager import ClientManager
import logging
import threading
import asyncio
from urllib.parse import parse_qs
from config import PARAMETERS
import uvicorn
from huggingface_hub import login

# Configure logging settings
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.getLogger("torch.distributed.nn.jit.instantiator").setLevel(logging.WARNING)
logging.getLogger("speechbrain.pretrained.fetching").setLevel(logging.WARNING)
logging.getLogger("speechbrain.utils.parameter_transfer").setLevel(logging.WARNING)


# change to env variable
login('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')


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
app = socketio.ASGIApp(sio)
# app = web.Application()
# sio.attach(app)

client_manager = ClientManager()


@sio.on("connect")
async def handle_connect(sid, environ):
    logging.info("Client connected, initializing stream...")
    query_string = environ["QUERY_STRING"]
    query_params = parse_qs(query_string)
    config = {}
    for parameter in PARAMETERS:
        current_parameter = query_params.get(parameter)
        if current_parameter:
            config[parameter] = current_parameter[0]
    logging.info(f"Stream configuration received: {config}")
    await client_manager.start_stream(sid=sid, sio=sio, config=config)


@sio.on("disconnect")
async def handle_disconnect(sid):
    logging.info("Disconnection detected")
    threading.Thread(target=client_manager.disconnect_from_stream, args=(sid,)).start()


@sio.on("stopWhispering")
async def handle_stream_end(sid):
    logging.info("Received stop stream request")
    threading.Thread(target=asyncio.run, args=(client_manager.end_stream(sid),)).start()


@sio.on("audioChunk")
async def handle_chunk(sid, chunk):
    logging.debug("New chunk arrived")
    client_manager.receive_chunk(sid, chunk)

@sio.on("send")
async def send():
    pass


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
