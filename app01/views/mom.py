from django.shortcuts import render, redirect

from app01.utils.pagination import Pagination
from app01.utils.form import MomForm, AdminEditModelForm
from app01 import models


def mom_list(request):
    """ 个人信息管理"""

    queryset = models.MomInfo.objects.all()

    return render(request, 'mon_list.html', {'queryset': queryset})


def mom_edit(request, nid):
    """ 编辑个人信息 """
    row_object = models.MomInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = MomForm(instance=row_object)
        return render(request, 'mom_edit.html', {'form': form})

    form = MomForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要再用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/mom/list/')
    return render(request, 'mom_edit.html', {"form": form})


def mom_account_edit(request, nid):
    """ 编辑管理员 """
    # 对象 / None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        # return render(request, 'error.html', {"msg": "数据不存在"})
        return redirect('/mom/list/account/')

    title = "编辑账户"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/mom/list/account/')
    return render(request, 'change.html', {"form": form, "title": title})


def mom_account_delete(request, nid):
    """ 管理员删除 """
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/mom/list/account/")


def mom_list_account(request):
    """ 管理员列表 """
    data_dict = {}
    # 搜索框
    search_data = request.GET.get('q', "")
    if search_data:
        # Django特有函数找出用户名里面有这个值的对象
        data_dict["username__contains"] = search_data
    queryset = models.Admin.objects.filter(**data_dict)

    page_object = Pagination(request, queryset)

    content = {
        'queryset': queryset,
        'page_string': page_object.html(),
        'search_data': search_data,
    }
    return render(request, 'mom_list_account.html', content)
