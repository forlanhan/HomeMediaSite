#!/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2017-3-2
@author: Yuan Yi fan
"""
import logging
import math

import time
import video_processor
from bdata.porn.xhamster import *
from util.pyurllib import  DownloadTask
from util import BackgroundTask

video_temp = "buffer/video_temp_%X.mp4"
shortcuts_temp = "buffer/shortcuts_temp_%X.gif"


class xHamsterDownloadTask(BackgroundTask):
    def set_progress(self, value):
        self.progress = value

    def __init__(self, page_url, key=None):
        BackgroundTask.__init__(self, name="download video")
        if key is None:
            self.key = int(math.ceil(time.time() * 1000))
        else:
            self.key = int(key)
        self.page_url = page_url

    def run(self):
        self.progress = 0
        self.progress_info = "Started, querying page data..."
        page_data, page_soup = getSoup(self.page_url)

        self.progress = 10
        self.progress_info = "Got page data, analysing...."

        mp4url = getDownloadLink(page_soup)
        title = getTitleFromSoup(page_soup)
        labels = getCategories(page_soup)
        save_filename = video_temp % self.key

        self.progress = 15
        self.progress_info = "Downloading video ..."
        task = DownloadTask(mp4url, save_filename, lambda value: self.set_progress(value * 0.65 + 15))
        task.start()
        task.join(timeout=3600 * 24)

        self.progress = 80
        self.progress_info = "Processing video ..."
        vcap = video_processor.get_video_cap(save_filename)
        video_basic_info = video_processor.get_video_basic_info(vcap)
        video_processor.get_video_preview(vcap, file_name=shortcuts_temp % self.key)

        self.progress = 95
        self.progress_info = "Inserting to database ..."
        # TODO: Copy files to target and insert info to mongodb
        print video_basic_info

        self.progress = 100
        self.terminated = True
