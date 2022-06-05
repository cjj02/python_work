from django.shortcuts import render, redirect, HttpResponse

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import BlogEditModelForm


def blog_list(request):
    data_dict = {}
    # 搜索框
    search_data = request.GET.get('q', "")
    if search_data:
        # Django特有函数找出用户名里面有这个值的对象
        data_dict["title__contains"] = search_data
    queryset = models.Blog.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset

    content = {
        'queryset': page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data,
    }
    return render(request, 'blog_list.html', content)


def blog_delete(request, nid):
    row_object = models.Blog.objects.filter(id=nid).first()
    row_object.delete()
    return redirect('/blog/list/')


def blog_edit(request, nid):
    row_object = models.Blog.objects.filter(id=nid).first()
    title = "编辑博客"
    if request.method == "GET":
        form = BlogEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})
    form = BlogEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/blog/list/')
    return render(request, 'change.html', {"form": form, "title": title})


def blog_create(request):
    title = "撰写博客"
    if request.method == "GET":
        form = BlogEditModelForm()
        return render(request, 'change.html', {"form": form, "title": title})
    form = BlogEditModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/blog/list/')
    return render(request, 'change.html', {"form": form, "title": title})
