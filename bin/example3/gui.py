import os
import sys

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QApplication, QLabel, QTextEdit, QVBoxLayout, QWidget

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


# 创建PySide GUI应用
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        path = os.path.dirname(__file__)
        hotword_file = os.path.join(path, "hotword.txt")
        with open(hotword_file, "r", encoding="utf-8") as f:
            hotword = f.readlines()
        hotwords = "".join(hotword)

        self.label = QLabel("Waiting for speech...")
        self.text_box = QTextEdit()
        self.text_box.setText(hotwords)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_box)
        self.setLayout(layout)
        self._init_servers()

    def _init_servers(self):
        # 创建并启动麦克风的线程
        self.mic_thread = MicroPhoneThread()
        self.mic_thread.start()
        self.mic_thread.text_received.connect(self.update_text)

    def update_text(self, text):
        print(text)
        self.text_box.setText(text)

    def closeEvent(self, event):
        self.mic_thread.quit()


if __name__ == '__main__':
    # 创建Qt应用
    qapp = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()

    # 启动Qt事件循环
    sys.exit(qapp.exec())
