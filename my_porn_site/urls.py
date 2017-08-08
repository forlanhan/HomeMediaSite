"""my_porn_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from api.views import *
from bgtasks.views import *
from page_render.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^get/images/', get_image_list),
    url(r'^get/novel/', get_novel),

    url(r'^query/novel/bytitle', query_novel_by_title),
    url(r'^query/video/bytitle', query_video_list),

    url(r'^query/task/all', query_tasks),

    url(r'^view/query/novel', render_query_novel),
    url(r'^view/novel', render_novel_reader),

    url(r'^append/task', append_task),
    url(r'^remove/task', remove_task),
    url(r'^manage/tasks', render_task_manage_page),
]
