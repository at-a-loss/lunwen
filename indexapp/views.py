import json
import os
import uuid

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from redis import Redis

from indexapp.models import Pic
from utils.send_mess import YunPian
from utils.random_code import get_mas
from ymy_cmfz import settings

re = Redis(host='127.0.0.1', port=6379)
def index(request):
    return render(request, "index.html")

def login(request):
    return render(request,"login.html")

@csrf_exempt
def get_code(request):
    mobile = request.POST.get('mobile')
    data=re.get(mobile+"_1")
    if data:
        return HttpResponse("0")
    else:
        mas=get_mas()
        yunpian = YunPian(settings.APIKEY)
        yunpian.send_message(mobile,mas)
        re.setex(mobile+"_1",3*60, mas)
        re.setex(mobile + "_2", 30 * 60, mas)
        return HttpResponse("1")

@csrf_exempt
def loginlogic(request):
    mobile = request.POST.get('mobile')
    code = request.POST.get('code')
    mas=re.get(mobile+"_2")
    if mas:
        if mas.decode()==code:
            return HttpResponse("1")
        else:
            return HttpResponse("2")
    return HttpResponse("0")

@csrf_exempt
def add_pic(request):
    title = request.POST.get("title")
    status = request.POST.get("status")
    pic = request.FILES.get("pic")
    pic.name = str(uuid.uuid4()) + os.path.splitext(pic.name)[1]
    Pic.objects.create(title=title,status=status,pic=pic)
    return HttpResponse("1")


def data(request):
    num=request.GET.get("page")
    rownum=request.GET.get("rows")
    emp=Pic.objects.all()
    pagtor=Paginator(emp,rownum)
    page=pagtor.page(num)
    data={
        "page":num,
        "total":pagtor.num_pages,
        "records":pagtor.count,
        "rows":list(page)
    }
    emps=json.dumps(data,default=pic_default)
    return HttpResponse(emps)

@csrf_exempt
def opener(request):
    title=request.POST.get("title")
    status=request.POST.get("status")
    create_time=request.POST.get("create_time")
    oper=request.POST.get("oper")
    id = request.POST.get("id")
    if oper=="edit":
        p = Pic.objects.get(pk=id)
        p.title=title
        p.create_time=create_time
        if status=="显示":
            p.status=1
        else:
            p.status = 0
        p.save()
    elif oper=="del":
        p = Pic.objects.get(pk=id)
        p.delete()
    return HttpResponse("1")

def get_status(request):
    sel = "<select>"
    sel += "<option value='显示'>显示</option>"
    sel += "<option value='不显示'>不显示</option>"
    sel += "</select>"
    return HttpResponse(sel)

def pic_default(p):
    if isinstance(p,Pic):
        if p.status:
            status="显示"
        else:
            status="不显示"
        return {"id":p.id,"title":p.title,"status":status,"create_time":p.create_time.strftime("%Y-%m-%d %H:%M:%S"),"pic":p.pic.url}