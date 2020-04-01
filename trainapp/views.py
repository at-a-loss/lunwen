import json
import os
import uuid

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from trainapp.models import Train
from userapp.models import Dept, Users


def data(request):
    num=request.GET.get("page")
    rownum=request.GET.get("rows")
    id=request.GET.get("id")
    name=request.GET.get("name")
    trains=Train.objects.filter(status=1)
    if id or name:
        user1=trains.filter(id=id)
        user2=trains.filter(name=name)
        user=user1 | user2

    else:
        user=trains
    pagtor=Paginator(user,rownum)
    page=pagtor.page(num)
    data={
        "page":num,
        "total":pagtor.num_pages,
        "records":pagtor.count,
        "rows":list(page)
    }
    users=json.dumps(data,default=user_default)
    return HttpResponse(users)


@csrf_exempt
def opener(request):
    oper=request.POST.get("oper")
    id = request.POST.get("id")
    phone = request.POST.get("phone")
    dept_id = request.POST.get("dept_id")
    if oper=="edit":
        u = Train.objects.get(pk=id)
        u.phone=phone
        u.dept_id = Dept.objects.get(name=dept_id)
        u.save()
    elif oper=="del":
        u = Train.objects.get(pk=id)
        u.delete()
    return HttpResponse("1")

def add(request):
    id=request.GET.get("id")
    train=Train.objects.get(pk=id)
    print(train.addr)
    if train.addr[0]=="内" or train.addr[0]=="黑":
        addr1 =train.addr[0:1]
    else:
        addr1 = train.addr[0:2]
    try:
        Users.objects.create(name=train.name,password=123,gender=train.gender,phone=train.phone,addr1=addr1,addr2=train.addr,head=train.head,freeze=1,dept_id=train.dept_id,performance=0)
        train.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

def user_default(u):
    if isinstance(u,Train):
        if u.gender:
            gender="男"
        else:
            gender="女"
        if u.status:
            status = "培训"
        else:
            status = "招聘"
        return {"id":u.id,"name":u.name,"gender":gender,"create_time":u.create_time.strftime("%Y-%m-%d %H:%M:%S"),"head":u.head.url,"phone":u.phone,"addr":u.addr,"dept_id":u.dept_id.name}