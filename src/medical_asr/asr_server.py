import asyncio
from multiprocessing import Queue
from typing import Optional

from websockets.server import serve

from medical_asr.model import SeacoASRModel


def main(queue: Optional[Queue] = None):
    model = SeacoASRModel()

    async def echo(websocket):
        async for message in websocket:
            if not isinstance(message, str):
                text = model.recognize(message)
                await websocket.send(text)

    async def run():
        async with serve(echo, "localhost", 8765):
            await asyncio.Future()

    if queue:
        queue.put(1)
    asyncio.run(run())
