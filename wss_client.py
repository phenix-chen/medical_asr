from medical_asr.microphone import MicroPhoneServer
import requests


def post_text(text: str):
    url = 'http://127.0.0.1:5000/print'
    data = {"text": text}
    response = requests.post(url, data=data)


if __name__ == "__main__":
    print("启动语音识别客户端")
    microphone = MicroPhoneServer()
    microphone.set_callback(post_text)  # 设置回调函数
    microphone.run()
