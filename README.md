## 安装

```
sudo apt install build-essential portaudio19-dev ffmpeg
pip install -r requirements.txt
pip install .
```

## 架构简介

- 语音识别程序主要包含两部分，一部分是语音识别模型，另一部分是麦克风录音模块。
- `medical_src.microphone`模块负责从麦克风中读取音频数据，然后将音频数据通过websocket传递给语音识别模型进行识别，音频格式为bytes。
- `medical_src.asr_server`是语音识别模型的websocket服务端，负责接收音频数据，进行识别，然后将识别结果返回给客户端，识别结果格式为str。
- 模型存放位置为`~/.cache/modelscope/hub/`，语音识别服务运行前，会检查模型是否存在，如果不存在会自动下载模型。

## Examples

### example1 独立运行服务端和客户端

``` shell
python bin/example1/asr_server.py
# 服务端启动需要6-7s，等待服务端启动完成后再启动客户端。
python bin/example1/asr_client.py
``` 

### example2 独立运行服务端、客户端和flask服务端

``` shell
python bin/example2/asr_server.py
# 服务端启动需要6-7s，等待服务端启动完成后再启动客户端。
python bin/example2/asr_client.py
python bin/example2/flask_server.py
``` 

### example3 语音识别客户端嵌入gui

``` shell
python bin/example3/asr_server.py
# 服务端启动需要6-7s，等待服务端启动完成后再启动客户端。
python bin/example3/gui.py
``` 

### example4 同时启动语音识别服务端和gui

``` shell
python bin/example4/gui.py
``` 

## FAQ

Q：为什么启动服务要等待那么久？
A：1. 依赖包funasr导入时间较长 2. 服务端启动需要加载模型，加载模型需要时间。
