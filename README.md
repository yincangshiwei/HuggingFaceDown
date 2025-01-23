<p align="center">
  <a href="https://github.com/yincangshiwei/HuggingFaceDown.git/releases">Download</a>
  ·
  <a href="https://github.com/yincangshiwei/HuggingFaceDown.git/blob/master/README.md">中文文档</a>
  ·
  <a href="https://github.com/yincangshiwei/HuggingFaceDown.git/blob/master/README-EN.md">English Documents</a>
</p>

- - -
## 项目介绍

> 该项目主要是作用在方便下载Hugging Face网站的模型，纯个人喜好开发的一个小程序项目，之前一直使用脚本来运行，后来就用AI帮我做出这个可视化小程序，期间一直跟AI做程序调试和调教。

## 功能介绍

> 支持中英切换

> 支持下载模型目录，支持指定文件下载

> 提供帮助说明

![image](https://github.com/user-attachments/assets/2873ed46-a32f-4f04-9574-2f62fb647513)


## 使用说明

> 运行文件：dist/HuggingFaceDownApp/HuggingFaceDownApp.exe

> 如需另行存放目录，需拷贝HuggingFaceDownApp整个目录。

## 相关技术

> Python版本：3.10.13(大于3.8都可)

> GUI UI使用：tkinter

> 帮助文档使用：tkhtmlview

> 打包程序使用：py2exe

### 目录结构

```
HuggingFaceDown/
├── main.py
├── setup.py
├── requirements.txt
├── README.md
├── help_docs/
│   ├── en.html
│   └── zh.html
├── utils/
│   ├── download_utils.py
│   └── language_utils.py
└── assets/
    ├── images/
    │   ├── icon.png
    │   └── logo.png
    └── styles/
        └── style.css
```

```

架构介绍：

- `main.py`: 主程序文件。
- `setup.py`: 用于打包应用程序的脚本。
- `requirements.txt`: 列出了所有依赖项。
- `README.md`: 项目的说明文档（中文）。
- `README-EN.md`: 项目的说明文档（英文）。
- `resources`: 静态资源目录。

```

## 安装说明

### 1. 拉取项目
```sh
git clone https://github.com/yincangshiwei/HuggingFaceDown.git
```

### 2. 进入项目目录
```sh
cd HuggingFaceDown
```

### 3. 安装相关依赖
```sh
pip install -r requirements.txt
```

### 4. 运行文件
```sh
python -u main.py
```

### 5. 打包exe
```sh
python setup.py py2exe
```

## 现阶段问题

> 帮助文档没有有效的展示出图片，后续有时间再修改。
