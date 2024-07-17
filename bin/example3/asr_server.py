import os

from medical_asr.asr_server import AsrServer

if __name__ == "__main__":
    # 设置热词文件路径
    hotword_file = os.path.join(os.path.dirname(__file__), "hotword.txt")
    asr_server = AsrServer(hotword_file)  # 加载模型，需要6-7s
    print("模型加载完毕")
    asr_server.start()  # 启动websocket服务
