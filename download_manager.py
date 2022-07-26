#!/usr/bin/env python3
# This is a Python script that automates the management of the Downloads folder 
# for an organized experience. It will sort images, videos, documents, and ISO
# files on download.
#
# Written by Jadon Yack (jyack)

from os import scandir, getlogin, rename
from os.path import splitext, exists, join, isfile
from shutil import move as mv
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

user = getlogin()
src_dir = f"/home/{user}/Downloads"
img_dst = f"/home/{user}/Pictures/DownloadedImages"
vid_dst = f"/home/{user}/Videos"
doc_dst = f"/home/{user}/Documents"
iso_dst = f"/home/{user}/ISOs"

def makeUniq(file, dst, name):
    filename, extension = splitext(name)
    counter = 1
    uniq_name = name
    # If the file exists, add the counter to the filename
    while exists(f"{dst}/{name}"):
        uniq_name = f"{filename}({counter}){extension}"
        counter += 1

    return uniq_name

def move(entry, name, dst_dir):
    # Generate a unique file name and move the file to the destination 
    # directory
    uniq_name = makeUniq(entry, dst_dir, name)
    # Check that entry is a file before moving it
    if (isfile(entry.path)):
        mv(entry.path, f"{dst_dir}/{uniq_name}")

class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(src_dir) as entries:
            for entry in entries:
                name = entry.name
                dst = src_dir
                # If entry is an image
                if name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png'):
                    dst = img_dst
                    move(entry, name, dst)
                # If entry is a video
                elif name.endswith('.mp4') or name.endswith('.mov'):
                    dst = vid_dst
                    move(entry, name, dst)
                # If entry is a document
                elif name.endswith('.docx') or name.endswith('.pdf'):
                    dst = doc_dst
                    move(entry, name, dst)
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
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
