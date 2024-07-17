import sys
from PySide6.QtWidgets import QApplication, QLabel, QTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import QThread, Signal
from flask import Flask, request
import threading

# 创建Flask应用
app = Flask(__name__)


# 创建一个类用于处理Flask服务的线程
class FlaskThread(QThread):
    text_received = Signal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        app.run(port=5000)


# 定义一个Flask路由，用于接收文本
@app.route('/print', methods=['POST'])
def receive_text():
    text = request.form['text']
    flask_thread.text_received.emit(text)  # 发出信号，将文本传递给GUI
    return 'Text received'


# 创建PySide GUI应用
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Waiting for text...")
        self.text_box = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_box)
        self.setLayout(layout)

    def update_text(self, text):
        self.text_box.setText(text)


if __name__ == '__main__':
    # 创建Qt应用
    qapp = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()

    # 创建并启动Flask服务的线程
    flask_thread = FlaskThread()
    flask_thread.text_received.connect(widget.update_text)
    flask_thread.start()

    # 启动Qt事件循环
    sys.exit(qapp.exec())
