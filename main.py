import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from PIL import Image, ImageTk
from huggingface_hub import hf_hub_download, snapshot_download
from tkhtmlview import HTMLLabel  # Import for rendering HTML content
import os
import sys
import threading
import time
import re


class CustomLogHandler:
    """Redirect stdout and stderr to the tkinter log box."""
    def __init__(self, log_function):
        self.log_function = log_function

    def write(self, message):
        # Remove ANSI escape sequences and other unwanted characters
        clean_message = self.remove_ansi_sequences(message)
        if clean_message.strip():  # Avoid logging empty or whitespace lines
            self.log_function(clean_message)

    def flush(self):
        pass  # This is required but does nothing

    @staticmethod
    def remove_ansi_sequences(text):
        # Regex to remove ANSI escape sequences (e.g., color codes and cursor moves)
        ansi_escape = re.compile(r'\x1B(?:[@-_][0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)


class HuggingFaceModelDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Hugging Face Model Downloader")
        self.root.geometry("500x600")

        # Style configuration
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12))
        style.configure('TFrame', padding=(10, 10))

        # Load folder icon
        try:
            self.folder_icon = Image.open("./resources/folder.png")  # Ensure you have a folder.png image in the same directory
            self.folder_icon = self.folder_icon.resize((20, 20), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
            self.folder_photo = ImageTk.PhotoImage(self.folder_icon)
        except Exception as e:
            print(f"Error loading folder icon: {e}")
            self.folder_photo = None

        # Create main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create language switch button
        self.language_var = tk.StringVar(value="CN")
        self.lang_button = ttk.Button(main_frame, textvariable=self.language_var, command=self.switch_language, width=3)
        self.lang_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)

        # Create help button
        self.help_button = ttk.Button(main_frame, text="帮助", command=self.show_help_dialog)
        self.help_button.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        # Initialize UI elements
        self.repo_id_label = ttk.Label(main_frame, text="")
        self.repo_id_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.repo_id_entry = ttk.Entry(main_frame, width=40)
        self.repo_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW, columnspan=3)

        self.save_dir_label = ttk.Label(main_frame, text="")
        self.save_dir_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.save_dir_text = tk.Text(main_frame, height=2, wrap='word')
        self.save_dir_text.grid(row=2, column=1, padx=10, pady=5, sticky=tk.EW, columnspan=2)

        self.directory_button = ttk.Button(main_frame, text='', command=self.select_directory, compound=tk.LEFT)
        self.directory_button.image = self.folder_photo  # Keep a reference to avoid garbage collection
        self.directory_button.grid(row=2, column=3, padx=5, pady=5)

        self.filename_label = ttk.Label(main_frame, text="")
        self.filename_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        self.filename_entry = ttk.Entry(main_frame, width=40)
        self.filename_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.EW, columnspan=3)

        self.proxy_label = ttk.Label(main_frame, text="")
        self.proxy_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

        self.proxy_entry = ttk.Entry(main_frame, width=40)
        self.proxy_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.EW, columnspan=2)
        self.proxy_entry.insert(0, 'https://hf-mirror.com')  # Default proxy URL

        self.enable_proxy_var = tk.BooleanVar(value=True)
        self.enable_proxy_check = ttk.Checkbutton(main_frame, text="", variable=self.enable_proxy_var)
        self.enable_proxy_check.grid(row=4, column=3, padx=5, pady=5)

        # Buttons frame to hold download and stop buttons side by side
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=4, pady=10)

        self.download_button = ttk.Button(buttons_frame, text="", command=self.start_download)
        self.download_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = ttk.Button(buttons_frame, text="", state=tk.DISABLED, command=self.exit_program)
        self.stop_button.pack(side=tk.RIGHT, padx=10)

        self.log_box = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=60, height=10)
        self.log_box.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky=tk.NSEW)

        # Configure grid weights for better resizing
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)

        # Thread control variables
        self.download_thread = None
        self.stop_event = threading.Event()

        # Redirect stdout and stderr to custom handler
        sys.stdout = CustomLogHandler(self.log_message)
        sys.stderr = CustomLogHandler(self.log_message)

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize UI language
        self.update_ui_language(self.language_var.get())

    def select_directory(self):
        save_directory = filedialog.askdirectory()
        if save_directory:
            self.save_dir_text.delete(1.0, tk.END)
            self.save_dir_text.insert(tk.END, save_directory)

    def start_download(self):
        repo_id = self.repo_id_entry.get().strip()
        save_directory = self.save_dir_text.get(1.0, tk.END).strip()
        filename = self.filename_entry.get().strip()

        if not repo_id:
            self.log_message("请输入 Repo ID.", "red")
            return

        if not save_directory:
            self.log_message("请输入/选择 存放目录路径.", "red")
            return

        self.download_thread = threading.Thread(target=self.download_model, args=(repo_id, save_directory, filename))
        self.download_thread.start()
        self.download_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.stop_event.clear()

    def exit_program(self):
        self.log_message("程序即将退出...", "orange")
        self.stop_event.set()

        # 给后台线程最多 1 秒钟的时间退出
        timeout = 1
        start_time = time.time()
        while self.download_thread and self.download_thread.is_alive():
            if time.time() - start_time > timeout:
                self.log_message("后台线程未能及时退出，强制退出程序。", "red")
                break
            time.sleep(0.1)

        self.root.destroy()
        os._exit(0)  # 确保彻底退出

    def on_closing(self):
        self.exit_program()

    def download_model(self, repo_id, save_directory, filename):
        try:
            if filename:
                # Download specific file
                self.log_message(f"{self.get_log_message('start_downloading_file').format(filename, save_directory)}...")
                hf_hub_download(repo_id=repo_id, filename=filename, local_dir=save_directory, etag_timeout=1000, endpoint=self.proxy_entry.get().strip() if self.enable_proxy_var.get() else None)
                self.log_message(f"{self.get_log_message('file_downloaded_successfully').format(filename, save_directory)}", "green")
            else:
                # Download the entire repository
                self.log_message(f"{self.get_log_message('start_downloading_repo').format(repo_id, save_directory)}...")
                snapshot_download(repo_id=repo_id, local_dir=save_directory, etag_timeout=1000, endpoint=self.proxy_entry.get().strip() if self.enable_proxy_var.get() else None)
                self.log_message(f"{self.get_log_message('model_downloaded_successfully').format(save_directory)}", "green")
        except Exception as e:
            if not self.stop_event.is_set():
                self.log_message(f"{self.get_log_message('download_error')} {str(e)}", "red")
        finally:
            self.download_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def log_message(self, message, color="black"):
        self.log_box.config(state=tk.NORMAL)

        self.log_box.insert(tk.END, message + "\n", ("color", color))
        self.log_box.tag_configure("color", foreground=color)
        self.log_box.yview(tk.END)
        self.log_box.config(state=tk.DISABLED)

    def switch_language(self):
        current_lang = self.language_var.get()
        new_lang = "EN" if current_lang == "CN" else "CN"
        self.language_var.set(new_lang)
        self.update_ui_language(new_lang)

    def update_ui_language(self, lang):
        if lang == "CN":
            self.repo_id_label.config(text="Repo ID:")
            self.save_dir_label.config(text="存放目录路径:")
            self.filename_label.config(text="文件名 (可选):")
            self.proxy_label.config(text="代理地址:")
            self.directory_button.config(text='选择路径')
            self.enable_proxy_check.config(text="启用代理")
            self.download_button.config(text="下载模型")
            self.stop_button.config(text="退出程序")
            self.help_button.config(text="帮助")
        elif lang == "EN":
            self.repo_id_label.config(text="Repo ID:")
            self.save_dir_label.config(text="Save Directory Path:")
            self.filename_label.config(text="Filename (optional):")
            self.proxy_label.config(text="Proxy Address:")
            self.directory_button.config(text='Select Path')
            self.enable_proxy_check.config(text="Enable Proxy")
            self.download_button.config(text="Download Model")
            self.stop_button.config(text="Exit Program")
            self.help_button.config(text="Help")

    def get_log_message(self, key):
        messages = {
            "start_downloading_file": {
                "CN": "开始下载文件 {} 到 {}...",
                "EN": "Starting to download file {} to {}..."
            },
            "file_downloaded_successfully": {
                "CN": "文件 {} 成功下载到 {}",
                "EN": "File {} downloaded successfully to {}"
            },
            "start_downloading_repo": {
                "CN": "开始下载整个仓库 {} 到 {}...",
                "EN": "Starting to download the entire repository {} to {}..."
            },
            "model_downloaded_successfully": {
                "CN": "模型成功下载到 {}",
                "EN": "Model downloaded successfully to {}"
            },
            "download_error": {
                "CN": "模型下载错误:",
                "EN": "Model download error:"
            },
            "error": {
                "CN": "错误:",
                "EN": "Error:"
            },
            "help_findNoFile": {
                "CN": "找不到帮助文档文件:",
                "EN": "Unable to find the help document file:"
            },
            "help_doc_window_title": {
                "CN": "帮助文档:",
                "EN": "Help Doc"
            }
        }
        return messages[key][self.language_var.get()]

    def show_help_dialog(self):
        help_window = tk.Toplevel(self.root)
        help_window.title(self.get_log_message('help_doc_window_title'))
        help_window.geometry("600x400")

        # Determine which help file to load based on the current language
        current_lang = self.language_var.get()
        html_file_path = f"./resources/help_{current_lang}.html"

        if not os.path.exists(html_file_path):
            messagebox.showerror(self.get_log_message('error'), f"{self.get_log_message('help_findNoFile')}: {html_file_path}")
            help_window.destroy()
            return

        with open(html_file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        html_label = HTMLLabel(help_window, html=html_content, bg='white')
        html_label.pack(expand=True, fill='both')

        help_window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = HuggingFaceModelDownloader(root)
    root.mainloop()