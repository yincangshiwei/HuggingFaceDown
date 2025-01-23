<p align="center">
  <a href="https://github.com/yincangshiwei/HuggingFaceDown.git/releases">Download</a>
  ·
  <a href="https://github.com/yincangshiwei/HuggingFaceDown.git/blob/master/README.md">中文文档</a>
  ·
  <a href="https://github.com/yincangshiwei/HuggingFaceDown.git/blob/master/README-EN.md">English Documents</a>
</p>

- - -
## Project Introduction

> This project is mainly aimed at facilitating the downloading of models from the Hugging Face website. It's a small program developed purely out of personal interest. Initially, it was run using scripts, but later an AI was used to help create this visual application, with continuous debugging and tuning with the help of AI.

## Features

> Supports switching between Chinese and English

> Supports downloading model directories, as well as specified file downloads

> Provides help documentation

## Usage Instructions

> Run File: dist/HuggingFaceDownApp/HuggingFaceDownApp.exe

> If you need to store in another directory, copy the entire HuggingFaceDownApp directory.

## Relevant Technologies

> Python version: 3.10.13 (any version above 3.8 is acceptable)

> GUI UI used: tkinter

> Help documentation used: tkhtmlview

> Packaging program used: py2exe

### Directory Structure

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

Architecture Introduction:

- `main.py`: Main program file.
- `setup.py`: Script for packaging the application.
- `requirements.txt`: Lists all dependencies.
- `README.md`: Project documentation (Chinese).
- `README-EN.md`: Project documentation (English).
- `resources`: Static resources directory.

```

## Installation Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/yincangshiwei/HuggingFaceDown.git
```

### 2. Enter the Project Directory
```sh
cd HuggingFaceDown
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Run the Application
```sh
python -u main.py
```

### 5. Package into EXE
```sh
python setup.py py2exe
```

## Current Issues

> The help documentation does not effectively display images, which will be modified when time permits.
