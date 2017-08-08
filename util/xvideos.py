#!/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2017-3-2
@author: Yuan Yi fan
"""
import re

import math

import time

import video_processor
from bs4 import BeautifulSoup
from util.pyurllib import urlread2, CreateDownloadTask, DownloadTask
from util.str_util import validation_filename
from util import BackgroundTask

XML_DECODER = "lxml"
video_temp = "buffer/video_temp_%X.mp4"
shortcuts_temp = "buffer/shortcuts_temp_%X.gif"


def get_data(url):
    return urlread2(url)


def get_soup(url):
    return BeautifulSoup(urlread2(url), XML_DECODER)


def get_data_soup(url):
    data = get_data(url)
    return data, BeautifulSoup(data, XML_DECODER)


def get_mp4_url(page_data):
    return re.findall("html5player.setVideoUrlHigh(.*?);", page_data)[0][2:-2]


def get_title(page_soup):
    return page_soup.find("meta", attrs={"property": "og:title"})['content']


def get_keyword(page_soup):
    return page_soup.find("meta", attrs={"name": "keywords"})['content'].split(",")


def get_download_task(url, save_path):
    page_data = get_data(url)
    page_soup = BeautifulSoup(page_data, XML_DECODER)
    mp4url = get_mp4_url(page_data)
    title = get_title(page_soup)
    save_filename = save_path + validation_filename(title) + ".mp4"
    return CreateDownloadTask(mp4url, save_filename)


def auto_process_urls(urls, save_path):
    process_list = list()
    for url in urls:
        try:
            download_thread = get_download_task(url, save_path)
            process_list.append(download_thread)
            download_thread.start()
        except Exception as ex:
            print "Error while appending task:", ex

    for process in process_list:
        process.join()


class XVideoDownloadTask(BackgroundTask):
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
        page_data = get_data(self.page_url)

        self.progress = 10
        self.progress_info = "Got page data, analysing...."
        page_soup = BeautifulSoup(page_data, XML_DECODER)
        mp4url = get_mp4_url(page_data)
        title = get_title(page_soup)
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

        self.progress = 100
        self.terminated = True
