"""day16 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app01.views import admin, account, mom, blog,cover
from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 登录页面
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),
    # 母亲个人信息
    path('mom/list/', mom.mom_list),
    path('mom/<int:nid>/edit/', mom.mom_edit),
    # 母亲账号管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    # 博客信息
    path('blog/list/', blog.blog_list),
    path('blog/<int:nid>/delete/', blog.blog_delete),
    path('blog/<int:nid>/edit/', blog.blog_edit),
    path('blog/create/', blog.blog_create),
    #封面大图
    path('cover/',cover.cover),
]
