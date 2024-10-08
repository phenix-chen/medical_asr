import os
import sys
from multiprocessing import Event, Process

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QApplication, QLabel, QTextEdit, QVBoxLayout, QWidget

from medical_asr.asr_server import AsrServer
from medical_asr.microphone import MicroPhoneServer


class MicroPhoneThread(QThread):
    text_received = Signal(str)

    def __init__(self):
        super().__init__()
        self.mic = MicroPhoneServer()

    def run(self):
        self.mic.set_callback(self.text_received.emit)
        self.mic.run()

    def quit(self):
        self.mic.stop()


class AsrProcess(Process):

    def __init__(self, event: Event):
        super().__init__()
        self.event = event

    def run(self):
        # 设置热词文件路径
        hotword_file = os.path.join(os.path.dirname(__file__), "hotword.txt")
        asr_server = AsrServer(hotword_file)  # 加载模型，需要6-7s
        self.event.set()  # 通知客户端可以启动了
        asr_server.start()  # 通过 asyncio 运行服务


# 创建PySide GUI应用
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Waiting for speech...")
        self.text_box = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_box)
        self.setLayout(layout)
        self._init_servers()

    def _init_servers(self):
        # 创建并启动语音识别的进程
        print("启动语音识别服务")
        event = Event()
        self.asr_process = AsrProcess(event)
        self.asr_process.start()
        event.wait()
        print("语音识别服务启动成功")

        # 创建并启动麦克风的线程
        self.mic_thread = MicroPhoneThread()
        self.mic_thread.start()
        self.mic_thread.text_received.connect(self.update_text)

    def update_text(self, text):
        print(text)
        self.text_box.setText(text)

    def closeEvent(self, event):
        self.asr_process.terminate()
        self.asr_process.join()
        self.mic_thread.quit()


if __name__ == '__main__':
    # 创建Qt应用
    qapp = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()

    # 启动Qt事件循环
    sys.exit(qapp.exec())
