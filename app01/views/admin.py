from django.shortcuts import render, redirect
from django import forms
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import AdminEditModelForm,AdminModelForm




def admin_list(request):
    data_dict = {}
    # 搜索框
    search_data = request.GET.get('q', "")
    if search_data:
        # Django特有函数找出用户名里面有这个值的对象
        data_dict["username__contains"] = search_data
    queryset = models.Admin.objects.filter(**data_dict)
    page_object = Pagination(request, queryset, 10)
    content = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data,
    }
    return render(request, 'admin_list.html', content)





def admin_add(request):
    # 添加管理员
    title = "新建管理员"
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, "change.html", {"form": form, "title": title})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, "change.html", {"form": form, "title": title})


def admin_edit(request, nid):
    """ 编辑管理员 """
    # 对象 / None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        # return render(request, 'error.html', {"msg": "数据不存在"})
        return redirect('/admin/list/')

    title = "编辑管理员"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {"form": form, "title": title})


def admin_delete(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    row_object.delete()
    return redirect('/admin/list/')
