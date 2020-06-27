"""memo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import (
    MemoList, MemoDetail, MemoCreate, MemoDelete, MemoUpdate, MemoListAPI, MemoRetirieveAPI, MemoCreateAPI, MemoUpdateAPI, MemoDestroyAPI,
)

app_name = 'memo'
urlpatterns = [
    path('', MemoList.as_view(), name='index'),
    path('new_memo', MemoCreate.as_view(), name='new_memo'),
    path('detail/<slug:slug>', MemoDetail.as_view(), name='detail'),
    path('delete/<slug:slug>', MemoDelete.as_view(), name='delete_memo'),
    path('edit/<slug:slug>', MemoUpdate.as_view(), name='edit_memo'),
    path('api/memos/', MemoListAPI.as_view(), name='api_list'),
    path('api/memos/<slug:slug>/', MemoRetirieveAPI.as_view(), name='api_retrieve'),
    path('api/memos/new/', MemoCreateAPI.as_view(), name='api_create'),
    path('api/memos/edit/<slug:slug>/', MemoUpdateAPI.as_view(), name='api_update'),
    path('api/memos/delete/<slug:slug>/', MemoDestroyAPI.as_view(), name='api_delete'),
]
