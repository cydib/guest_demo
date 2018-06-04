# -*- coding: utf-8 -*-
# 视图层，处理请求，获取信息
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest


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

        # if page_username != "admin" and page_password != "123":
        #     error = "username   or password error"
        #     return render(request, "index.html", {"index_error": error})
        # elif page_username == "admin" and page_password != "123":
        #     error = "username or password error"
        #     return render(request, "index.html", {"index_error": error})
        # elif page_username != "admin" and page_password == "123":
        #     error = "username or password error"
        #     return render(request, "index.html", {"index_error": error})
        # else:
        #     #return render(request, "event_manage.html")
        #     # return HttpResponseRedirect('/event_manage/')#重定向
        #     # cookie使用
        #     # respone = HttpResponseRedirect("/event_manage/")
        #     # respone.set_cookie("user", username, 3600)
        #     # return respone
        #
        #     # session使用
        #     respone = HttpResponseRedirect("/event_manage/")
        #     request.session["user"] = username # 将session信息记录到浏览器中
        #     return respone


@login_required()
def event_manage(request):
    events = Event.objects.all()
    # username =request.COOKIES.get("user", "")# 读取浏览器cooie
    username = request.session.get("user", "")  # 读取浏览器session
    return render(request, "event_manage.html", {"event_user": username,
                                                 "events_list": events})
