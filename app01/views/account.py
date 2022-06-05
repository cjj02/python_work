from django.shortcuts import render, HttpResponse, redirect


from app01 import models
from app01.utils.form import LoginForm
from app01.utils.code import check_code
from io import BytesIO





def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取到的用户名和密码
        # form.cleaned_data={'username': 'wupeiqi', 'password': '123',"code":123}

        # 验证码的校验
        # pop的不同之处就是放入数据库之前先把code字段剔除掉
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确，获取用户对象、None
        # admin_object = models.Admin.objects.filter(username=xxx, password=xxx).first()
        # .first()特殊的功能可以把QuerySet对象转换为字典对象，方便字典对象点属性取值
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        # 如果没有对应上
        if not admin_object:
            # 添加错误,文本添加到密码框下边
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/cover/")

    return render(request, 'login.html', {'form': form})


def logout(request):
    """ 注销 """

    request.session.clear()

    return redirect('/login/')


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)
    # 内存里面的文件对象,将图片写到里面去
    stream = BytesIO()
    img.save(stream, 'png')
    # 返回图片里面的内容
    return HttpResponse(stream.getvalue())
