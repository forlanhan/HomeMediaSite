#!/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2017-2-3
@author: Yuan Yi fan

处理超链接以及超链接获取的BeautifulSoup类
"""
import os
import string
import urllib
import urllib2
import re

import math
from bs4 import BeautifulSoup
import threading

from util import BackgroundTask

# 请求超时设置
request_timeout = 25

# 浏览器的User Agent参数
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " + \
             "AppleWebKit/537.36 (KHTML, like Gecko) " + \
             "Chrome/42.0.2311.135 " + \
             "Safari/537.36 " + \
             "Edge/12.10240"

# XML解析器
XML_decoder = 'lxml'


def get_request_head(url):
    req_header = {
        'User-Agent': user_agent,
        'Accept': '"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Host': re.findall('://.*?/', url, re.DOTALL)[0][3:-1]
    }
    return req_header


def get_request(url):
    return urllib2.Request(url, None, get_request_head(url))


def urlread2(url, retry_times=10):
    for i in range(retry_times):
        try:
            req_header = {
                'User-Agent': user_agent,
                'Accept': '"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Host': re.findall('://.*?/', url, re.DOTALL)[0][3:-1]}

            return urllib2.urlopen(get_request(url), None, request_timeout).read()
        except:
            pass
    print "Error while reading:", url


def get_soup(url, retry_tms=10):
    for i in range(retry_tms):
        try:
            return BeautifulSoup(urlread2(url), XML_decoder)  # html.parser
        except Exception, e:
            print "Error info:", e
            if e.code == 301:
                return BeautifulSoup("", XML_decoder)
            print "Retrying to get data of %s" % url


class CreateDownloadTask(threading.Thread):
    """
    File download module
    """

    def __init__(self, src_url, dst_path):
        # type: (string, string) -> CreateDownloadTask
        threading.Thread.__init__(self)
        self.url = src_url
        self.dst = dst_path
        self.info = []

    def set_current_info(self, info):
        self.info = info

    def get_current_info(self):
        return self.info

    def run(self):
        urllib.urlretrieve(
            url=self.url,
            filename=self.dst,
            reporthook=lambda block_download_count, block_size, file_size: self.set_current_info({
                "current_percent": block_download_count * block_size * 100.0 / file_size,
                "block_download_count": block_download_count,
                "block_size": block_size,
                "file_size": file_size
            }))


class LiteFileDownloader(threading.Thread):
    """
    小文件下载线程
    """

    def __init__(self, image_url, filename):
        threading.Thread.__init__(self)
        self.image_url = image_url
        self.filename = filename
        self.done = 0

    def run(self):
        if not os.path.exists(self.filename):  # 已经下载过了
            data = urlread2(url=self.image_url)
            if data is not None:
                with open(self.filename, 'wb') as fid:
                    fid.write(data)


class LiteDataDownloader(threading.Thread):
    """
    小文件下载线程(数据缓存)
    """

    def __init__(self, image_url, tag):
        threading.Thread.__init__(self)
        self.image_url = image_url
        self.data = None
        self.tag = tag

    def run(self):
        self.data = urlread2(url=self.image_url)

    def write_file(self, filename):
        if self.data is not None:
            with open(filename, 'wb') as fid:
                fid.write(self.data)


class DownloadTask(BackgroundTask):
    def __init__(self, url, filename, progress_callback=lambda value: None, block_size=1024 * 1024):
        BackgroundTask.__init__(self, name="download:" + filename)
        self.set_parent_progress = progress_callback
        self.target_url = url
        self.save_file = filename
        self.block_size = block_size

    def run(self):
        self.progress_info = "获取请求中..."
        response = urllib2.urlopen(get_request(self.target_url), None, request_timeout)
        try:
            file_size = string.atoi(response.headers.get('content-length'))
        except:
            file_size = None
        with open(self.save_file, "wb") as fp:
            if file_size is None:
                self.progress_info = "正在下载小文件..."
                self.progress = 0
                fp.write(response.read())
                self.progress = 100
            else:
                self.progress_info = "大文件下载中..."
                self.progress = 0
                block_count = int(math.ceil(file_size * 1.0 / self.block_size))
                for i in range(block_count):
                    fp.write(response.read(self.block_size))
                    # fp.flush() # 手动刷新
                    self.progress = (i + 1) * 100.0 / block_count

        self.terminated = True
