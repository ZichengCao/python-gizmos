# 听写单词


效果：
输入单词本的路径，随机选取单词，显示中文解释并发音，用户需输入英文单词，回车提交拼写

原理：
1. 输入单词本的路径，读取需要学习的单词，下面以单词hello为例
2. 基于有道api（https://dict.youdao.com/suggest?num=5&ver=3.0&doctype=json&cache=false&le=en&q=hello） 获取hello的释义
3. 基于有道的api（https://dict.youdao.com/dictvoice?audio=hello&type=1）或者tts库获取hello的发音

## 使用说明

1. **安装 Python 和相关库：** 确保你的计算机上已经安装了 Python，
2. **安装相关库：** 将目录下的 `requirements.txt` 保存至本地，在命令行中运行 `pip install -r requirements.txt` 安装相关库。
3. **运行程序：** 将提供的 Python 代码保存为 `xx.py` 文件，然后在命令行中使用 `python xx.py ` 运行该文件即可。
4. **停止程序：** 若要停止程序，可以关闭程序运行的窗口或者在命令行中按下 `Ctrl+C` 组合键。