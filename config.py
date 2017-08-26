#!/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2017-2-4
@author: Yuan Yi fan

配置文件，记录各种配置
"""

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

video_temp = "buffer/video_temp_%X.mp4"
shortcuts_temp = "buffer/shortcuts_temp_%X.gif"

media_file_dir = "E:/File/www/"
video_saving_path = media_file_dir + "video/file/porv_%d.mp4"
shortcuts_saving_path = media_file_dir + "video/preview/prev_%d.gif"

trash_video_dir = media_file_dir + "trash/video/"
trash_video_file = trash_video_dir + "porv_%d.mp4"
trash_video_info = trash_video_dir + "porv_%d.json"
