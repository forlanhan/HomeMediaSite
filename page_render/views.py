# -*- coding: utf-8 -*-
from django.shortcuts import render
from api.views import get_novel_object


def render_query_novel(request):
    return render(request, "query_novel.html")


def render_novel_reader(request):
    novel_info = get_novel_object(request)
    novel_text = novel_info["novel_text"].replace(r"　", " ")
    lastSize = len(novel_text)
    while (True):
        novel_text = novel_text.replace("   ", "  ")
        if len(novel_text) == lastSize:
            break
        else:
            lastSize = len(novel_text)
    return render(request, "read_novel.html", {
        "title": novel_info["title"],
        "text": novel_text.replace("  ", "\n")
    })


def render_task_manage_page(request):
    return render(request, "task_manage.html")
