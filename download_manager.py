#!/usr/bin/env python3
"""
This is a Python script that automates the management of the Downloads folder 
for an organized experience. It will sort images, videos, documents, and ISO
files on download.

Written by Jadon Yack (jyack)
"""

from os import scandir, getlogin
from os.path import split, splitext, exists, isfile
from shutil import move as mv
from time import sleep
import threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from dm_logs import dm_logger_t

user = getlogin()
src_dir = f"/home/{user}/Downloads/"
img_dst = f"/home/{user}/Pictures/DownloadedImages/"
vid_dst = f"/home/{user}/Videos/"
doc_dst = f"/home/{user}/Documents/"
iso_dst = f"/home/{user}/ISOs/"

dm_logger = dm_logger_t()

file_types = {
    'image': [
        '.jpg',
        '.jpeg',
        '.png',
        '.gif',
        '.bmp',
        '.tiff',
        '.svg',
        '.webp',
        '.ico',
        '.heic',
        '.psd'
        ],
    'video': [
        '.mp4',
        '.mkv',
        '.avi',
        '.mov',
        '.wmv',
        '.flv',
        '.webm',
        '.mpeg',
        '.mpg',
        '.m4v',
        '.3gp'
        ],
    'doc':   [
        '.pdf',
        '.doc',
        '.docx',
        '.txt',
        '.rtf',
        '.odt',
        '.ppt',
        '.pptx',
        '.xls',
        '.xlsx',
        '.csv',
        '.epub'
        ]
}

def makeUniq(dst, name):
    filename, extension = splitext(name)
    counter = 1
    uniq_name = name
    # If the file exists, add the counter to the filename
    while exists(f"{dst}/{name}"):
        uniq_name = f"{filename}({counter}){extension}"
        counter += 1

    dm_logger.dm_log_info(f'Generated unique file name {uniq_name}')
    return uniq_name

def move(event, name, dst_dir):
    # Generate a unique file name and move the file to the destination
    # directory
    uniq_name = makeUniq(dst_dir, name)
    # Check that event is a file before moving it
    if isfile(event.src_path):
        mv(event.src_path, f"{dst_dir}/{uniq_name}")
        dm_logger.dm_log_info(f"Moved file {uniq_name} to {dst_dir}")
    else:
        dm_logger.dm_log_err(f"ERROR: {name} not a file")

class FileHandler(FileSystemEventHandler):
    def __init__(self, buffer_time=5):
        self.events = []
        self.buffer_time = buffer_time
        self.lock = threading.Lock()
        self.timer = None

    def on_created(self, event):
        with self.lock:
            dm_logger.dm_log_debug(f"Found new file {event.src_path}")
            self.events.append(event)
            if not self.timer:
                self.timer = threading.Timer(self.buffer_time,
                                            self.process_event)
                self.timer.start()

    def process_event(self):
        with self.lock:
            dm_logger.dm_log_info(f'Processing {len(self.events)} files...')
            for event in self.events:
                file_name      = split(event.src_path)[1]
                file_extension = splitext(file_name)[1]
                dst            = src_dir
                dm_logger.dm_log_debug(f"Sorting {file_name}...")

                # If event is an image
                if file_extension in file_types['image']:
                    dst = img_dst
                    move(event, file_name, dst)
                # If event is a video
                elif file_extension in file_types['video']:
                    dst = vid_dst
                    move(event, file_name, dst)
                # If event is a document
                elif file_extension in file_types['doc']:
                    dst = doc_dst
                    move(event, file_name, dst)
                # If event is an ISO file
                elif file_extension == 'iso':
                    dst = iso_dst
                    move(event, file_name, dst)

            self.events = []
            self.timer = None


if __name__ == "__main__":
    dm_logger.dm_log_info('Starting watchdog module...')
    path = src_dir
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(3)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
