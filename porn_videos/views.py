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


def getVideo(request):
    try:
        ID = request.GET['id']
        filename = pvideo_dir + pvideo_file % ID
        return stream_video(request, filename)
    except:
        return HttpResponse("CDN Error: error while processing parameters.")


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


def stream_video(request, path):
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(file_iterator(path), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp
