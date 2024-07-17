from medical_asr.asr_server import AsrServer

if __name__ == "__main__":
    server = AsrServer()
    server.start()
    print("语音识别服务启动成功")
