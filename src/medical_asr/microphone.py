import asyncio
from typing import Optional

import pyaudio
from websockets.client import connect


class Microphone:

    def __init__(self) -> None:
        super().__init__()
        FORMAT = pyaudio.paInt16  # 2 bytes
        CHANNELS = 1
        RATE = 16000  # hz
        chunk_size = 60 * 10 / 10
        self.CHUNK = int(RATE / 1000 * chunk_size)  # 60ms per chunk

        p = pyaudio.PyAudio()
        self.stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,  # sample rate
            input=True,
            frames_per_buffer=self.CHUNK,  # a buffer is 60ms
        )

    def record(self):
        data = self.stream.read(self.CHUNK)
        return data


class MicroPhoneServer:

    def __init__(self):
        super().__init__()
        self.is_running = True
        self.callback: Optional[callable] = None

    def set_callback(self, hook: callable):
        self.callback = hook

    async def send(self, serve):
        mic = Microphone()
        while True:
            if not self.is_running:
                break
            voice = mic.record()
            await serve.send(voice)
            await asyncio.sleep(0.001)

    async def recv(self, serve):
        while True:
            if not self.is_running:
                break
            message = await serve.recv()
            if message != "":
                print(message)
                if self.callback:
                    self.callback(message)

    async def _run(self):
        async with connect("ws://localhost:8765") as ws:
            task1 = asyncio.create_task(self.send(ws))
            task2 = asyncio.create_task(self.recv(ws))
            await asyncio.gather(task1, task2)

    def run(self):
        try:
            asyncio.run(self._run())
        except asyncio.exceptions.CancelledError:
            print("Reconnecting...")

    def stop(self):
        self.is_running = False
