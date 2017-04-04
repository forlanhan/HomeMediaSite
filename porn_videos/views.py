# coding:utf-8
import os
import re
import string
import mimetypes
from django.http import HttpResponse
from util.httputils import *
from util.db import *
from django.shortcuts import render
from util.config import *
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
        pagesize = string.atoi(get_request_get_default(request, 'pagesize', default_pagesize))
        pageid = string.atoi(get_request_get_default(request, 'pageid', '1'))
        if query is None and new != "1" and ID is None:
            """
            标记为Like的视频
            """
            pass
        elif query is not None and new != "1" and ID is None:
            """
            搜索视频
            """
            offset = (pageid - 1) * pagesize
            sql_query = """
                        SELECT  index, tags, basic_info, like_it 
                        FROM public.video_basic_info 
                        WHERE basic_info->>'name' like '%%%s%%'
                        ORDER BY index desc 
                        LIMIT %d 
                        OFFSET %d
                        """ % (query, pagesize, offset)
            queryResult = queryInfoNewConn(sql_query)
            renderInfo = generateRenderStruct(queryResult)
            #翻页显示控制
            if pageid > 0:
                renderInfo["paginationList"].append({
                    'url': "./?query=%s&pageid=%d" % (query, 0),
                    "text": "<<"
                })
                renderInfo["paginationList"].append({
                    'url': "./?query=%s&pageid=%d" % (query, (pageid - 1)),
                    "text": "<"
                })
            renderInfo["paginationList"].append({
                'url': "./?query=%s&pageid=%d" % (query, (pageid + 1)),
                "text": ">"
            })
            return render(request, "view_video.html", renderInfo)

        elif query is None and new == "1" and ID is None:
            """
            依照分页规则获取最新的pagesize条数据
            """
            offset = (pageid - 1) * pagesize
            sql_query = """
                        SELECT  index, tags, basic_info, like_it 
                        FROM public.video_basic_info 
                        ORDER BY index desc 
                        LIMIT %d 
                        OFFSET %d
                        """ % (pagesize, offset)
            queryResult = queryInfoNewConn(sql_query)
            renderInfo = generateRenderStruct(queryResult)
            # 翻页显示控制
            if pageid > 0:
                renderInfo["paginationList"].append({
                    'url': "./?new=1&pageid=%d" % 0,
                    "text": "<<"
                })
                renderInfo["paginationList"].append({
                    'url': "./?new=1&pageid=%d" % (pageid - 1),
                    "text": "<"
                })
            renderInfo["paginationList"].append({
                'url': "./?new=1&pageid=%d" % (pageid + 1),
                "text": ">"
            })
            return render(request, "view_video.html", renderInfo)

        elif query is None and new != "1" and ID is not None:
            """
            仅仅显示一个视频的信息
            并且显示标记Tag的按钮，以及详细设置的控件
            """
            pass
        else:
            raise Exception("Error parameters")
        return HttpResponse("Unachievable place")
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


def generateRenderStruct(queryResult):
    renderInfo = {"title": "最新视频", "paginationList": [], "videoInfoList": []}
    for resRow in queryResult:
        id = resRow[0]
        basicInfo = resRow[2]
        renderInfo["videoInfoList"].append({
            "previewUrl": preview_dir + preview_file % id,
            "mp4Url": pvideo_dir + pvideo_file % id,
            "videoTitle": basicInfo["name"],
            "playTime": basicInfo["duration"],
            "resolution": "%d×%d" % (basicInfo["width"], basicInfo["height"]),
            "tagList": resRow[1],
        })
    return renderInfo
