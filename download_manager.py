#!/usr/bin/env python3
# This is a Python script that automates the management of the Downloads folder 
# for an organized experience. It will sort images, videos, documents, and ISO
# files on download.
#
# Written by Jadon Yack (jyack)

import os

user = os.getlogin()
src_dir = "/home/" + user + "/Downloads"
img_dst = "/home/" + user + "/Pictures/DownloadedImages"
vid_dst = "/home/" + user + "/Videos"
doc_dst = "/home/" + user + "/Documents"
iso_dst = "/home/" + user + "/ISOs"

