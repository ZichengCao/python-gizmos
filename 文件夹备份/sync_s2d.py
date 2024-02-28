"""
@Description :   使用 watchdog 库实现实时文件夹同步备份
@Author      :   Evan
@Time        :   2024/02/27 11:04:33
@Version     :   1.0
"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os,time
import shutil

# 装饰器函数，用于异常处理和输出异常信息
def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pass#print(f"An error occurred: {e}")
    return wrapper

# 复制文件或文件夹
@handle_exception
def copy(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)

# 删除文件或文件夹
@handle_exception
def delete(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

# 文件夹同步处理器
class FolderSyncHandler(FileSystemEventHandler):
    def __init__(self, src_folder, dst_folder):
        self.src_folder = src_folder
        self.dst_folder = dst_folder


    def sync(self, src_path, dst_path):
        if os.path.exists(src_path):
            copy(src_path, dst_path)
        else:
            delete(dst_path)

    def on_created(self, event):
        src_path = event.src_path
        dst_path = src_path.replace(self.src_folder, self.dst_folder)
        self.sync(src_path, dst_path)

    def on_deleted(self, event):
        src_path = event.src_path
        dst_path = src_path.replace(self.src_folder, self.dst_folder)
        self.sync(src_path, dst_path)

    def on_modified(self, event):
        src_path = event.src_path
        dst_path = src_path.replace(self.src_folder, self.dst_folder)
        self.sync(src_path, dst_path)

    def on_moved(self, event):
        src_path = event.src_path
        dst_path = event.dest_path.replace(self.src_folder, self.dst_folder)
        self.sync(src_path, dst_path)

        # 删除旧的目标文件或文件夹
        old_dst_path = event.src_path.replace(self.src_folder, self.dst_folder)
        print(old_dst_path)
        delete(old_dst_path)

# 启动文件夹同步备份
def start_folder_sync(src_folder, dst_folder):
    event_handler = FolderSyncHandler(src_folder, dst_folder)
    observer = Observer()
    observer.schedule(event_handler, src_folder, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    src_folder = "folder1"
    dst_folder = "folder2"

    
    start_folder_sync(src_folder, dst_folder)