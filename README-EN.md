Here's the English version of your text:

<p align="center">
  <a href="https://github.com/yincangshiwei/HuggingFaceDown.git/releases">Download</a>
  ·
  <a href="https://github.com/yincangshiwei/HuggingFaceDown.git/blob/master/README.md">Chinese Docs</a>
  ·
  <a href="https://github.com/yincangshiwei/HuggingFaceDown.git/blob/master/README-EN.md">English Documents</a>
</p>

- - -
## Project Introduction

> This project aims to facilitate downloading models from the Hugging Face website. It is a small program developed purely out of personal interest. Initially, it was run using scripts but later transformed into this visual application with the help of AI, including debugging and tuning processes.

## Features

> Supports switching between Chinese and English

> Allows downloading model directories, supports downloading specified files

> Provides help documentation

## Technologies Used

> Python version: 3.10.13 (compatible with versions above 3.8)

> GUI framework: tkinter

> Help documentation rendering: tkhtmlview

> Packaging tool: py2exe

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

Architecture Overview:

- `main.py`: Main program file.
- `setup.py`: Script used for packaging the application.
- `requirements.txt`: Lists all dependencies.
- `README.md`: Project documentation in Chinese.
- `README-EN.md`: Project documentation in English.
- `resources`: Static resources directory.

## Installation Instructions

### 1. Clone the repository
```sh
git clone https://github.com/yincangshiwei/HuggingFaceDown.git
```

### 2. Navigate to the project directory
```sh
cd HuggingFaceDown
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

### 4. Run the application
```sh
python -u main.py
```

### 5. Package into an executable
```sh
python setup.py py2exe
```

## Current Issues

> The help documentation does not properly display images. This will be addressed when time permits.