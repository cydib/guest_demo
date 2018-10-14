#!/usr/bin/env python
# -*- coding: GBK -*-
# @Date    : 2018-07-01 22:07:57
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

# 视图层，处理请求，获取信息
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    # return HttpResponse("<html><h1>Hello Django!</h1></html>")
    return render(request, "index.html")


def login_action(request):
    if request.method == "POST":
        page_username = request.POST.get("username", "")  # admin
        page_password = request.POST.get("password", "")  # admin123
        if page_username == "" or page_password == "":
            error = "username or password null"
            return render(request, "index.html", {"index_error": error})

        user = auth.authenticate(username=page_username, password=page_password)
        if user is not None:  # 如果用户不是空
            auth.login(request, user)  # 登录
            response = HttpResponseRedirect("/event_manage/")
            request.session["user"] = page_username  # 将session信息记录到浏览器中
            return response
        else:
            error = "username or password error！"
            return render(request, "index.html", {"index_error": error})

    else:
        return render(request, "index.html")


@login_required()
def event_manage(request):
    events = Event.objects.all()
    # username =request.COOKIES.get("user", "")# 读取浏览器cooie
    username = request.session.get("user", "")  # 读取浏览器session
    return render(request, "event_manage.html", {"event_user": username,
                                                 "events_list": events})


@login_required()
def guest_manage(request):
    username = request.session.get('user', '')
    guests = Guest.objects.all()
    paginator = Paginator(guests, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"guest_user": username, "guests_list": contacts})


@login_required()
def search_name(request):
    search_name = request.GET.get("name", '')
    username = request.session.get("user", "")  # 读取浏览器session
    events = Event.objects.filter(name__contains=search_name)
    if len(events) == 0:
        return render(request, "event_manage.html", {"event_list": username,
                                                     "hint": "根据输入的 `发布会名称` 查询结果为空！"})
    return render(request, "event_manage.html", {"event_list": username, "events_list": events})


@login_required()
def search_phone(request):
    search_name = request.GET.get("phone", "")
    username = request.session.get("user", "")
    guests = Guest.objects.filter(phone__contains=search_name)
    if len(guests) == 0:
        return render(request, "guest_manage.html", {"guests_list": guests})
    return render(request, "guest_manage.html", {"guest_user": username, "guests_list": guests})


@login_required()
def sign_index(request, event_id):
    username = request.session.get("user", "")
    event = get_object_or_404(Event, id=event_id)
    return render(request, "sign_index.html", {"event": event, "user": username})


@login_required()
def logout(request):
    auth.logout(request)
    respones = HttpResponseRedirect("/index/")
    return respones


@login_required
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone', '')  # 获取表单中输入的手机号
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, "sign_index.html", {'event': event, 'hint': 'Phone number does not exist'})

    result = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result:
        return render(request, "sign_index.html", {'event': event, 'hint': 'event id or phone error'})

    result = Guest.objects.get(phone=phone, event_id=event_id)
    if result.sign:
        return render(request, "sign_index.html", {'event': event, 'hint': 'user already sign in'})
    else:
        Guest.objects.filter(phone=phone, event_id=event_id).update(sign=1)
        return render(request, "sign_index.html", {'event': event, 'hint': 'Sign in success', 'guest': result})
