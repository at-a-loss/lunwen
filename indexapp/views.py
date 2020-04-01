import json
import os
import random
import string
import time
import uuid

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from redis import Redis

from indexapp.captcha.image import ImageCaptcha
from userapp.models import Users
from ymy_cmfz import settings

re = Redis(host='127.0.0.1', port=6379)
def index(request):
    return render(request, "index.html")

def login(request):
    name = request.COOKIES.get("name")
    # pwd = request.COOKIES.get("pwd")
    # user=User.objects.filter(username=name,pwd=pwd)
    # flag = request.COOKIES.get("flag")
    if name:
        request.session["name"] = name
        return redirect("indexapp:index")
    return render(request,"login.html")


def loginlogic(request):
    name=request.POST.get("name")
    pwd=request.POST.get("pwd")
    my=request.POST.get("my")
    pw=request.POST.get("pw")
    number=request.POST.get("number")
    user=Users.objects.filter(name=name,password=pwd)
    print(user)
    captcha=request.session.get("captcha")
    if captcha.lower()==number.lower():
        if user:
            re = redirect("indexapp:index")
            request.session["name"]=user[0].name
            if my:
                re.set_cookie("name",name,max_age=7*24*3600)
                # re.set_cookie("pwd",pwd,max_age=7*24*3600)
                # re.set_cookie("flag",True,max_age=7*24*3600)
            if pw:
                re.set_cookie("pwu", name, max_age=7 * 24 * 3600)
                re.set_cookie("pw",pw,max_age=7*24*3600)
            return re
        return HttpResponse("登录失败！")
    return HttpResponse("验证码错误！")

def loginAjax(request):
    pw=request.COOKIES.get("pw")
    pwu=request.COOKIES.get("pwu")
    name = request.GET.get("name")
    user=Users.objects.filter(name=name)
    if name==pwu:
        if pw and pwu:
            return HttpResponse(user[0].pwd)
    return HttpResponse("")

def captcha(request):
    img=ImageCaptcha()
    captcha="".join(random.sample(string.ascii_letters+string.digits,5))
    request.session["captcha"]=captcha
    print(captcha)
    return HttpResponse(img.generate(captcha),"image/png")

def captchaAjax(request):
    val=request.POST.get("val")
    captcha=request.session.get("captcha")
    time.sleep(0.5)
    if captcha.lower()==val.lower():
        return HttpResponse("可用！！")
    else:
        return HttpResponse("不可用！！")