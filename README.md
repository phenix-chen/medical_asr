## 安装

```
pip install -r requirements.txt
pip install .
```

## Quick Start

``` shell
python bin/gui.py
``` 

## 架构介绍

语音识别程序主要包含两部分，一部分是语音识别模型，另一部分是麦克风录音模块。
microphone.py模块负责从麦克风中读取音频数据，然后将音频数据通过websocket传递给语音识别模型进行识别，音频格式为bytes。
asr_server.py是语音识别模型的websocket服务端，负责接收音频数据，进行识别，然后将识别结果返回给客户端，识别结果格式为str。

## 独立运行服务端和客户端

``` shell
python bin/exampl1/asr_server.py
python bin/exampl1/asr_lient.py
``` 

## 下载模型

模型默认存储在

``` shell
python 
``` 

## flask模式

``` python
python flask_gui.py
```
