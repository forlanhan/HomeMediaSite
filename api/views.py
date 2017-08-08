# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import string
from util.list_file_io import read_raw
from util.connections import *
from util.http import *
from util.files import *

# Region default settings

"""
Should inited by dict, for example:
{
    "host":"192.168.1.103",
    "page_index":10200,
    "image_filename":"0.jpg"
}
"""
apache_image_url_template = "http://%(host)s/external/img_pool/%(page_index)08d/%(image_filename)s"
local_image_list_path = "/media/yuanyifan/ext_data/img_pool/%(page_index)08d/"
local_novel_path_gen = "/media/yuanyifan/ext_data/novel_lib/%d.txt"


# Region: get information from database/filesystem for frontend api

@response_json
def get_image_list(request):
    """
    Query image urls by indicated index
    :param request: HTTP request
    :return: images' urls by given index
    """
    image_page_index = string.atoi(request.GET["id"])
    host = get_host(request)
    file_list = filter(filter_images, os.listdir(local_image_list_path % {
        "page_index": image_page_index
    }))

    return {
        "images": [apache_image_url_template % {
            "host": host,
            "page_index": image_page_index,
            "image_filename": filename
        } for filename in file_list]
    }


@response_json
def get_novel_object(request):
    """
    Query image urls by indicated index
    :param request: HTTP request
    :return: images' urls by given index
    """
    novel_index = string.atoi(request.GET["id"])
    with MongoDBDatabase("website_pron") as mgdb:
        res = mgdb.get_collection("novels").find_one({"_id": {"$eq": novel_index}})
        assert res is not None
        res["novel_text"] = read_raw(local_novel_path_gen % novel_index)
        return res


@response_json
def get_novel(request):
    """
    Query image urls by indicated index
    :param request: HTTP request
    :return: images' urls by given index
    """
    return get_novel_object(request)


@response_json
def query_novel_by_title(request):
    """
    Query novel list by title <-- generated regex
    :param request:
    :return:
    """
    query_keyword = request.GET["query"]
    block_settings = json.loads(get_request_with_default(request, "block", "[]"))
    page_size = string.atoi(get_request_with_default(request, "n", "30"))
    page_index = string.atoi(get_request_with_default(request, "p", "1"))
    assert page_size >= 1
    assert page_index >= 1
    with MongoDBDatabase("website_pron") as mgdb:
        query_res = mgdb.get_collection("novels").find({
            "title": {
                "$regex": "(%s)" % "|".join(query_keyword.split(" "))
            },
            "novel_type": {
                "$nin": block_settings
            }
        }).sort("words_count", -1).skip((page_index - 1) * page_size).limit(page_size)
        return [x for x in query_res]


@response_json
def query_novel_by_condition(request):
    """
    Query novel list by title <-- json condition
    :param request:
    :return:
    """
    query_condition = json.loads(request.GET["condition"])
    page_size = string.atoi(get_request_with_default(request, "n", "30"))
    page_index = string.atoi(get_request_with_default(request, "p", "1"))
    assert page_size >= 1
    assert page_index >= 1
    with MongoDBDatabase("website_pron") as mgdb:
        query_res = mgdb.get_collection(
            "novels"
        ).find(
            query_condition
        ).sort(
            "words_count", -1
        ).skip(
            (page_index - 1) * page_size
        ).limit(
            page_size
        )
        return [x for x in query_res]


@response_json
def query_video_list(request):
    """
    Query video list by title <-- generated regex
    :param request:
    :return:
    """
    query_keyword = request.GET["name"]
    page_size = string.atoi(get_request_with_default(request, "n", "30"))
    page_index = string.atoi(get_request_with_default(request, "p", "1"))
    assert page_size >= 1
    assert page_index >= 1
    with MongoDBDatabase("website_pron") as mgdb:
        query_res = mgdb.get_collection("video_info").find({
            "name": {
                "$regex": "(%s)" % "|".join(query_keyword.split(" "))
            }
        }).sort(
            "_id", -1
        ).skip(
            (page_index - 1) * page_size
        ).limit(
            page_size
        )
        return [x for x in query_res]

# Region: Operation to delete/modify database and filesystem
