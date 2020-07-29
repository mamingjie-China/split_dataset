# split_dataset
该脚本主要用于对各类数据集进行切分，提供给进行训练，预计未来会集成到PaddleX中，欢迎大家使用[PaddleX](https://www.paddlepaddle.org.cn/paddle/paddleX)。
目前，已经支持COCO格式和VOC格式的数据集的切分，ImageNet和Seg格式的数据切分即将进行支持，具体的数据格式见[数据格式](https://paddlex.readthedocs.io/zh_CN/develop/data/format/index.html)。


**按需安装以下依赖**  
pycocotools[安装指导](https://paddlex.readthedocs.io/zh_CN/develop/install.html#pycocotools)

## 下载
### 下载方法一
```
git clone https://github.com/mamingjie-China/split_dataset.git
cd split_dataset
git checkout develop
```
### 下载方法二
直接下载zip文件[链接](https://github.com/PaddlePaddle/X2Paddle/archive/develop.zip)，解压缩后进入文件夹

## 使用方法
```
python split.py --type VOC --dir insect_det --val_percent 0.2 --test_percent 0.1
```

### 参数选项
| 参数 | |
|----------|--------------|
|--type | 数据集格式类型 (VOC、COCO、ImageNet、Seg) |
|--dir | 数据集文件夹的路径 |
|--val_percent | 验证集切分的比例（如0.2） |
|--test_percent | 测试集切分的比例（如0.1） |

## 交流与反馈

- 项目官网: https://www.paddlepaddle.org.cn/paddle/paddlex
- PaddleX用户交流群: 1045148026 (手机QQ扫描如下二维码快速加入)  
<img src="./docs/gui/images/QR.jpg" width="250" height="300" alt="QQGroup" align="center" />
