import asyncio
from typing import Optional

from websockets.server import serve

from medical_asr.model import SeacoASRModel


class AsrServer:
    def __init__(self, hotword_file: Optional[str] = None, model_dir: Optional[str] = None):
        self.model = SeacoASRModel(hotword_file=hotword_file, model_dir=model_dir)

    async def process_audio(self, websocket):
        async for message in websocket:
            if isinstance(message, bytes):
                text = self.model.recognize(message)
                await websocket.send(text)

    async def run(self):
        async with serve(self.process_audio, "localhost", 8765):
            await asyncio.Future()

    def start(self):
        asyncio.run(self.run())
