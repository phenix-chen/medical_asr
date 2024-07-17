from medical_asr.microphone import MicroPhoneServer


def callback(text: str):
    print("识别结果：", text)


if __name__ == "__main__":
    print("启动语音识别客户端")
    microphone = MicroPhoneServer()
    microphone.set_callback(callback)  # 设置回调函数
    microphone.run()
