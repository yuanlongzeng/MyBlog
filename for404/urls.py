from django.conf.urls import url
from . import views

app_name = 'blog'  # 视图函数命名空间
urlpatterns = [
url(r'^no/$', views.page_not_found, name='search'),]