# coding:utf-8


def get_request_get(request, key):
    try:
        return request.GET[key]
    except:
        return None


def get_request_get_default(request, key, default_value):
    try:
        return request.GET[key]
    except:
        return default_value
