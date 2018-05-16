from django.conf.urls import url,include
from . import views


app_name = 'blog'  # 视图函数命名空间
urlpatterns = [
    # 以空字符串开头且以空字符串结尾
    # url(r'^$',views.index,name='index'),  # url映射文件/处理函数  name处理函数 index 的别名
    # # (?P<pk>[0-9]+) 表示命名捕获组,把传过来的pk（符合后面的RE 规则的字符串）,作为参数传递给views解析，要一样才行
    # # Django 会从用户访问的 URL 中自动提取这两个参数的值，然后传递给其对应的视图函数
    #url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name="detail"),
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives, name='archives'),
    #url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),

    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchiveView.as_view(), name='archives'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.PostDetailView.as_view(),name="detail"),
    url(r'tag/(?P<pk>[0-9]+)/$',views.TagView.as_view(),name='tag'),
    url(r'^contact/',views.contact,name='contact'),
    # url(r'^fill/$', views.postMF, name='fill'),
    #url(r'^captcha/', include('captcha.urls')),
    #url(r'^search/$', views.search, name='search'),  # 使用现成的app:haystack
]
