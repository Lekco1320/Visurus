# Visurus

[![hugo-papermod](https://img.shields.io/badge/Visurus-@Lekco-red)](https://github.com/Lekco1320/Visurus)
[![release](https://img.shields.io/github/v/release/Lekco1320/Visurus)](https://github.com/Lekco1320/Visurus/releases)
[![Apache License](https://img.shields.io/npm/l/echarts?color=green)](LICENSE)

> ***Visurus*** is the future participle form of the Latin verb ***videō*** (to see).

*Visurus* 是一个批量图像格式化、图像拼接和添加水印的开源工具。

## 功能展示
### 图像格式化
|||
|:-:|:-:|
|![](samples/species_label.jpg)物种标注|![](samples/photo_params_s.jpg)参数标注（样式1）|
|![](samples/photo_params_c.jpg)参数标注（样式2）|![](samples/photo_params_b.jpg)参数标注（样式3）|

格式化设置中可以一键设置图像大小、图像阴影、图像圆角，附有详细的参数设置。

### 添加水印
* 支持批量添加文字或图片水印
* 水印尺寸可自由指定、自适应或比例缩放

### 其他功能
* 图像拼接
* 图像装裱

### 首选项
* 用户可根据喜好调整各功能的首选项

## 安装与使用
### Windows
* 请先安装Python环境(>=3.11)和pip。
* 点击[Release](https://github.com/Lekco1320/Visurus/releases)
下载对应版本的压缩包`Source code.zip`或`Source code.tar.gz`。
* 解压到除系统盘外的任意磁盘下，使用终端打开文件夹`src`，执行安装命令：
``` bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
deactivate
```

* 运行脚本时，进入`src`文件夹，执行命令：
``` bash
venv\Scripts\activate
python ./main.py
```

### Unix系统 (MacOS, Linux, etc.)
* 请先安装Python环境(>=3.11)和pip。
* 启动终端，执行安装命令：
``` bash
git clone --depth 1 https://github.com/Lekco1320/Visurus.git ./Visurus
cd ./Visurus
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
python3 ./main.py
```

* 运行脚本时，进入`src`文件夹，执行命令：
``` bash
source ./venv/bin/activate
python3 ./main.py
```

## 许可声明
Visurus基于 [Apache License 2.0](LICENSE) 发布。

Visurus引用了：
* [Pillow](https://python-pillow.org/)，其发布基于
[License](https://github.com/python-pillow/Pillow/blob/main/LICENSE) .
* [pyreadline3](https://github.com/pyreadline3/pyreadline3)，其发布基于
[License](https://github.com/pyreadline3/pyreadline3/blob/master/LICENSE.md) .
* [思源宋体](https://source.typekit.com/source-han-serif/)，其发布基于
[License](https://github.com/adobe-fonts/source-han-serif/blob/release/LICENSE.txt) .
* [阿里巴巴普惠体3.0](https://www.alibabafonts.com/#/font)，其发布基于
[法律声明](https://www.yuque.com/yiguang-wkqc2/puhuiti/nus9wiinq4aeiegy) .
