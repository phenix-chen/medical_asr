import logging
from multiprocessing import Event, Process

import requests

from medical_asr.asr_server import AsrServer
from medical_asr.microphone import MicroPhoneServer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def post_text(text: str):
    logger.info(f"识别结果：{text}")
    url = 'http://127.0.0.1:5000/print'
    data = {"text": text}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        logging.error(f"文本发送失败：{text}")


class AsrProcess(Process):
    def __init__(self, event: Event):
        super().__init__()
        self.event = event

    def run(self):
        asr_server = AsrServer()  # 加载模型，需要6-7s
        self.event.set()
        asr_server.start()  # 通过 asyncio 运行服务


if __name__ == "__main__":
    print("启动语音识别服务")
    event = Event()
    asr_process = AsrProcess(event)
    asr_process.start()
    event.wait()
    print("语音识别服务启动成功")

    print("启动语音识别客户端")
    microphone = MicroPhoneServer()
    microphone.set_callback(post_text)  # 设置回调函数
    microphone.run()
    print("语音识别客户端启动成功")
