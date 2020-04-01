import json
import os
import uuid

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from trainapp.models import Train
from userapp.models import Dept


@csrf_exempt
def editAttendance(request):
    name = request.POST.get("name")
    gender = request.POST.get("gender")
    phone = request.POST.get("phone")
    addr = request.POST.get("addr")
    dept = request.POST.get("dept")
    head = request.FILES.get("head")
    head.name = str(uuid.uuid4()) + os.path.splitext(head.name)[1]
    try:
        Train.objects.create(name=name,gender=gender,phone=phone,addr=addr,head=head,status=0,dept_id=Dept.objects.get(pk=dept))
        return HttpResponse("1")
    except:
        return HttpResponse("0")

def data(request):
    num=request.GET.get("page")
    rownum=request.GET.get("rows")
    id=request.GET.get("id")
    name=request.GET.get("name")
    trains=Train.objects.filter(status=0)
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

def get_status(request):
    sel = "<select>"
    sel += "<option value='招聘'>招聘</option>"
    sel += "<option value='培训'>培训</option>"
    sel += "</select>"
    return HttpResponse(sel)

@csrf_exempt
def opener(request):
    status=request.POST.get("status")
    oper=request.POST.get("oper")
    id = request.POST.get("id")
    phone = request.POST.get("phone")
    dept_id = request.POST.get("dept_id")
    if oper=="edit":
        u = Train.objects.get(pk=id)
        u.phone=phone
        u.dept_id = Dept.objects.get(name=dept_id)
        if status=="培训":
            u.status=1
        else:
            u.status = 0
        u.save()
    elif oper=="del":
        u = Train.objects.get(pk=id)
        u.delete()
    return HttpResponse("1")


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
        return {"id":u.id,"name":u.name,"gender":gender,"create_time":u.create_time.strftime("%Y-%m-%d %H:%M:%S"),"head":u.head.url,"phone":u.phone,"addr":u.addr,"status":status,"dept_id":u.dept_id.name}