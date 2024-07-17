## 安装

```
pip install -r requirements.txt
pip install .
```

## 架构介绍

语音识别程序主要包含两部分，一部分是语音识别模型，另一部分是麦克风录音模块。
microphone.py模块负责从麦克风中读取音频数据，然后将音频数据通过websocket传递给语音识别模型进行识别，音频格式为bytes。
asr_server.py是语音识别模型的websocket服务端，负责接收音频数据，进行识别，然后将识别结果返回给客户端，识别结果格式为str。

模型存放位置为`~\.cache\modelscope\hub\`
语音识别服务运行前，会检查模型是否存在，如果不存在会自动下载模型。

## Examples

### example1 独立运行服务端和客户端

``` shell
python bin/example1/asr_server.py
python bin/example1/asr_lient.py
``` 

### example2 语音识别客户端嵌入gui

``` shell
python bin/example2/asr_server.py
python bin/example2/gui.py
``` 

### example3 语音识别客户端和服务端嵌入gui

``` shell
python bin/example3/asr_server.py
python bin/example3/gui.py
``` 

### example4 独立运行服务端、客户端和flask服务端

``` shell
python bin/example4/asr_server.py
python bin/example4/asr_lient.py
python bin/example4/flask_server.py
``` 