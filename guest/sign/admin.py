# -*- coding: utf-8 -*-


# Register your models here.
# 数据库内容映射到默认的后台，把models的数据库映射到admin后台

from django.contrib import admin
from sign.models import Event, Guest


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'start_time', 'id']
    search_fields = ['name']  # 搜索功能
    list_filter = ['status']  # 过滤器


class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone', 'email', 'sign', 'create_time', 'event_id']
    list_display_links = ('realname', 'phone')  # 显示链接
    search_fields = ['realname', 'phone']  # 搜索功能
    list_filter = ['event_id']  # 过滤器


admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
