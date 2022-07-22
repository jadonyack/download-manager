#!/usr/bin/env python3
# This is a Python script that automates the management of the Downloads folder 
# for an organized experience. It will sort images, videos, documents, and ISO
# files on download.
#
# Written by Jadon Yack (jyack)

import os
import shutil
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

user = os.getlogin()
src_dir = "/home/" + user + "/Downloads"
img_dst = "/home/" + user + "/Pictures/DownloadedImages"
vid_dst = "/home/" + user + "/Videos"
doc_dst = "/home/" + user + "/Documents"
iso_dst = "/home/" + user + "/ISOs"

def makeUniq(path, name):
    

def move(entry, name, dst_dir):
    name = makeUniq(entry.path, name)
    

class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(src_dir) as entries:
            for entry in entries:
                name = entry.name
                dst = src_dir
                # If entry is an image
                if name.endswith('.jpg') or name.endswith('.jpeg') 
                or name.endswith('.png'):
                    dst = img_dst
                # If entry is a video
                elif name.endswith('.mp4') or name.endswith('.mov'):
                    dst = vid_dst
                # If entry is a document
                elif name.endswith('.docx') or name.endswith('.pdf'):
                    dst = doc_dst
                # If entry is an ISO file
                elif name.endswith('.iso'):
                    dst = iso_dst

                move(entry, name, dst)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = src_dir
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
