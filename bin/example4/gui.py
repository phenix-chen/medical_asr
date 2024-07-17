import os
import subprocess
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

        self.label = QLabel("Waiting for speech...")
        self.text_box = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_box)
        self.setLayout(layout)
        self._init_servers()

    def _init_servers(self):
        # 创建并启动语音识别服务进程
        asr_path = os.path.join(os.path.dirname(__file__), 'asr_server.py')
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        self.asr_process = subprocess.Popen(['python', asr_path], stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, env=env)

        # 不断读取ASR服务进程的输出，直到服务启动或进程结束
        while True:
            # 根据操作系统类型选择合适的编码方式读取进程输出
            if sys.platform == "win32":
                output = self.asr_process.stdout.readline().decode(encoding="gbk")
            else:
                output = self.asr_process.stdout.readline().decode()

            # 打印ASR服务的输出信息
            print(output)

            # 检查ASR服务进程是否已结束
            if self.asr_process.poll() is not None:
                break

            # 当输出中包含"模型加载完毕"时，认为ASR服务已启动完成，退出循环
            if output and "模型加载完毕" in output:
                break

        # 创建并启动麦克风的线程
        self.mic_thread = MicroPhoneThread()
        self.mic_thread.start()
        self.mic_thread.text_received.connect(self.update_text)

    def update_text(self, text):
        print(text)
        self.text_box.setText(text)

    def closeEvent(self, event):
        self.asr_process.terminate()
        self.mic_thread.quit()


if __name__ == '__main__':
    # 创建Qt应用
    qapp = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()

    # 启动Qt事件循环
    sys.exit(qapp.exec())
