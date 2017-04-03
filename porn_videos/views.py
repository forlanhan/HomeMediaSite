# coding:utf-8
import os
import re
import string
import mimetypes
from django.http import HttpResponse
from util.httputils import get_request_get
from django.shortcuts import render
from util.config import preview_dir, preview_file, pvideo_dir, pvideo_file
from wsgiref.util import FileWrapper
from django.http.response import StreamingHttpResponse

range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)

def view_videos(request):
    try:
        ID = get_request_get(request, 'id')
        if ID is not None:
            ID = string.atoi(ID)
        query = get_request_get(request, 'query')
        new = get_request_get(request, 'new')
        pagesize = string.atoi(get_request_get(request, 'pagesize', '10'))
        pageid = string.atoi(get_request_get(request, 'pageid', '1'))
        if query is None and new != "1" and ID is None:
            pass
        elif query is not None and new != "1" and ID is None:
            """
            依照分页规则获取最新的pagesize条数据
            """

        elif query is None and new == "1" and ID is None:
            pass
            # New videos
        elif query is None and new != "1" and ID is not None:
            pass
        else:
            raise Exception("Error parameters")
        return HttpResponse("Debug mode.")
    except Exception, e:
        print "Error message:", e.message
        return HttpResponse("Error while processing parameters.")


def getPreviewImage(request):
    try:
        ID = request.GET['id']
        filename = preview_dir + preview_file % ID
        response = StreamingHttpResponse(file_iterator(filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(preview_file % ID)
        return response
    except:
        return HttpResponse("CDN Error: error while processing parameters.")


def file_iterator(file_name, chunk_size=4096):
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def testViewVideo(request):
    return render(request, "view_video.html", {
        "title": "Test Video",
        "videoInfoList": [
            {
                "previewUrl": "http://192.168.1.103/prev_1128.gif",
                "mp4Url": "http://192.168.1.103/porv_1128.mp4",
                "videoTitle": "VideoTest1",
                "playTime": "10:25",
                "resolution": "100×150",
                "tagList": ["porn", "pussy wide"],
            },
            {
                "previewUrl": "http://192.168.1.103/prev_1128.gif",
                "mp4Url": "http://192.168.1.103/porv_1128.mp4",
                "videoTitle": "VideoTest2",
                "playTime": "10:25",
                "resolution": "100×150",
                "tagList": [
                    "porn", "anal", "homemade", "porn", "anal", "homemade",
                    "porn", "anal", "homemade", "porn", "anal", "homemade",
                    "porn", "anal", "homemade", "porn", "anal", "homemade",
                ],
            },
        ],"paginationList":[
            {'url':"javascript:alert(1);", "text":1},
            {'url': "javascript:alert(2);", "text": 2},
            {'url': "javascript:alert(3);", "text": 3},
        ]})


def testIterator(request):
    return render(request, "test_iterator.html",
                  {"testList": [
                      {'a': ['a', 'b', 'v'], 'b': 2},
                      {'a': ['a1', 'b1', 'v1'], 'b': 2, "c": 'd'},
                      {'a': ['a2', 'b', 'v'], 'b': 2, "c": 1},
                  ]})