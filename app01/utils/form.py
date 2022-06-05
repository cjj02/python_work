from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm


# 这些类默认继承BootStrapModelForm
class MomForm(BootStrapModelForm):
    mobile = forms.CharField(
        label="手机号",
        # 网上查的手机号验证正则表达式,r'之后$之前就是正则表达式,1开头,第二个数字3~9,后面九位全是数字
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    name = forms.CharField(
        min_length=1,
        label="昵称",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "age", 'mobile']


# 继承自带BootStrap样式的ModelForm
class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin  # 显示的数据库
        fields = ['username', 'password']  # 想显示几个字段就加几个字段


class AdminModelForm(BootStrapModelForm):
    # 加一个在数据库内不存在的数据项:确认密码
    confirm_password = forms.CharField(label="确认密码",
                                       widget=forms.PasswordInput(render_value=True),
                                       )

    class Meta:
        model = models.Admin
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)  # 每次返回页面时显示的是上一次输入的密码
        }


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']

        # 判断用户名是否存在
        if models.Admin.objects.filter(username=username).exists():
            # 存在即不符合规则，必须抛出ValidationError异常
            raise ValidationError('该用户名已存在')
        # 校验通过，则返回清洗后的数据
        return self.cleaned_data['username']


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label="确认密码",
                                       widget=forms.PasswordInput(render_value=True),
                                       )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        # 判断用户名是否存在
        if models.Admin.objects.filter(username=username).count():
            # 存在即不符合规则，必须抛出ValidationError异常
            raise ValidationError('该用户名已存在')
        # 校验通过，则返回清洗后的数据
        return self.cleaned_data['username']

    # 密码验证函数
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if pwd != confirm:
            raise ValidationError("密码不一致,请重新输入")
        # 返回什么,此字段以后要返回什么
        return confirm


class LoginForm(BootStrapForm):
    username = forms.CharField(label="用户名",
                               widget=forms.TextInput,
                               required=True,  # 该空不为空
                               )
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(render_value=True),  # 刷新时密码还在
                               required=True,
                               )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )


class BlogEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Blog
        fields = ['title', 'contain']
