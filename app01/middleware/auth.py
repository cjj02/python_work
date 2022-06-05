from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


# 新中间件得MiddlewareMixin,定义完成之后在settings里面加上  MIDDLEWARE ='app01.middleware.auth.AuthMiddleware',
class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的页面,如果该方法没有返回值就继续往后走
        #   request.path_info 获取当前用户请求的URL /login/  /image/code/
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 1.读取当前访问的用户的session信息，如果能读到，说明已登陆过，就可以继续向后走。
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            return

        # 2.没有登录过，重新回到登录页面
        return redirect('/login/')
