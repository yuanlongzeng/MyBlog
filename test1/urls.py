"""test1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from blog.feeds import AllPosts
from login.views import signin, register, RegisterView, IndexView, SigninView
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.conf import settings
import blog
import xadmin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'', include('blog.urls')),
    # 空字符串时就匹配到首页---具体应该是放在blog这个应用中的urls中进行解析 如果是  r'/info/' 的话，那么最后匹配得到的网址应该是  /info/about  等
    url(r'^all/rss/$', AllPosts(), name='rss'),
    url(r'search/', include('haystack.urls')),
    url(r'^ck/', include('ckeditor_uploader.urls')),
    url(r'^ueditor/', include('DjangoUeditor.urls')),

    url(r'^index/', IndexView.as_view(), name='index'),
    # url(r'^login/', signin, name='login'),
    url(r'^login/', SigninView.as_view(), name='login'),
    # url(r'^register/', register, name='register'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'ueditor/',include("DjangoUeditor.urls")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#
# if settings.DEBUG is False:
#     urlpatterns += patterns('',
#                             url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
#                                 {'document_root': settings.STATIC_ROOT,
#                                  }),
#                             )

handler404 = blog.views.handler404  #不是写成字符串形式
